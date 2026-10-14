# CLAUDE.md

Instructions for Claude Code in this repository.

## Project

**Renter Trust Network**: a take-home feature for 1Now by Rao Rizwan.
1Now gives car rental companies their own direct-booking site. On Turo, bad renters get banned; on a direct
site nobody warns the next company. This feature lets companies report bad customers and checks every new
booking against those reports with an explainable 0–100 risk score.

Full spec: `docs/TECHNICAL.md` (source of truth). Install guide: `docs/SETUP.md`. Decisions log: `docs/JOURNEY.md`.

## Commands

```bash
# Backend (from backend/)
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn app.main:app --reload      # http://localhost:8000
.venv/bin/pytest                             # 19 tests

# Frontend (from frontend/)
npm install
npm run build                                # served by the backend
npm run dev                                  # http://localhost:5173, proxies /api to :8000
```

Reset demo data: stop the server and delete `backend/data/trust.db`.

## Structure

```
backend/app/     config, database, schema.sql, identity, risk, repository, services, access, models, seed, main
backend/app/routes/   hosts, bookings, reports
backend/tests/   test_identity, test_risk, test_api
frontend/src/    api/, components/{bookings,layout,reports,ui}/, constants/, hooks/, pages/, styles/, utils/
docs/            SETUP.md, TECHNICAL.md, JOURNEY.md, media/
```

## Rules that must not break

- **Privacy:** the shared `network_reports` table holds only HMAC fingerprints of licence, email and phone,
  plus incident type, severity and date. Raw customer details go only to the company that owns the booking.
  Never expose who reported, private notes or booking ids to another company.
- **Matching:** normalise before hashing (Gmail dots and `+tags`, `+92` phone default, `PROVINCE:NUMBER` licence).
- **Scoring:** every point needs a readable reason. Licence match +60; email/phone-only match +35 (verify, don't decline).
  Thresholds: 0–29 low, 30–59 medium, 60+ high. Points live as named constants in `risk.py`.
- **Fairness:** reports expire after 24 months and can be withdrawn by the reporter.
- **Access:** every route that takes `host_id` checks ownership and returns 403 otherwise.
- **Risk is computed on read**, never stored.

## Conventions

- Code uses 1Now's terms (`host`, `renter`); the UI says **company** and **customer**. Never show "host" or "renter" in the UI.
- Python: small modules, no docstrings, no leading-underscore names, no `__init__.py`. Comments only explain *why*.
  SQL lives in `repository.py`; shared writes (`create_booking`, `create_report`) are reused by routes and seed data.
- React: one component per file, grouped by feature. Shared constants in `constants/`, data loading through `useFetch`.
- Styling: tokens in `styles/tokens.css` (Geist, navy `#14253A`, orange `#FE7743`, cream `#FAF8F4`). Use the custom
  `Dropdown` (never a native `<select>`), capsules for status-like values, no emoji or decorative filler in the UI.
- Dates in the frontend use local time (`utils/format.js`), never `toISOString()`.
- Verify UI changes with screenshots at 1440px and 390px wide.

## Demo data

Signed in as **Rao Rizwan**, owner of **Rao Rent-a-Car** (Lahore). Other companies: Karachi Drive, Islamabad Wheels.
Expected scores at Rao Rent-a-Car: Bilal 95 · Zain 55 · Hamza 40 · Usman 40 · Fatima 0 · Hira 0.
Demo flow: Bilal is high risk → Karachi Drive reports Ayesha → her new booking at Rao Rent-a-Car scores 70 → withdraw → 0.

## Working style

- Propose a short plan and wait for approval before larger changes; the user makes scope and design calls.
- Keep the MVP small. Out of scope: auth, real ID checks, 1Now integration, appeals, abuse protection, ML, notifications.
- Run the tests and the demo flow before calling anything done. Report failures honestly.
- When behaviour changes, update `docs/TECHNICAL.md`, `README.md` and this file together; update `docs/SETUP.md` when commands or requirements change.
