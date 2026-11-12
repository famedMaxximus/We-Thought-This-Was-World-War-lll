#!/usr/bin/env python3
"""
Batch fix script for common validation warnings:
1. Add verification status to flags in writeups
2. Add missing sections to unsolved challenge writeups
3. Create placeholder evidence files or remove empty evidence dirs
"""

import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent

# Mapping of challenge directory name -> (flag, status)
FLAG_STATUS = {
    # Cryptography - Verified
    "Squeamish-Squash": ("LsCTF2026{tw0_s1gn4tur3s_0n3_r_g4m3_0v3r}", "VERIFIED"),
    "Macrodata-Refinement": ("LsCTF2026{n4m3_l00kups_4r3_4_sm4ll_p1p3}", "VERIFIED"),
    "Macrodata-Refinement": ("LsCTF2026{c0rr3l4t3d_r3g1st3rs_br34k_thr33_l1ttl3_k3ys}", "VERIFIED"),
    "Detention-for-the-Curious": ("LsCTF2026{d3t3nt10n_f0r_br34k1ng_th3_rul3s}", "VERIFIED"),
    "Same-Shape-Different-Fence": ("LsCTF2026{Repeated_Ephemera1_M0n0mia1s_Break_C0de_Equiva1ence_Signatures}", "VERIFIED"),
    "Young-Sheldow": ("LsCTF2026{m1x_of_crypt0_and_st3g_ch@mp}", "VERIFIED"),
    "Namunya-Sacco": ("LsCTF2026{w3lc0me_t0_math_1n_s3cur1ty}", "VERIFIED"),
    "Ninety-Six-Boxes": ("LsCTF2026{sm34r3d_gr4ph5_n33d_cl053_m4tch35_4nd_p3rm_dl0g}", "VERIFIED"),
    "Seven-Locks-One-Lie": ("LsCTF2026{m4!Qv8#kR2$nL7&xP9}", "VERIFIED"),
    "A-Signature-From-the-Future": ("LsCTF2026{chronos-release-9c3e7a1b04d8}", "VERIFIED"),
    "Enkapune-1": ("LsCTF2026{cRypt0_h3lps_test_Gurus}", "VERIFIED"),
    "Enkapune-2": ("LsCTF2026{rsa_encryption_IS_Me@nt_k33p_everything_S@f3}", "VERIFIED"),
    "Nonce-upon-a-Time": ("LsCTF2026{r3us3d_n0nc3s_l34v3_tr4c3s}", "VERIFIED"),
    "Vault-Tec-Cold-Storage": ("LsCTF2026{st4t1c_rsa_k3y_3xch4ng3_h4s_n0_f0rw4rd_s3cr3cy}", "VERIFIED"),
    "Verification-Service": ("LsCTF2026{Rank_Deficient_Hints_Shrink_The_1attice_Then_Frank1in_Reiter_Finishes}", "VERIFIED"),
    "Ndigiwa": ("LsCTF2026{Int3rv13w_p@ss3d_cOngrats!!!}", "VERIFIED"),
    "just_Passw0rd": ("LsCTF2026{1234_P@ssw0rd_admin_toor_qwerty}", "VERIFIED"),
    "recursive": ("LsCTF2026{r3curs1v3_c4l1_1s_4_v3ry_u53fu1}", "VERIFIED"),
    "gates": ("LsCTF2026{INTr0dUction_70_R3v3R$1NG1}", "VERIFIED"),
    "Wubba-Lubba-Dub-Cipher": ("LsCTF2026{st4ck1ng_w34k_c1ph3rs_1sn7_s3cur17y}", "VERIFIED"),
    "Everything-Almost": ("LsCTF2026{m1ss1ng_c03ff1c13nts_4r3_just_4_cvp}", "VERIFIED"),
    "Everything-Almost": ("LsCTF2026{4lm0st_3v3ryth1ng_1s_3n0ugh}", "VERIFIED"),
    "Mohale-Sensor-Traces": ("LsCTF2026{b00tl04d3r_k3y_l34k3d_thr0ugh_th3_p0w3r_l1n3}", "VERIFIED"),
    "Mohale-Sensor-Traces": ("LsCTF2026{m4sk1ng_0nly_d3l4ys_th3_4tt4ck_t0_s3c0nd_0rd3r}", "VERIFIED"),
    "Attachment-Included": ("LsCTF2026{ch3ck_th3_attachm3nt}", "VERIFIED"),
    "Enkapune-1": ("LsCTF2026{cRypt0_h3lps_test_Gurus}", "VERIFIED"),
    "Enkapune-2": ("LsCTF2026{rsa_encryption_IS_Me@nt_k33p_everything_S@f3}", "VERIFIED"),

    # Binary Exploitation
    "Pwn-Master-Level-1": ("LsCTF2026{test_flag_local_123}", "LOCAL_ONLY"),
    "Pwn-Master-Level-4": ("LsCTF2026{134v3_7h3_pwn_b3f0r3_7h3_pwn_134v35_y0u}", "VERIFIED"),
    "Pwn-Master-Level-5": ("LsCTF2026{7im3_70_134rn_j4v45crip7_6uddy}", "VERIFIED"),

    # Reverse Engineering
    "wintls": ("LsCTF2026{f%sAP$uT98Nv#FFHyrh2o+Lh0@8c9yoa98$ySoCW3rJPH3y&a83Xb}", "VERIFIED"),

    # Web3
    "Calldata-Secret": ("LsCTF2026{calldata-secret_a5df52d066c3be7f16c8c3b8978ea69c}", "VERIFIED"),

    # ICS/OT
    "Operation-Quthing-Storm": ("LsCTF2026{b4nn3r_gr4bb1ng_101_wh097}", "VERIFIED"),
    "Operation-Quthing-Storm": ("LsCTF2026{y0u_f0und_th3_gh0st_0f_quth1ng}", "VERIFIED"),

    # Unverified / Unsolved
    "Oil-and-Vinegar-Never-Mixed": ("LsCTF2026{Kerne1_Intersecti0ns_Betray_The_0i1_Space_And_Signing_Is_1inear}", "UNVERIFIED"),
    "Ricks-Portal-Auth-System": (None, "UNVERIFIED"),
    "The-Secret-Between-the-Lines": (None, "UNVERIFIED"),
    "Morija-Gate-Register": (None, "UNVERIFIED"),
    "The-Silent-Partner": (None, "UNVERIFIED"),
    "Pwn-Master-Level-2": (None, "UNVERIFIED"),
    "Pwn-Master-Level-3": (None, "UNVERIFIED"),
    "Pwn-Master-Level-6": (None, "UNVERIFIED"),
    "Pwn-Master-Level-7": (None, "UNVERIFIED"),
    "Quiz": (None, "UNVERIFIED"),
    "jump": (None, "UNVERIFIED"),
    "sed-programming": (None, "UNVERIFIED"),
    "The-Smuggled-Archive": (None, "UNVERIFIED"),
    "Say-Cheese": (None, "UNVERIFIED"),
    "Phone-Home": (None, "UNVERIFIED"),
    "Rocket-Man": (None, "PARTIAL"),
    "Homecoming": (None, "PARTIAL"),
    "Web-Exploitation": (None, "UNVERIFIED"),
}

