# Cyber-sec: Web Server Security Assignment

**IIIT Allahabad · Department of Information Technology**
**Instructor:** Dr. Soumyadev Maity

An intentionally vulnerable Flask + SQLite lab built to demonstrate, exploit
and mitigate four categories of web server vulnerabilities: **SQL
injection**, **OS command injection**, **Cross-Site Scripting (XSS)**, and
**Cross-Site Request Forgery (CSRF)**. Each member implements one variant,
exploits it with evidence, and secures it with one mitigation.

> ⚠ **Run on localhost only.** This application is deliberately insecure and
> must never be deployed or exposed to the internet.

---

## Ownership declaration (Table 3)

| Member | Roll number | Category | Variant | Status |
|---|---|---|---|---|
| Aditi (M1) | IIT2024007 | SQL injection | Authentication bypass | ✅ Done |
| Srujan Gawande (M2) | IIT2024016 | XSS | Stored | ⏳ Pending |
| Disha Gupta (M3) | IIT2024039 | OS command injection | In-band | ⏳ Pending |
| Apurva (M4) | IIT2024034 | XSS | Reflected | ⏳ Pending |
| Pratishtha (M5) | IIT2024040 | CSRF | POST-based | ⏳ Pending |

*(Table complete. Status column updates as each member merges their work.)*

---

## Quick start

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py                   # open http://127.0.0.1:5000
```

The home page lists every module with a **ready** or **todo** badge.

---

## Project structure

```
Cyber-sec/
├── app.py                  # shared entrypoint — auto-registers every module, don't edit
├── db.py                   # per-module SQLite helper (db.get_conn("<module>"))
├── requirements.txt
├── templates/
│   ├── base.html           # shared theme — all pages extend this
│   ├── index.html          # home page (module cards)
│   └── <module>/           # each member's own templates
├── modules/
│   ├── sqli.py              ✅ M1 — SQL injection (auth bypass)
│   ├── xss_stored.py        ⏳ M2 — Stored XSS
│   ├── cmdi.py               ⏳ M3 — OS command injection (in-band)
│   ├── xss_reflected.py     ⏳ M4 — Reflected XSS
│   └── csrf.py               ⏳ M5 — CSRF (POST-based)
├── docs/
│   ├── M1_sqli.md           ✅ payload, root cause, fix, theory
│   ├── M2_xss_stored.md     ⏳
│   ├── M3_cmdi.md           ⏳
│   ├── M4_xss_reflected.md  ⏳
│   ├── M5_csrf.md           ⏳
│   └── screenshots/         # exploit + blocked screenshots go here
└── data/                    # per-module SQLite files (git-ignored, auto-created)
```

Every module exposes:
- `/<module>/` — overview + example payloads
- `/<module>/vuln/...` — the vulnerable version
- `/<module>/fixed/...` — the same feature with one mitigation applied

---

## ✅ Completed: M1 — SQL Injection (Authentication bypass)

- **Vulnerable route:** `/sqli/vuln/login` — login query built by string
  concatenation.
- **Exploit payloads:** `' OR '1'='1' --` and `admin' --` both bypass the
  password check and log in as `admin`.
- **Root cause:** user input is concatenated directly into the SQL string,
  so the database can't distinguish code from data.
- **Fixed route:** `/sqli/fixed/login` — parameterised query (`?`
  placeholders); the same payloads are rejected.
- **Theory (other mitigations):** input validation with allow-lists,
  least-privilege database accounts, safe/generic error messages.
- Full write-up: [`docs/M1_sqli.md`](docs/M1_sqli.md)

---

## ⏳ Remaining work (for the rest of the group)

Each of the four members below needs to, inside **their own** module file,
template folder and docs file only:

1. Replace the `TODO` stub in `modules/<your_module>.py` with:
   - A `setup()` that creates your own SQLite table (see `modules/sqli.py`
     for the pattern) if your variant needs stored data.
   - A `/vuln/...` route containing the actual flaw.
   - A `/fixed/...` route with one mitigation applied.
   - Set `READY = True` once both routes work (this updates your badge on
     the home page automatically).
2. Create templates under `templates/<your_module>/` that extend
   `templates/base.html` — this keeps the whole site's look consistent, you
   do not need to write any CSS.
3. Fill in your write-up in `docs/<your_file>.md` — copy
   `docs/M1_sqli.md`'s structure: (a) vulnerable code, (b) exploit payload,
   (c) root cause, (d) mitigation + screenshot, (e) theory on the other
   mitigations from the slides.
4. Take two screenshots (exploit working, exploit blocked) and save them in
   `docs/screenshots/`.
5. Fill in your name and roll number in the ownership table above.
6. Work on your own branch and open a pull request into `main`:
   ```bash
   git checkout -b m2-xss-stored    # use your own member/variant name
   # ... do your work ...
   git add .
   git commit -m "M2: stored XSS vulnerable + fixed"
   git push -u origin m2-xss-stored
   ```

**Reference theory (from the slides), per category:**
- SQL injection: parameterised queries, allow-list validation, least
  privilege, safe errors.
- Command injection: avoid the shell, parameterised execution (argument
  vector), allow-list validation, least privilege.
- XSS: context-aware output encoding, framework auto-escaping, a sanitiser
  for rich HTML, Content Security Policy, HttpOnly cookies, safe DOM sinks.
- CSRF: anti-CSRF (synchronizer) tokens, SameSite cookies,
  re-authentication for sensitive actions, avoiding state-changing GET
  requests.

---

## Deliverables checklist

- [ ] Source code in this public GitHub repository
- [ ] Group video (2-3 min per member, each narrating their own variant)
- [ ] Ownership declaration (table above) completed
- [ ] Every member ready to demo and answer viva questions on their own
      variant

## Team workflow

Work only in your own module, template folder and docs file, on your own
branch. Open a pull request into `main` when ready. `app.py` and
`templates/base.html` are shared — don't edit these unless coordinating with
the group, so everyone's branch stays conflict-free.
