#!/usr/bin/env python3
"""
Flag Formatter & Validator for LsCTF2026
Normalizes, validates, and deduplicates flags.
"""
import re
import sys
from pathlib import Path
from typing import Set, List, Tuple

FLAG_REGEX = re.compile(r"LsCTF2026\{[^}]+\}")
FLAG_PREFIX = "LsCTF2026{"

class FlagFormatter:
    def __init__(self):
        self.flags: Set[str] = set()
        self.invalid: List[Tuple[str, str]] = []

    def extract_from_text(self, text: str) -> Set[str]:
        """Extract all flag-like strings from text."""
        return set(FLAG_REGEX.findall(text))

    def extract_from_file(self, path: Path) -> Set[str]:
        """Extract flags from a file."""
        try:
            text = path.read_text(encoding='utf-8', errors='ignore')
            return self.extract_from_text(text)
        except Exception as e:
            self.invalid.append((str(path), str(e)))
            return set()

    def extract_from_dir(self, directory: Path, pattern: str = "**/*.md") -> Set[str]:
        """Extract flags from all matching files in directory."""
        flags = set()
        for path in directory.rglob(pattern):
            if path.is_file():
                flags.update(self.extract_from_file(path))
        return flags

    def validate_flag(self, flag: str) -> Tuple[bool, str]:
        """
        Validate flag format.
        Returns (is_valid, error_message)
        """
        if not flag.startswith(FLAG_PREFIX):
            return False, f"Missing prefix '{FLAG_PREFIX}'"
        if not flag.endswith("}"):
            return False, "Missing closing brace"
        if flag.count("{") != 1 or flag.count("}") != 1:
            return False, "Mismatched braces"
        inner = flag[len(FLAG_PREFIX):-1]
        if not inner:
            return False, "Empty flag content"
        if len(flag) > 256:
            return False, "Flag too long (>256 chars)"
        # Check for suspicious patterns
        if " " in inner and not inner.startswith("{"):
            # Allow spaces in content but flag it
            pass
        return True, ""

    def normalize(self, flag: str) -> str:
        """Normalize flag (strip whitespace, ensure format)."""
        flag = flag.strip()
        if not flag.startswith(FLAG_PREFIX):
            # Try to find flag inside
            match = FLAG_REGEX.search(flag)
            if match:
                return match.group()
        return flag

    def add(self, flag: str) -> bool:
        """Add flag after validation and normalization."""
        flag = self.normalize(flag)
        valid, error = self.validate_flag(flag)
        if not valid:
            self.invalid.append((flag, error))
            return False
        self.flags.add(flag)
        return True

    def load_from_flag_index(self, path: Path) -> int:
        """Load verified flags from FLAG_INDEX.md."""
        count = 0
        try:
            text = path.read_text()
            # Only get flags marked VERIFIED
            for line in text.splitlines():
                if "VERIFIED" in line.upper():
                    for flag in FLAG_REGEX.findall(line):
                        self.add(flag)
                        count += 1
        except Exception as e:
            self.invalid.append((str(path), str(e)))
        return count

    def deduplicate(self, flags: List[str]) -> List[str]:
        """Remove duplicates while preserving order."""
        seen = set()
        result = []
        for f in flags:
            norm = self.normalize(f)
            if norm not in seen:
                seen.add(norm)
                result.append(norm)
        return result

    def report(self) -> str:
        """Generate report."""
        lines = [
            f"Total flags: {len(self.flags)}",
            f"Invalid entries: {len(self.invalid)}",
            "",
            "Flags:"
        ]
        for flag in sorted(self.flags):
            lines.append(f"  {flag}")
        if self.invalid:
            lines.append("\nInvalid:")
            for flag, error in self.invalid:
                lines.append(f"  {flag} -> {error}")
        return "\n".join(lines)

    def save(self, path: Path):
        """Save flags to file, one per line."""
        path.write_text("\n".join(sorted(self.flags)) + "\n")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Flag formatter and validator")
    parser.add_argument("--input", "-i", help="Input directory to scan")
    parser.add_argument("--flag-index", help="FLAG_INDEX.md path")
    parser.add_argument("--output", "-o", help="Output file for flags")
    parser.add_argument("--verify", action="store_true", help="Validate all flags")
    args = parser.parse_args()

    formatter = FlagFormatter()

    if args.flag_index:
        idx_path = Path(args.flag_index)
        if idx_path.exists():
            count = formatter.load_from_flag_index(idx_path)
            print(f"Loaded {count} verified flags from {idx_path}")

    if args.input:
        in_path = Path(args.input)
        if in_path.is_dir():
            flags = formatter.extract_from_dir(in_path)
            for f in flags:
                formatter.add(f)
            print(f"Extracted {len(flags)} flags from {args.input}")
        elif in_path.is_file():
            flags = formatter.extract_from_file(in_path)
            for f in flags:
                formatter.add(f)
            print(f"Extracted {len(flags)} flags from {args.input}")

    if args.verify:
        print("\nValidation Results:")
        for flag in sorted(formatter.flags):
            valid, error = formatter.validate_flag(flag)
            status = "✅" if valid else f"❌ ({error})"
            print(f"  {status} {flag}")

    if args.output:
        out_path = Path(args.output)
        formatter.save(out_path)
        print(f"Saved {len(formatter.flags)} flags to {out_path}")

    print(formatter.report())


if __name__ == "__main__":
    main()