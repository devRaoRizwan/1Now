

https://github.com/user-attachments/assets/4306a56a-95c3-4ad4-9a95-dd1435580818

<div align="center">

<img src="frontend/public/logos/1now.svg" alt="1Now" height="30">

# Renter Trust Network

Rental companies warn each other about bad customers,<br>
so nobody hands their keys to someone who already caused trouble elsewhere.

Built by **Rao Rizwan** · Take-home assignment for [1Now](https://1now.ai)

<br>

<a href="docs/media/renter-trust-network-demo.mp4">
  <img src="docs/media/demo-preview.gif" alt="Demo of Renter Trust Network" width="100%">
</a>

<sub><a href="docs/media/renter-trust-network-demo.mp4">▶ Watch the full demo (1:46)</a></sub>

</div>

---

## The problem

**Turo** is like Airbnb for cars, and it keeps 10–30% of every booking. **1Now** gives car rental companies their own
website, so customers book directly and the company keeps all the money.

But there's a catch. On Turo, a customer who damages a car or refuses to pay **gets banned**. On a company's own
website **nobody is watching**, and the same customer can book with another company the next day.

## The solution

| 1. Report | 2. Check | 3. Decide |
|---|---|---|
| A company reports a customer after a bad experience. | When that customer books with **any** other company on 1Now, they're recognised. | The company sees a risk score with plain reasons, and approves or declines. |

| Score | Meaning |
|:---:|---|
| 🟢 **0 – 29** | Low risk: fine to approve |
| 🟡 **30 – 59** | Medium risk: ask for more info first |
| 🔴 **60 – 100** | High risk: decline, or check ID in person |

**Private by design.** Companies never see each other's customers. Only a scrambled fingerprint of the licence,
email and phone is shared, and reports expire after 2 years.

## Try it

Runs locally, no hosting or accounts needed. You need **Python 3.10+** and **Node.js 18+**.
Full step-by-step guide (Windows, tests, reset): **[docs/SETUP.md](docs/SETUP.md)**.

```bash
cd backend && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
cd ../frontend && npm install && npm run build
cd ../backend && .venv/bin/uvicorn app.main:app
```

Open **http://localhost:8000**. You're signed in as **Rao Rizwan**, owner of **Rao Rent-a-Car**.

1. Click **Bilal Ahmed**. He's high risk: two other companies reported him.
2. Switch company (bottom-left) to **Karachi Drive**, open **Ayesha Siddiqui**, and click **Report customer**.
3. Switch back, click **New booking (demo)**, and choose **Ayesha**. She's flagged straight away.
4. In Karachi Drive's **My reports**, click **Withdraw**. Her flag disappears.

## What's left out

Login, real ID checks, connecting to 1Now's live system, customer appeals and fake-report protection. All data is
sample data. The reasons are in [docs/TECHNICAL.md](docs/TECHNICAL.md#9-scope-cuts).

## Documents

| Document | What's inside |
|---|---|
| [docs/SETUP.md](docs/SETUP.md) | Requirements, install, run, tests and reset |
| [docs/TECHNICAL.md](docs/TECHNICAL.md) | How it works: risk rules, privacy design, data model, API, tests |
| [docs/JOURNEY.md](docs/JOURNEY.md) | How I picked the problem, key decisions, and where I got stuck |
| [CLAUDE.md](CLAUDE.md) | The rules Claude Code followed while building this project |

## Project structure

```
backend/     FastAPI + SQLite API, risk engine and tests
frontend/    React app styled with 1Now's font, colours and logo
docs/        Technical notes, journey and demo media
```
