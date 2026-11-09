# OSINT Recon (Passive) — Building the Dossier

> **Passive only during the recon phase:** collect from public sources, do NOT contact the target
> (no calls, emails, logins, or active scans) until the live phase opens. Only the organizer-named
> target. Cite a source for every flag.

## 1. Goal

Turn a company name into a dossier rich enough to (a) bank OSINT flags and (b) fuel believable
pretexts. You want to sound like you already belong.

## 2. Source checklist (work top to bottom)

**Company surface**
- [ ] Official website — About, Team, Careers, Contact, Locations, Press, Blog, footer (vendors,
      certifications, office hours, phone numbers, email format).
- [ ] **Job postings** (their site, LinkedIn, job boards) — *gold mine* for tech stack: named
      software, OS, cloud, security tools, ticketing systems, "experience with X required".
- [ ] Press releases / news — partnerships, new offices, recent events, new hires, incidents.
- [ ] Annual reports / filings (if public) — org structure, leadership, suppliers.

**People**
- [ ] LinkedIn — org chart, names, titles, who reports to whom, tenure (new hires = softer targets),
      "we use [tool]" posts. Note reception/front-desk, IT, HR, facilities, procurement.
- [ ] Other socials (Facebook, X, Instagram, TikTok) — informal info, photos of badges/desks/
      screens, office layout, events, dress code, internal lingo.
- [ ] Conference talks / webinars / podcasts by staff — they reveal tooling and process on stage.

**Technical footprint (passive)**
- [ ] Email format: `first.last@`, `flast@`, etc. (hunter.io patterns, from published addresses).
- [ ] Domains/subdomains: `crt.sh` (cert transparency), DNS `dig`, Wayback Machine for old pages.
- [ ] Tech fingerprints: BuiltWith / Wappalyzer / `whatweb` on the public site (CMS, analytics,
      chat widget, email security banners).
- [ ] Metadata in public documents (PDF/DOCX on their site): authors, software versions, usernames,
      internal paths — `exiftool`.
- [ ] GitHub / GitLab org & employees' repos: tech stack, internal tooling, sometimes secrets.
- [ ] Google dorks:
      `site:target.com filetype:pdf` · `"@target.com"` · `site:linkedin.com "target"`
      `intitle:"index of" target` · `"target" "helpdesk" OR "password reset"`

**Physical / operational**
- [ ] Google Maps / Street View — building, entrances, signage, nearby businesses, parking.
- [ ] Office hours, holidays, event calendar.
- [ ] Vendors/contractors: cleaning, security, catering, IT MSP, shredding, couriers (great pretext
      personas — "I'm from [the actual MSP] about your ticket").

## 3. Flag ideas (what judges typically score)

Facts to hunt for (each is a likely flag):
- Operating system(s) and version · browser · antivirus/EDR · email provider (O365/Google)
- VPN / remote-access tool · ERP/CRM/HR system names · ticketing/helpdesk system
- Wireless network name(s) · whether there's guest wifi
- Physical: cafeteria? badge type? smoking area? who does the cleaning? shredding vendor?
- Process: how do staff reset passwords? is there a helpdesk number? do they have a newsletter?
- People: name of IT manager / reception / a specific team; email naming convention; phone tree.

Keep a running **flag sheet**: `flag | value | source(url) | confidence`.

## 4. Dossier template

```
=== TARGET DOSSIER: <Org> ===
Industry / size / locations:
Office hours / timezone / key dates:
Email format:                      Phone main / tree:
Website tech (Wappalyzer):
Tech stack from job ads:           (OS, cloud, security tools, ERP/CRM, ticketing)
Known vendors/contractors:         (MSP, cleaning, security, catering, courier)
Internal lingo / brands:
--- People ---
Name | Title | Dept | Notes (tenure, socials, quotes)
...
--- Pretext hooks ---  (facts that enable a believable call)
- e.g. "They just opened a Maseru branch" -> 'new-office IT setup' pretext
- e.g. "Job ad lists [ticketing tool]" -> 'helpdesk following up on your ticket' pretext
--- Flag sheet ---
flag | value | source | confidence
```

## 5. Tooling (passive)

```bash
# username / people
sherlock <handle>                 # accounts across platforms (whatsmyname.app as backup)
# domains / certs / history
whois target.com ; dig +short target.com ANY
curl -s 'https://crt.sh/?q=%25.target.com&output=json' | jq -r '.[].name_value' | sort -u
curl -s 'http://web.archive.org/cdx/search/cdx?url=target.com*&fl=original&collapse=urlkey' | sort -u
# tech + metadata
whatweb https://target.com        # (passive banner read)
exiftool downloaded_public_doc.pdf
# email patterns: inspect published addresses; hunter.io / phonebook.cz for format
```
(Tools like theHarvester/recon-ng aggregate the above — fine for passive recon if the rules allow
them and you only query public data about the authorized target.)

## 6. Discipline

- **Log the source of every fact** — unsourced flags may be rejected.
- Stay strictly passive until the live phase; a single pre-call can disqualify you.
- Don't collect sensitive personal data on individuals beyond what the flags require.
- Organize the dossier so the Navigator can find any fact in <5 seconds during a live call.
