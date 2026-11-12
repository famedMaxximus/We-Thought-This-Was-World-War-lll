#!/usr/bin/env python3
"""
Lesotho CTF Writeups Repository Validation Script

Validates the repository structure, writeup completeness, flag consistency,
and cross-reference integrity.
"""

import os
import re
import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field

REPO_ROOT = Path(__file__).parent.parent

CATEGORIES = [
    "Cryptography",
    "Binary-Exploitation",
    "Reverse-Engineering",
    "Digital-Forensics",
    "Web-Exploitation",
    "Web3",
    "ICS-OT-Security",
    "Steganography",
    "OSINT",
    "Network-Security",
    "Hardware-Security",
    "Programming",
    "Miscellaneous",
]

FLAG_PATTERN = re.compile(r'LsCTF2026\{[^}]+\}')
FLAG_STATUS_PATTERN = re.compile(r'(VERIFIED|UNVERIFIED|PARTIAL|LOCAL_ONLY)')

@dataclass
class ValidationResult:
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    info: List[str] = field(default_factory=list)

    def add_error(self, msg: str):
        self.errors.append(msg)

    def add_warning(self, msg: str):
        self.warnings.append(msg)

    def add_info(self, msg: str):
        self.info.append(msg)

    def has_errors(self) -> bool:
        return len(self.errors) > 0

    def print_summary(self):
        print(f"\n{'='*60}")
        print(f"VALIDATION SUMMARY")
        print(f"{'='*60}")
        print(f"Errors:   {len(self.errors)}")
        print(f"Warnings: {len(self.warnings)}")
        print(f"Info:     {len(self.info)}")
        print(f"{'='*60}")

        if self.errors:
            print("\n❌ ERRORS:")
            for e in self.errors:
                print(f"  - {e}")

        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for w in self.warnings:
                print(f"  - {w}")

        if self.info:
            print("\nℹ️  INFO:")
            for i in self.info:
                print(f"  - {i}")


def validate_structure(result: ValidationResult):
    """Validate the repository directory structure."""
    required_root = ["README.md", "FLAG_INDEX.md", "CATEGORIES.md", "CONTRIBUTING.md", "LICENSE", ".gitignore"]
    for f in required_root:
        if not (REPO_ROOT / f).exists():
            result.add_error(f"Missing required root file: {f}")

    for cat in CATEGORIES:
        cat_path = REPO_ROOT / cat
        if cat_path.exists() and cat_path.is_dir():
            result.add_info(f"Category directory exists: {cat}")
        else:
            result.add_warning(f"Category directory missing: {cat}")


def find_challenges() -> Dict[str, List[Path]]:
    """Find all challenge directories."""
    challenges = {}
    for cat in CATEGORIES:
        cat_path = REPO_ROOT / cat
        if cat_path.exists() and cat_path.is_dir():
            for item in cat_path.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    challenges.setdefault(cat, []).append(item)
    return challenges


def validate_challenge_writeups(result: ValidationResult, challenges: Dict[str, List[Path]]):
    """Validate each challenge has a proper writeup."""
    required_sections = [
        "Challenge Overview",
        "Initial Analysis",
        "Investigation and Methodology",
        "Vulnerability",
        "Exploitation",
        "Flag",
        "Lessons Learned",
        "Tools Used",
        "Evidence and References",
    ]

    for cat, chal_dirs in challenges.items():
        for chal_dir in chal_dirs:
            readme = chal_dir / "README.md"
            if not readme.exists():
                result.add_error(f"Missing README.md: {chal_dir.relative_to(REPO_ROOT)}")
                continue

            content = readme.read_text(encoding='utf-8', errors='ignore')

            # Check for required sections
            for section in required_sections:
                if section.lower() not in content.lower():
                    result.add_warning(f"Missing section '{section}' in {chal_dir.name}")

            # Check for flag
            flag_match = FLAG_PATTERN.search(content)
            if not flag_match:
                result.add_warning(f"No flag pattern found in {chal_dir.name}")
            else:
                flag = flag_match.group(0)
                # Check verification status near flag
                flag_pos = content.find(flag)
                context = content[max(0, flag_pos-200):flag_pos+200]
                if "UNVERIFIED" in context.upper():
                    result.add_info(f"Flag marked UNVERIFIED: {chal_dir.name} - {flag}")
                elif "VERIFIED" in context.upper():
                    result.add_info(f"Flag marked VERIFIED: {chal_dir.name} - {flag}")
                elif "PARTIAL" in context.upper():
                    result.add_info(f"Flag marked PARTIAL: {chal_dir.name} - {flag}")
                elif "LOCAL_ONLY" in context.upper():
                    result.add_info(f"Flag marked LOCAL_ONLY: {chal_dir.name} - {flag}")
                else:
                    result.add_warning(f"Flag found but no verification status: {chal_dir.name} - {flag}")

            # Check evidence directory
            evidence_dir = chal_dir / "evidence"
            if not evidence_dir.exists():
                result.add_warning(f"Missing evidence/ directory: {chal_dir.name}")
            elif not any(evidence_dir.iterdir()):
                result.add_warning(f"Empty evidence/ directory: {chal_dir.name}")


