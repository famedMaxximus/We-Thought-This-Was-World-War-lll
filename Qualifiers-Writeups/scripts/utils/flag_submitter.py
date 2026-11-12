#!/usr/bin/env python3
"""
Flag Submitter for LCA Finals
Batch submits verified flags with validation, deduplication, and rate limiting.
"""
import asyncio
import aiohttp
import re
import os
import sys
import json
from pathlib import Path
from typing import Set, List, Dict, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict

FLAG_REGEX = re.compile(r"LsCTF2026\{[^}]+\}")
FLAG_PREFIX = "LsCTF2026{"

# Configuration
SUBMIT_URL = os.getenv("LCA_SUBMIT_URL", "https://lca.labs.ctfroom.com/api/submit")
TEAM_TOKEN = os.getenv("LCA_TEAM_TOKEN", "")
RATE_LIMIT = float(os.getenv("SUBMIT_RATE_LIMIT", "0.5"))  # seconds between requests
MAX_CONCURRENT = int(os.getenv("MAX_CONCURRENT", "3"))
RETRY_ATTEMPTS = int(os.getenv("RETRY_ATTEMPTS", "3"))
RETRY_DELAY = float(os.getenv("RETRY_DELAY", "1.0"))

console = Console()


@dataclass
class SubmissionResult:
    flag: str
    success: bool
    response: Dict
    timestamp: str
    attempts: int
    error: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)


