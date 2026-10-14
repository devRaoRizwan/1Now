# Technical details

**Renter Trust Network** · Rao Rizwan · take-home assignment for 1Now

Architecture, risk engine, privacy design, data model, API, frontend, tests and trade-offs.
For the plain-English overview see the [README](../README.md); for decisions see [JOURNEY.md](JOURNEY.md).

---

## 1. Problem

1Now's pitch is *"take direct bookings and keep the 10–30% Turo would take."* But a direct booking loses Turo's
trust layer: a renter banned on Turo can still book on any host's own site, and hosts share no memory of bad renters.

**Goal:** a shared, privacy-preserving warning network plus explainable risk checks on every incoming booking.

| Code term | UI term | Meaning |
|---|---|---|
| host | company | A rental business on 1Now |
| renter | customer | The person booking a car |
| network report | report | An incident one company shares with all companies |

## 2. Architecture

```
frontend (React + Vite)  ──fetch /api──▶  backend (FastAPI)  ──▶  SQLite
                                              │
     routes/  →  access (ownership)  →  services (assemble views)  →  repository (SQL)
                                              │
                                    risk.assess()   identity.identity_hashes()
```

```
 Customer books at company B
             │
             ▼
 bookings (private to B) ── normalise + HMAC ──▶ email_hash · phone_hash · license_hash
                                                          │ lookup, last 24 months
 Company A reported this customer earlier ──▶ network_reports (shared, fingerprints only)
                                                          ▼
                              risk.assess(booking, vehicle, matches) → score, level, reasons
                                                          ▼
                                      Company B sees the score and decides
```

Risk is **computed on read**, never stored, so a new or withdrawn report changes every company's view immediately.

## 3. Risk engine (`backend/app/risk.py`)

Pure functions, points as named constants, unit-tested in isolation.

### Network signals (reports from the last 24 months)

| Code | Signal | Points |
|---|---|---:|
| `network_license_match` | Licence fingerprint matches a report | +60 |
| `network_contact_match` | Only email or phone matches (may be shared, so verify) | +35 |
| `network_multiple_hosts` | Reported by more than one company | +10 per extra, max +20 |
| `network_severe_incident` | Includes theft, fake ID or chargeback | +10 |

### Booking signals

| Code | Signal | Points |
|---|---|---:|
| `license_expired` | Licence expired before pick-up | +50 |
| `license_expires_during_trip` | Licence expires before return | +30 |
| `very_young_driver` | Under 21 at pick-up | +25 |
| `young_driver` | 21–24 at pick-up | +10 |
| `last_minute_high_value` | Booked ≤ 1 day ahead, car worth ≥ Rs 1 crore | +15 |
| `long_trip` | Longer than 21 days | +10 |
| `disposable_email` | Throwaway inbox domain | +15 |

| Score | Level | Recommendation |
|---|---|---|
| 0–29 | low | Approve |
| 30–59 | medium | Request more info (ID selfie, proof of insurance) |
| 60–100 | high | Decline, or verify ID in person |

Each reason is returned as `{code, label, detail, points, source}`. Rules were chosen over ML because there is no
labelled outcome data yet and a company must be able to explain a decline.

## 4. Identity and privacy (`backend/app/identity.py`)

| Field | Normalisation | Equal examples |
|---|---|---|
| Email | lowercase, drop `+tag`, drop Gmail dots, `googlemail.com` → `gmail.com` | `Bilal.Ahmed+lahore@Gmail.com` = `bilalahmed@gmail.com` |
| Phone | digits only, international, `+92` default | `0300-1234567` = `+92 300 1234567` = `0092 300 1234567` |
| Licence | `PROVINCE:ALPHANUMERIC` | `sd` + `khi-19-88123` = `SD:KHI1988123` |

Fingerprint: `HMAC-SHA256(TRUST_NETWORK_SECRET, "<kind>:<value>")`. Keyed, so the shared table can't be reversed with
a list of known numbers; prefixed by kind, so an email can never collide with a phone.

| Visible to other companies? | |
|---|---|
| Name, email, phone, licence | No. Only the owning company |
| Which company reported, private note, booking id | No |
| Incident type, severity, date, which identifiers matched | Yes |

Enforced in `repository.NETWORK_MATCHES` (selects no notes or ids) and `services.public_match` (hides the reporter).
Reports expire after 24 months (`config.REPORT_RETENTION_DAYS`) and can be withdrawn; duplicates return `409`.

## 5. Backend layout

| Module | Responsibility |
|---|---|
| `config.py` | Paths, secret, retention window |
| `schema.sql` / `database.py` | Tables, indexes, connections |
| `repository.py` | All SQL; shared `create_booking` and `create_report` used by routes and seed data |
| `services.py` | Builds API views: risk assessment, booking summary/detail, public matches |
| `access.py` | Ownership checks (404 / 403) |
| `models.py` | Pydantic request models and validation |
| `routes/` | `hosts.py`, `bookings.py`, `reports.py` |
| `seed.py` | Demo companies, cars, bookings and reports (dates relative to today) |