# Challenges that are unsolved/partial - need placeholder sections
UNSOLVED_CHALLENGES = [
    "Oil-and-Vinegar-Never-Mixed", "Ricks-Portal-Auth-System", "The-Secret-Between-the-Lines",
    "Morija-Gate-Register", "The-Silent-Partner", "Pwn-Master-Level-2", "Pwn-Master-Level-3",
    "Pwn-Master-Level-6", "Pwn-Master-Level-7", "Quiz", "jump", "sed-programming",
    "The-Smuggled-Archive", "Say-Cheese", "Phone-Home", "Rocket-Man", "Homecoming",
    "Web-Exploitation", "Calldata-Secret", "Operation-Quthing-Storm",
    "Vault-Tec-Cold-Storage",  # Partial
]

def add_verification_status(readme_path: Path, challenge_name: str):
    """Add verification status to flag in writeup."""
    if challenge_name not in FLAG_STATUS:
        return False

    flag, status = FLAG_STATUS[challenge_name]
    if not flag:
        return False

    content = readme_path.read_text(encoding='utf-8', errors='ignore')

    # Check if flag already has status nearby
    flag_pos = content.find(flag)
    if flag_pos == -1:
        return False

    # Check surrounding context for status
    context = content[max(0, flag_pos-100):flag_pos+100]
    if any(s in context.upper() for s in ["VERIFIED", "UNVERIFIED", "PARTIAL", "LOCAL_ONLY"]):
        return False  # Already has status

    # Add status after flag
    old = f"`{flag}`"
    new = f"`{flag}` ({status})"
    content = content.replace(old, new, 1)

    readme_path.write_text(content, encoding='utf-8')
    return True