class FlagSubmitter:
    def __init__(self, token: str = None, submit_url: str = None):
        self.token = token or TEAM_TOKEN
        self.submit_url = submit_url or SUBMIT_URL
        self.session: Optional[aiohttp.ClientSession] = None
        self.semaphore = asyncio.Semaphore(MAX_CONCURRENT)
        self.submitted: Set[str] = set()
        self.results: List[SubmissionResult] = []
        self.submitted_file = Path("submitted_flags.txt")

    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
            headers={"Authorization": f"Bearer {self.token}"} if self.token else {}
        )
        # Load previously submitted flags
        if self.submitted_file.exists():
            self.submitted = set(self.submitted_file.read_text().strip().split())
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def extract_flags(self, source: Path) -> Set[str]:
        """Extract all flags from a file or directory."""
        flags = set()
        if source.is_file():
            text = source.read_text(encoding='utf-8', errors='ignore')
            flags.update(re.findall(FLAG_REGEX, text))
        elif source.is_dir():
            for md_file in source.rglob("*.md"):
                try:
                    text = md_file.read_text(encoding='utf-8', errors='ignore')
                    flags.update(re.findall(FLAG_REGEX, text))
                except Exception:
                    pass
        return flags

    def load_verified_flags(self, flag_index: Path) -> Set[str]:
        """Load only VERIFIED flags from FLAG_INDEX.md."""
        flags = set()
        if flag_index.exists():
            text = flag_index.read_text()
            for line in text.splitlines():
                if "VERIFIED" in line.upper():
                    for flag in FLAG_REGEX.findall(line):
                        yield flag
        return set()

    def normalize_flag(self, flag: str) -> str:
        """Normalize flag format."""
        flag = flag.strip()
        if not flag.startswith(FLAG_PREFIX):
            match = FLAG_REGEX.search(flag)
            if match:
                return match.group()
        return flag

    def validate_flag(self, flag: str) -> Tuple[bool, str]:
        """Validate flag format."""
        flag = self.normalize_flag(flag)
        if not flag.startswith(FLAG_PREFIX):
            return False, "Missing prefix"
        if not flag.endswith("}"):
            return False, "Missing closing brace"
        if flag.count("{") != 1 or flag.count("}") != 1:
            return False, "Mismatched braces"
        inner = flag[len(FLAG_PREFIX):-1]
        if not inner:
            return False, "Empty content"
        if len(flag) > 256:
            return False, "Too long"
        return True, ""

    async def submit_single(self, flag: str) -> SubmissionResult:
        """Submit a single flag with retries."""
        flag = self.normalize_flag(flag)
        valid, error = self.validate_flag(flag)
        if not valid:
            return SubmissionResult(
                flag=flag,
                success=False,
                response={},
                timestamp=datetime.utcnow().isoformat(),
                attempts=0,
                error=f"Validation failed: {error}"
            )

        if flag in self.submitted:
            return SubmissionResult(
                flag=flag,
                success=True,
                response={"message": "Already submitted"},
                timestamp=datetime.utcnow().isoformat(),
                attempts=0,
                error="Duplicate - already submitted"
            )

        async with self.semaphore:
            for attempt in range(1, RETRY_ATTEMPTS + 1):
                try:
                    await asyncio.sleep(RATE_LIMIT)
                    async with self.session.post(
                        self.submit_url,
                        json={"flag": flag}
                    ) as resp:
                        response = await resp.json()
                        
                        if resp.status == 200:
                            success = response.get("correct", False) or response.get("success", False)
                            if success:
                                self.submitted.add(flag)
                                self._save_submitted()
                                return SubmissionResult(
                                    flag=flag,
                                    success=True,
                                    response=response,
                                    timestamp=datetime.utcnow().isoformat(),
                                    attempts=attempt
                                )
                            else:
                                error_msg = response.get("message", "Incorrect flag")
                                if attempt == RETRY_ATTEMPTS:
                                    return SubmissionResult(
                                        flag=flag,
                                        success=False,
                                        response=response,
                                        timestamp=datetime.utcnow().isoformat(),
                                        attempts=attempt,
                                        error=error_msg
                                    )
                        else:
                            error_msg = f"HTTP {resp.status}: {await resp.text()}"
                            if attempt == RETRY_ATTEMPTS:
                                return SubmissionResult(
                                    flag=flag,
                                    success=False,
                                    response={"status": resp.status},
                                    timestamp=datetime.utcnow().isoformat(),
                                    attempts=attempt,
                                    error=error_msg
                                )
                
                except asyncio.TimeoutError:
                    if attempt == RETRY_ATTEMPTS:
                        return SubmissionResult(
                            flag=flag,
                            success=False,
                            response={},
                            timestamp=datetime.utcnow().isoformat(),
                            attempts=attempt,
                            error="Request timeout"
                        )
                except Exception as e:
                    if attempt == RETRY_ATTEMPTS:
                        return SubmissionResult(
                            flag=flag,
                            success=False,
                            response={},
                            timestamp=datetime.utcnow().isoformat(),
                            attempts=attempt,
                            error=str(e)
                        )
                
                await asyncio.sleep(RETRY_DELAY * attempt)
        
        return SubmissionResult(
            flag=flag,
            success=False,
            response={},
            timestamp=datetime.utcnow().isoformat(),
            attempts=RETRY_ATTEMPTS,
            error="Max retries exceeded"
        )

    def _save_submitted(self):
        """Save submitted flags to file."""
        self.submitted_file.write_text("\n".join(sorted(self.submitted)) + "\n")

    async def submit_all(self, flags: List[str]) -> List[SubmissionResult]:
        """Submit all flags concurrently."""
        console.print(f"[bold]Submitting {len(flags)} flags...[/bold]")
        
        tasks = [self.submit_single(flag) for flag in flags]
        results = []
        
        with Live(console=console, refresh_per_second=4) as live:
            for i, task in enumerate(asyncio.as_completed(tasks), 1):
                result = await task
                self.results.append(result)
                
                # Update progress
                status = "SUCCESS" if result.success else "FAILED"
                color = "green" if result.success else "red"
                live.update(Panel(
                    f"[bold]Progress: {i}/{len(flags)}[/bold]\n"
                    f"[{color}]{status}[/{color}] {result.flag}\n"
                    f"Attempts: {result.attempts}\n"
                    f"{result.error if not result.success else ''}",
                    title=f"Submitting Flags",
                    border_style="green" if result.success else "red"
                ))
        
        return self.results

    def generate_report(self) -> str:
        """Generate submission report."""
        total = len(self.results)
        successful = sum(1 for r in self.results if r.success)
        failed = total - successful
        
        lines = [
            f"# Flag Submission Report",
            f"Generated: {datetime.utcnow().isoformat()}",
            f"",
            f"## Summary",
            f"- Total: {total}",
            f"- Successful: {successful}",
            f"- Failed: {failed}",
            f"- Success Rate: {successful/total*100:.1f}%" if total > 0 else "N/A",
            f"",
            f"## Details",
        ]
        
        for r in self.results:
            status = "PASS" if r.success else "FAIL"
            lines.append(f"- [{status}] {r.flag} (attempts: {r.attempts})")
            if r.error:
                lines.append(f"  Error: {r.error}")
        
        return "\n".join(lines)

    def save_report(self, path: Path):
        """Save detailed report to file."""
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "summary": {
                "total": len(self.results),
                "successful": sum(1 for r in self.results if r.success),
                "failed": sum(1 for r in self.results if not r.success),
            },
            "results": [asdict(r) for r in self.results]
        }
        path.write_text(json.dumps(report, indent=2))


