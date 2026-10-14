# Journey

**Rao Rizwan** · notes on how this feature was picked, planned and built with Claude Code.

## 1. Understanding 1Now

- Researched 1now.ai and its market with Claude, then wrote a SWOT analysis.
- 1Now helps Turo hosts and small rental companies take **direct bookings** on their own site, so they keep the
  10–30% Turo would take.
- Competitors: Turo itself, FleetWire (cheaper, simpler), Wheelbase, and larger rental software (HQ, Rent Centric).

## 2. Picking the problem

The biggest threat in the SWOT: **on Turo, Turo protects hosts from bad renters; on a direct site the host is on
their own.** If hosts get burned on direct bookings, they go back to Turo, and 1Now's main pitch breaks.

| Option | Decision |
|---|---|
| Shared bad-customer warning network | **Chosen.** A fraud check that gets stronger with every company on 1Now, which a single host can't build |
| "How much is Turo costing you?" fee report | Dropped. Only supports the sales pitch, and Turo forbids moving its guests off-platform |
| Migration tool for Getaround/HyreCar hosts | Dropped. One-time use, hard to demo |

## 3. Planning before code

- Claude started building straight away. I stopped it and asked for the README and scope first, so rules and cuts
  were agreed before any code.
- Wrote a `CLAUDE.md` so every session follows the same rules: privacy, scoring, scope, and plan-before-code.

## 4. Decisions and assumptions

- **Licence is the strongest identity signal.** Email and phone can be shared, so a contact-only match scores lower
  and asks for verification instead of a decline.
- **Companies never see each other's customers.** The shared table stores keyed fingerprints only.
- **People deserve a way back.** Reports expire after 24 months and can be withdrawn.
- **Rules over AI.** Every point has a sentence behind it, so a decline can be explained to the customer.
- **No login.** The brief says skip it; a company switcher stands in.
- **Local names.** I found "host" and "renter" hard to tell apart in the demo, so the UI says *company* and
  *customer*, and the demo uses Pakistani companies and customers (Rs, +92 phones, provinces). The code keeps
  1Now's own terms.

## 5. Iterations

1. Plain HTML first, then switched to **React** with 1Now's real font (Geist), colours and logo.
2. Reworked the layout into a full-width dashboard: sidebar, custom dropdowns, capsules for every status,
   and clearly separated "waiting" and "past" groups. Tried a footer with 1Now's links, then removed it:
   it added clutter without helping the task.
3. Cleaned the codebase: split into `backend/` and `frontend/`, small modules, one component per file,
   shared booking/report writes used by both the API and the demo data.

## 6. Where I got stuck

- **Dropdown re-opening on click.** Wrapping the custom dropdown in a `<label>` made every option click re-trigger
  the button. Fixed by using a plain `<div>` wrapper for dropdown fields.
- **Off-by-one date after midnight.** The report form showed yesterday's date: the frontend used `toISOString()`,
  which is UTC, while Pakistan is UTC+5. Found during an end-to-end browser test and fixed with a local-date helper.
- **Demo data drifting.** Clicking around changed scores (Bilal dropped from 95 to 75 after a withdrawal).
  Reset is now documented: delete `backend/data/trust.db`. The demo video was recorded on a fresh database.

## 7. What I would do next

- A way for customers to see and appeal reports (fairness and consumer-report law).
- Protection against fake or revenge reports: only allow reports on completed trips, review reports from new companies.
- Run the check automatically in 1Now's booking flow, inside the "Gatekeeper" AI agent.
- US phone and licence formats for 1Now's real market.