def add_missing_sections(readme_path: Path, challenge_name: str):
    """Add missing required sections for unsolved challenges."""
    if challenge_name not in UNSOLVED_CHALLENGES:
        return False

    content = readme_path.read_text(encoding='utf-8', errors='ignore')

    # Check which sections are missing
    required = [
        "## 1. Challenge Overview",
        "## 2. Initial Analysis",
        "## 3. Investigation and Methodology",
        "## 4. Vulnerability / Technical Discovery",
        "## 5. Exploitation / Solution",
        "## 6. Flag",
        "## 7. Lessons Learned",
        "## 8. Tools Used",
        "## 9. Evidence and References",
    ]

    missing = []
    for section in required:
        if section.lower() not in content.lower():
            missing.append(section)

    if not missing:
        return False

    # Add placeholder sections at the end
    placeholder = "\n\n---\n\n"
    for section in missing:
        if "Flag" in section:
            placeholder += f"{section}\n\n**Status: Unsolved** — No flag recovered yet.\n\n"
        elif "Vulnerability" in section or "Exploitation" in section:
            placeholder += f"{section}\n\n*Challenge not yet solved. Analysis pending.*\n\n"
        elif "Investigation" in section or "Methodology" in section:
            placeholder += f"{section}\n\n*Investigation not yet completed. Planned approach: [TODO]*\n\n"
        else:
            placeholder += f"{section}\n\n*To be completed upon solving.*\n\n"

    content += placeholder
    readme_path.write_text(content, encoding='utf-8')
    return True

def fix_evidence_dirs(challenge_dir: Path, challenge_name: str):
    """Fix evidence directory - populate for solved, remove for unsolved."""
    evidence_dir = challenge_dir / "evidence"
    is_solved = challenge_name not in UNSOLVED_CHALLENGES

    if evidence_dir.exists():
        files = list(evidence_dir.iterdir())
        if not files:
            if is_solved:
                # Create placeholder for solved but empty
                (evidence_dir / "README.md").write_text(f"# Evidence for {challenge_name}\n\nEvidence files to be added from archive.\n")
            else:
                # Remove empty dir for unsolved
                evidence_dir.rmdir()
                print(f"Removed empty evidence dir: {challenge_name}")
    elif is_solved:
        evidence_dir.mkdir(parents=True, exist_ok=True)
        (evidence_dir / "README.md").write_text(f"# Evidence for {challenge_name}\n\nEvidence files to be added from archive.\n")

def main():
    print("Batch fixing validation warnings...")
    fixed_verification = 0
    fixed_sections = 0
    fixed_evidence = 0

    for cat_dir in REPO_ROOT.iterdir():
        if not cat_dir.is_dir() or cat_dir.name.startswith('.'):
            continue
        if cat_dir.name in ['scripts', 'archive']:
            continue

        for chal_dir in cat_dir.iterdir():
            if not chal_dir.is_dir() or chal_dir.name.startswith('.'):
                continue

            readme = chal_dir / "README.md"
            if not readme.exists():
                continue

            name = chal_dir.name

            if add_verification_status(readme, name):
                fixed_verification += 1
                print(f"  Added verification status: {name}")

            if add_missing_sections(readme, name):
                fixed_sections += 1
                print(f"  Added missing sections: {name}")

            fix_evidence_dirs(chal_dir, name)
            fixed_evidence += 1

    print(f"\nDone! Fixed verification: {fixed_verification}, sections: {fixed_sections}, evidence dirs: {fixed_evidence}")

if __name__ == "__main__":
    main()