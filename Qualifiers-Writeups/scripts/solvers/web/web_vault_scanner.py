#!/usr/bin/env python3
"""
Web Vault Scanner - 10-module vault scanner
LsCTF2026 Web Exploitation

Auto-discovers and attempts exploits on all 10 web vaults.
"""
import asyncio
import aiohttp
import re
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class Vault:
    name: str
    url: str
    port: int
    difficulty: str
    description: str

VAULTS = [
    Vault("token-forge", "http://{ip}:50001", 50001, "Easy", "JWT token forgery"),
    Vault("cookie-monster", "http://{ip}:50002", 50002, "Easy", "Cookie manipulation"),
    Vault("note-peek", "http://{ip}:50003", 50003, "Easy", "IDOR on notes"),
    Vault("injected", "http://{ip}:50004", 50004, "Medium", "SQL injection"),
    Vault("nosql-noise", "http://{ip}:50005", 50005, "Medium", "NoSQL injection"),
    Vault("template-tantrum", "http://{ip}:50006", 50006, "Medium", "SSTI"),
    Vault("proto-pollute", "http://{ip}:50007", 50007, "Medium", "Prototype pollution"),
    Vault("preview-portal", "http://{ip}:50008", 50008, "Hard", "SSRF with localhost bypass"),
    Vault("path-walker", "http://{ip}:50009", 50009, "Hard", "Path traversal"),
    Vault("token-twister", "http://{ip}:50010", 50010, "Hard", "JWT algorithm confusion"),
]

class VaultScanner:
    def __init__(self, base_ip: str):
        self.base_ip = base_ip
        self.session: Optional[aiohttp.ClientSession] = None
        self.results = {}

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def check_vault(self, vault: Vault) -> Dict:
        """Basic connectivity check."""
        url = vault.url.format(ip=self.base_ip)
        try:
            async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
                return {
                    "vault": vault.name,
                    "url": url,
                    "status": resp.status,
                    "accessible": True
                }
        except Exception as e:
            return {
                "vault": vault.name,
                "url": url,
                "status": 0,
                "accessible": False,
                "error": str(e)
            }

    async def scan_all(self) -> List[Dict]:
        """Scan all vaults for accessibility."""
        tasks = [self.check_vault(v) for v in VAULTS]
        return await asyncio.gather(*tasks)

    # Exploit modules (implement per vault)
    async def exploit_token_forge(self, url: str) -> Optional[str]:
        """JWT algorithm confusion / none algorithm."""
        # 1. Register/get token
        # 2. Decode JWT, change alg to "none", remove signature
        # 3. Set role=admin, submit
        pass

    async def exploit_cookie_monster(self, url: str) -> Optional[str]:
        """Cookie manipulation - premium flag."""
        # 1. Register free account
        # 2. Analyze cookie structure (JWT? signed? encrypted?)
        # 3. Forge premium cookie
        pass

    async def exploit_note_peek(self, url: str) -> Optional[str]:
        """IDOR on notes."""
        # 1. Register two accounts
        # 2. Create note with account A
        # 3. Access note ID with account B (IDOR)
        pass

    async def exploit_injected(self, url: str) -> Optional[str]:
        """SQL injection on login."""
        # 1. Find injectable parameter (username/password)
        # 2. Extract admin credentials or flag via UNION
        pass

    async def exploit_nosql_noise(self, url: str) -> Optional[str]:
        """NoSQL injection."""
        # 1. Find injectable field (login, search, etc.)
        # 2. Use {$ne: null}, {$gt: ""}, etc.
        pass

    async def exploit_template_tantrum(self, url: str) -> Optional[str]:
        """SSTI in card preview."""
        # 1. Test {{7*7}}, {{config}}, {{self.__class__.__mro__}}
        # 2. RCE via {{get_flashed_messages.__globals__.__builtins__.open}}
        pass

    async def exploit_proto_pollute(self, url: str) -> Optional[str]:
        """Prototype pollution."""
        # 1. Find JSON input (preferences, settings)
        # 2. Send {"__proto__": {"isAdmin": true}}
        # 3. Access beta features
        pass

    async def exploit_preview_portal(self, url: str) -> Optional[str]:
        """SSRF with localhost bypass."""
        # 1. Test various localhost representations:
        #    - http://127.0.0.1
        #    - http://0.0.0.0
        #    - http://localhost
        #    - http://[::1]
        #    - http://2130706433 (decimal)
        #    - http://0x7f000001 (hex)
        #    - http://127.1
        #    - http://127.0.0.1.nip.io
        pass

    async def exploit_path_walker(self, url: str) -> Optional[str]:
        """Path traversal on markdown files."""
        # 1. Test ../../etc/passwd, ../../proc/self/environ
        # 2. Bypass filters (..\, ..%2f, ..%00, double encoding)
        pass

    async def exploit_token_twister(self, url: str) -> Optional[str]:
        """JWT algorithm confusion (RS256 -> HS256)."""
        # 1. Get public key (JWKS endpoint or cert)
        # 2. Sign HS256 token with public key as secret
        # 3. Set role=admin
        pass

async def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="52.91.22.226", help="Lab IP")
    args = parser.parse_args()

    async with VaultScanner(args.ip) as scanner:
        results = await scanner.scan_all()
        for r in results:
            status = "✅" if r["accessible"] else "❌"
            print(f"{status} {r['vault']:20s} {r['url']} -> {r['status']}")

if __name__ == "__main__":
    asyncio.run(main())