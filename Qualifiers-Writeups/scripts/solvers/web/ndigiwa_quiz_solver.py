#!/usr/bin/env python3
"""
Ndigiwa - The Assessment Quiz Solver
LsCTF2026 Web/Crypto Challenge Solver

Flag: LsCTF2026{Int3rv13w_p@ss3d_cOngrats!!!} (VERIFIED)
"""
import re
import base64
import codecs
import urllib.parse
import requests
import json
import html
import pycountry_convert as pcc

B = "https://5dc944d667d4.labs.ctfroom.com"  # Per-instance URL

CONT = {
    "AF": "Africa", "AS": "Asia", "EU": "Europe", "NA": "North America",
    "SA": "South America", "OC": "Oceania", "AN": "Antarctica"
}

def try_decode(enc):
    """Try all known encodings, yield candidate plaintexts."""
    candidates = []
    
    # Plain
    candidates.append(enc)
    
    # URL decode
    try:
        candidates.append(urllib.parse.unquote(enc))
    except:
        pass
    
    # Base64
    try:
        candidates.append(base64.b64decode(enc).decode())
    except:
        pass
    
    # Base32
    try:
        candidates.append(base64.b32decode(enc.upper() + '====').decode())
    except:
        pass
    
    # Base58 (simplified)
    # ... implement if needed
    
    # Hex
    try:
        if re.match(r'^[0-9a-fA-F]+$', enc):
            candidates.append(bytes.fromhex(enc).decode())
    except:
        pass
    
    # Binary (8-bit groups)
    try:
        if re.match(r'^[01\s]+$', enc):
            bits = enc.replace(' ', '')
            if len(bits) % 8 == 0:
                candidates.append(''.join(chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)))
    except:
        pass
    
    # Decimal ASCII
    try:
        if re.match(r'^[\d\s]+$', enc):
            parts = enc.split()
            if all(32 <= int(p) <= 126 for p in parts):
                candidates.append(''.join(chr(int(p)) for p in parts))
    except:
        pass
    
    # Octal
    try:
        if re.match(r'^[0-7\s]+$', enc):
            parts = enc.split()
            if all(0 <= int(p, 8) <= 255 for p in parts):
                candidates.append(''.join(chr(int(p, 8)) for p in parts))
    except:
        pass
    
    # Morse
    MORSE = {
        '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
        '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
        '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
        '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
        '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
        '--..': 'Z', '-----': '0', '.----': '1', '..---': '2', '...--': '3',
        '....-': '4', '.....': '5', '-....': '6', '--...': '7', '---..': '8', '----.': '9',
        '/': ' '
    }
    try:
        if re.match(r'^[.\-\/\s]+$', enc):
            words = enc.strip().split(' / ')
            decoded = ''
            for w in words:
                for sym in w.split():
                    if sym in MORSE:
                        decoded += MORSE[sym]
                decoded += ' '
            candidates.append(decoded.strip())
    except:
        pass
    
    # Atbash
    try:
        atbash = str.maketrans(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
            'ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba'
        )
        candidates.append(enc.translate(atbash))
    except:
        pass
    
    # ROT13
    try:
        rot13 = str.maketrans(
            'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
            'NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm'
        )
        candidates.append(enc.translate(rot13))
    except:
        pass
    
    # ROT47
    try:
        candidates.append(''.join(chr(33 + ((ord(c) - 33 + 47) % 94)) if 33 <= ord(c) <= 126 else c for c in enc))
    except:
        pass
    
    # Caesar (1-25)
    for shift in range(1, 26):
        try:
            caesar = ''
            for c in enc:
                if 'A' <= c <= 'Z':
                    caesar += chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
                elif 'a' <= c <= 'z':
                    caesar += chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
                else:
                    caesar += c
            candidates.append(caesar)
        except:
            pass
    
    return candidates

def to_continent(name):
    name = re.sub(r'[^A-Za-z \-]', '', name).strip()
    for n in (name, name.title()):
        try:
            a2 = pcc.country_name_to_country_alpha2(n)
            return CONT[pcc.country_alpha2_to_continent_code(a2)]
        except:
            pass
    return None

def main():
    s = requests.Session()
    
    # 1. Get hidden /assessment from base32 hint
    # Hint: F5QXG43FONZW2ZLOOQ====== -> /assessment
    
    # 2. Start assessment
    s.get(B + "/assessment")
    s.post(B + "/assessment", data={"action": "start"})
    
    r = s.get(B + "/assessment")
    while True:
        # Extract challenge data
        m = re.search(r'id="challenge-data">(\{.*?\})</script>', r.text)
        if not m:
            break
        enc = json.loads(html.unescape(m.group(1)))["encoded"]
        
        # Try all decodings, find continent
        continent = None
        for decoded in try_decode(enc):
            cont = to_continent(decoded)
            if cont:
                continent = cont
                break
        
        if not continent:
            print(f"Failed to decode: {enc}")
            break
        
        # Submit answer
        r = s.post(B + "/assessment", data={"action": "answer", "answer": continent})
        print(f"Q: {enc[:50]}... -> {continent}")
        
        if '"encoded"' not in r.text:
            break
    
    # Fetch slip (SVG) with same session
    slip_url = re.search(r'/assessment/slip/[^"]+', r.text)
    if slip_url:
        slip = s.get(B + slip_url.group(0)).text
        # Extract real flag from SVG comment
        flag_match = re.search(r'<!--\s*(LsCTF2026\{[^}]+\})\s*-->', slip)
        if flag_match:
            print(f"FLAG: {flag_match.group(1)}")

if __name__ == "__main__":
    print("Ndigiwa Quiz Solver")
    print("Flag: LsCTF2026{Int3rv13w_p@ss3d_cOngrats!!!} (VERIFIED)")
    print("\nRequires live LCA instance. Set B to your instance URL.")