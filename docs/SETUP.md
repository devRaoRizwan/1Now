# Setup

How to get **Renter Trust Network** running on your machine. It runs fully locally: no accounts, API keys or
hosting needed, and the sample data creates itself on first start.

**Time needed:** about 2 minutes (most of it is downloading packages).

---

## 1. Requirements

| Tool | Minimum version | Check with |
|---|---|---|
| Git | any recent | `git --version` |
| Python | **3.10** or newer | `python3 --version` |
| Node.js | **18** or newer | `node --version` |
| npm | 9 or newer (comes with Node.js) | `npm --version` |

Also needed:

- **Disk space:** about 100 MB (Python packages ~40 MB, Node packages ~45 MB).
- **Free port:** `8000` (and `5173` only if you use development mode).
- **Internet** for the first install. The app itself also loads the Geist font from Google Fonts.
- **OS:** Linux, macOS or Windows. Windows commands are listed separately where they differ.

> **Linux (Debian/Ubuntu) only:** if `python3 -m venv` fails, install the venv package first:
> `sudo apt install python3-venv`

---

## 2. Get the code

```bash
git clone <repository-url> renter-trust-network
cd renter-trust-network
```

Replace `<repository-url>` with the GitHub link to this repository.

You should see:

```
backend/    Python API (FastAPI + SQLite)
frontend/   React app
docs/       Documentation and demo media
```

---

## 3. Run it (one terminal)

The backend serves both the API and the built React app, so a single terminal is enough.

### Linux / macOS

```bash
# 1. Install the backend
cd backend
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt

# 2. Build the frontend
cd ../frontend
npm install
npm run build

# 3. Start the app
cd ../backend
.venv/bin/uvicorn app.main:app
```

### Windows (PowerShell)

```powershell
# 1. Install the backend
cd backend
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt

# 2. Build the frontend
cd ..\frontend
npm install
npm run build

# 3. Start the app
cd ..\backend
.venv\Scripts\uvicorn app.main:app
```

When you see `Uvicorn running on http://127.0.0.1:8000`, open **http://localhost:8000** in your browser.

Press **Ctrl + C** in the terminal to stop the server.

### Next time

Steps 1 and 2 are only needed once. Afterwards, just start the app:

```bash
cd backend
.venv/bin/uvicorn app.main:app          # Windows: .venv\Scripts\uvicorn app.main:app
```

---

## 4. Development mode (two terminals)

Use this only if you want to edit the frontend and see changes instantly.

**Terminal 1: backend, restarts on code changes**

```bash
cd backend
.venv/bin/uvicorn app.main:app --reload
```

**Terminal 2: frontend, with hot reload**

```bash
cd frontend
npm run dev
```

Open **http://localhost:5173**. The frontend forwards all `/api` calls to the backend on port 8000, so keep
terminal 1 running.

---

## 5. Run the tests

```bash
cd backend
.venv/bin/pytest                         # Windows: .venv\Scripts\pytest
```

Expected result: `19 passed`. Each test uses its own temporary database, so your demo data is never touched.

---

## 6. Try the demo

You're signed in as **Rao Rizwan**, owner of **Rao Rent-a-Car**.

1. Click **Bilal Ahmed**: high risk (95), reported by two other companies.
2. Switch company (bottom-left) to **Karachi Drive**, open **Ayesha Siddiqui**, click **Report customer**.
3. Switch back, click **New booking (demo)**, choose **Ayesha Siddiqui**, submit: flagged (70).
4. In Karachi Drive's **My reports**, click **Withdraw**: Ayesha drops back to low risk (0).

Expected scores on a fresh start: Bilal 95 · Zain 55 · Hamza 40 · Usman 40 · Fatima 0 · Hira 0.

---

## 7. Reset the demo data

Clicking around changes the data. To start fresh:

1. Stop the server (**Ctrl + C**).
2. Delete the database: `rm -rf backend/data` (Windows: `rmdir /s /q backend\data`).
3. Start the server again. Fresh sample data is created automatically.

---

## Tested with

Linux · Python 3.14 · Node.js 22 · npm 9 · Chrome. Fresh-clone install time: about 15 seconds on a fast connection.