### Data model

| Table | Scope | Key columns |
|---|---|---|
| `hosts` | – | `name`, `owner_name`, `city`, `logo` |
| `vehicles` | per company | `host_id`, `name`, `daily_rate`, `value_pkr` |
| `bookings` | private | customer details, dates, `status`, the three fingerprints |
| `network_reports` | shared | `reporter_host_id`, fingerprints, `incident_type`, `severity`, `incident_date`, `private_note` |

### API

No auth (out of scope): the caller passes `host_id`. Every booking/report route checks ownership.

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/hosts` | Companies |
| GET | `/api/hosts/{id}/vehicles` | A company's cars |
| GET | `/api/hosts/{id}/bookings` | Bookings with `risk_score`, `risk_level` |
| GET | `/api/hosts/{id}/reports` | Reports this company made, with `expired` |
| GET | `/api/bookings/{id}?host_id=` | Full detail: customer, car, risk, network matches, own reports |
| POST | `/api/bookings` | Create a booking (the demo form) |
| POST | `/api/bookings/{id}/decision` | `approved` · `declined` · `info_requested` (409 once decided) |
| POST | `/api/bookings/{id}/report` | Report an incident (no future dates, no duplicates) |
| DELETE | `/api/reports/{id}?host_id=` | Withdraw a report (reporter only) |

## 6. Frontend layout (`frontend/src/`)

| Folder | Contents |
|---|---|
| `api/` | `client.js`: one fetch wrapper and all endpoints |
| `pages/` | `BookingsPage`, `ReportsPage` |
| `components/layout/` | `Sidebar`, `PageHeader` |
| `components/bookings/` | List (`RiskFilters`, `BookingGroup`, `BookingRow`) and detail (`DetailHeader`, `BookingSummary`, `DecisionBar`, `ReasonsTable`, `NetworkReports`, `CustomerDetails`, `ReportForm`), plus `NewBookingDialog` |
| `components/reports/` | `ReportsTable` |
| `components/ui/` | `Dropdown`, `Capsule`, `Field`, `Modal`, `Section`, `Toast`, `Icon`, `CompanyLogo` |
| `constants/` | Labels, navigation and footer links, demo customers |
| `hooks/` | `useFetch`, `useToast`, `useDocumentTitle` |
| `styles/` | `tokens`, `base`, `scrollbar`, `layout`, `controls`, `bookings`, `responsive` |
| `utils/` | Date and currency formatting (local dates, never UTC) |

A `version` counter in `App` is bumped after every write, and views refetch so scores always reflect the latest reports.
SEO: page titles per view, meta description, Open Graph image, SVG favicon (1Now car mark) and Apple touch icon.

## 7. Tests (`backend/tests/`)

19 tests, all passing.

| File | Covers |
|---|---|
| `test_identity.py` | Gmail and tag normalisation, Pakistani phone formats, licence formatting, fingerprints hide raw values |
| `test_risk.py` | Each rule, contact-only match → medium, score cap |
| `test_api.py` | Cross-company match despite format changes, expired reports ignored, 403 on another company's booking, report → flag → withdraw with notes never leaked, decision state, validation |

Each API test runs on a fresh temporary database (`TRUST_DB_PATH`).

## 8. Running it

Full guide with Windows commands: [SETUP.md](SETUP.md).

Requires Python 3.10+ and Node.js 18+.

```bash
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

cd ../frontend
npm install
npm run build

cd ../backend
.venv/bin/uvicorn app.main:app      # open http://localhost:8000
.venv/bin/pytest                    # run tests
```

- UI development: `npm run dev` in `frontend/` (http://localhost:5173, `/api` proxied to :8000).
- Reset demo data: stop the server and delete `backend/data/trust.db`.

Expected demo scores at Rao Rent-a-Car: Bilal 95 · Zain 55 · Hamza 40 · Usman 40 · Fatima 0 · Hira 0.

## 9. Scope cuts

| Left out | What production needs |
|---|---|
| Login | `host_id` from the authenticated session, never the request |
| Real ID verification | Use the result of 1Now's existing Vouched checks |
| 1Now integration | Run the check on every new booking, inside the Gatekeeper agent |
| Customer appeals | A way to see and contest reports (consumer-report law) |
| Abuse protection | Reports only on completed trips, rate limits, review of new reporters |
| ML scoring | Needs labelled outcomes first |
| Secret management | Secrets manager and a re-hashing plan for key rotation |
| Localisation | Demo uses Pakistani formats; 1Now's US market needs US phone and licence rules |