async def main():
    import argparse
    parser = argparse.ArgumentParser(description="LCA Flag Submitter")
    parser.add_argument("--flags", "-f", help="Flags file or directory to scan")
    parser.add_argument("--flag-index", help="FLAG_INDEX.md path (load verified only)")
    parser.add_argument("--token", help="LCA team token (or LCA_TEAM_TOKEN env)")
    parser.add_argument("--url", help="Submit URL (or LCA_SUBMIT_URL env)")
    parser.add_argument("--output", "-o", help="Output report file")
    parser.add_argument("--dry-run", action="store_true", help="Validate only, don't submit")
    args = parser.parse_args()

    if not args.flags and not args.flag_index:
        console.print("[red]Error: Must provide --flags or --flag-index[/red]")
        sys.exit(1)

    token = args.token or TEAM_TOKEN
    if not token:
        console.print("[red]Error: No token provided. Set LCA_TEAM_TOKEN or use --token[/red]")
        sys.exit(1)

    submitter = FlagSubmitter(token=token, submit_url=args.url)
    
    async with submitter:
        flags = set()
        
        if args.flag_index:
            flags.update(submitter.load_verified_flags(Path(args.flag_index)))
            console.print(f"Loaded {len(flags)} verified flags from {args.flag_index}")
        
        if args.flags:
            source = Path(args.flags)
            extracted = submitter.extract_flags(source)
            flags.update(extracted)
            console.print(f"Extracted {len(extracted)} flags from {args.flags}")
        
        if not flags:
            console.print("[yellow]No flags found[/yellow]")
            return

        # Normalize and validate
        valid_flags = []
        for flag in flags:
            flag = submitter.normalize_flag(flag)
            valid, error = submitter.validate_flag(flag)
            if valid:
                valid_flags.append(flag)
            else:
                console.print(f"[red]Invalid flag skipped: {flag} ({error})[/red]")

        # Deduplicate
        seen = set()
        unique_flags = []
        for f in valid_flags:
            if f not in seen:
                seen.add(f)
                unique_flags.append(f)

        console.print(f"[bold]Ready to submit {len(unique_flags)} unique flags[/bold]")
        
        if args.dry_run:
            console.print("[yellow]DRY RUN - Not submitting[/yellow]")
            for f in unique_flags:
                console.print(f"  {f}")
            return

        # Submit
        results = await submitter.submit_all(unique_flags)
        
        # Report
        successful = sum(1 for r in results if r.success)
        console.print(f"\n[bold]Results: {successful}/{len(results)} successful[/bold]")
        
        if args.output:
            out_path = Path(args.output)
            submitter.save_report(out_path)
            console.print(f"Report saved to {out_path}")
        
        # Print failures
        for r in results:
            if not r.success:
                console.print(f"[red]FAIL: {r.flag} - {r.error}[/red]")


if __name__ == "__main__":
    asyncio.run(main())