def validate_flag_index(result: ValidationResult):
    """Validate FLAG_INDEX.md consistency."""
    flag_index = REPO_ROOT / "FLAG_INDEX.md"
    if not flag_index.exists():
        result.add_error("FLAG_INDEX.md not found")
        return

    content = flag_index.read_text(encoding='utf-8', errors='ignore')

    # Extract all flags from index
    index_flags = FLAG_PATTERN.findall(content)
    result.add_info(f"FLAG_INDEX.md contains {len(index_flags)} flags")

    # Check for duplicates
    seen = set()
    for flag in index_flags:
        if flag in seen:
            result.add_error(f"Duplicate flag in FLAG_INDEX.md: {flag}")
        seen.add(flag)

    # Verify each flag in index has a corresponding writeup
    challenges = find_challenges()
    writeup_flags = set()
    for cat, chal_dirs in challenges.items():
        for chal_dir in chal_dirs:
            readme = chal_dir / "README.md"
            if readme.exists():
                content = readme.read_text(encoding='utf-8', errors='ignore')
                writeup_flags.update(FLAG_PATTERN.findall(content))

    for flag in index_flags:
        if flag not in writeup_flags:
            result.add_warning(f"Flag in FLAG_INDEX.md not found in any writeup: {flag}")

    for flag in writeup_flags:
        if flag not in index_flags:
            result.add_warning(f"Flag in writeup not in FLAG_INDEX.md: {flag}")


def validate_categories_index(result: ValidationResult):
    """Validate CATEGORIES.md consistency."""
    cat_index = REPO_ROOT / "CATEGORIES.md"
    if not cat_index.exists():
        result.add_error("CATEGORIES.md not found")
        return

    content = cat_index.read_text(encoding='utf-8', errors='ignore')

    challenges = find_challenges()
    for cat, chal_dirs in challenges.items():
        for chal_dir in chal_dirs:
            if chal_dir.name not in content:
                result.add_warning(f"Challenge {chal_dir.name} not listed in CATEGORIES.md")


def validate_evidence_files(result: ValidationResult, challenges: Dict[str, List[Path]]):
    """Validate evidence files are reasonable."""
    for cat, chal_dirs in challenges.items():
        for chal_dir in chal_dirs:
            evidence_dir = chal_dir / "evidence"
            if evidence_dir.exists():
                for f in evidence_dir.iterdir():
                    if f.is_file():
                        size = f.stat().st_size
                        if size == 0:
                            result.add_warning(f"Empty evidence file: {f.relative_to(REPO_ROOT)}")
                        elif size > 50 * 1024 * 1024:  # 50MB
                            result.add_warning(f"Large evidence file ({size/1024/1024:.1f}MB): {f.relative_to(REPO_ROOT)}")


def validate_solver_scripts(result: ValidationResult, challenges: Dict[str, List[Path]]):
    """Check for solver scripts."""
    for cat, chal_dirs in challenges.items():
        for chal_dir in chal_dirs:
            solvers = list(chal_dir.glob("solve*.py")) + list(chal_dir.glob("exploit*.py"))
            if solvers:
                result.add_info(f"Solver script(s) found: {chal_dir.name} - {[s.name for s in solvers]}")


def main():
    print("Lesotho CTF Writeups - Repository Validation")
    print("=" * 60)

    result = ValidationResult()

    validate_structure(result)
    challenges = find_challenges()
    validate_challenge_writeups(result, challenges)
    validate_flag_index(result)
    validate_categories_index(result)
    validate_evidence_files(result, challenges)
    validate_solver_scripts(result, challenges)

    result.print_summary()

    # Statistics
    total_challenges = sum(len(v) for v in challenges.values())
    result.add_info(f"Total challenges found: {total_challenges}")
    for cat, chal_dirs in challenges.items():
        if chal_dirs:
            result.add_info(f"  {cat}: {len(chal_dirs)} challenges")

    if result.has_errors():
        print("\n❌ VALIDATION FAILED")
        return 1
    else:
        print("\n✅ VALIDATION PASSED (warnings are non-blocking)")
        return 0


if __name__ == "__main__":
    sys.exit(main())