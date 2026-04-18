# Laplace's Demon 🔬

> *"We may regard the present state of the universe as the effect of its past and the cause of its future."*
> — Pierre-Simon Laplace

**Laplace's Demon** is a desktop application for scientific and mathematical computation. It provides a library of mathematical operations, a user authentication system, and a personal archive where every calculation you run is saved and searchable — so you can always trace back your work.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Database Schema](#database-schema)
- [Configuration](#configuration)
- [Security Notes](#security-notes)
- [Known Issues & Roadmap](#known-issues--roadmap)
- [Contributing](#contributing)

---

## Overview

Laplace's Demon is a multi-user desktop application built with **Python** and **PyQt6**. It connects to a **PostgreSQL** database running locally via **Docker**, where it stores user accounts, preferences, and a full history of every operation performed.

The application is structured around three core sections:

- **Laplace's Library** — the collection of mathematical/scientific operations available to run
- **Laplace's Archive** — a searchable log of all past calculations, filterable by date
- **Profile & Preferences** — per-user settings including theme, font color, and language

---

## Features

### Authentication
- Account registration and login with username/password
- "Remember Me" functionality using token-based persistent sessions stored securely via `QSettings`
- Token revocation on logout
- Login telemetry: last successful and failed login timestamps, IP address, and MAC address are recorded

### Laplace's Library
- A curated collection of mathematical operations
- Double-click any operation to open it as a new tab
- Results are automatically saved to the archive upon successful calculation

### Laplace's Archive
- Full history of every calculation you have run
- Filter records by date or date range
- Double-click any record to reopen its full input/output data
- Record count displayed in the UI header

### User Preferences
- Choose your preferred **language** (e.g., `en`, `tr`)
- Choose your preferred **theme** (e.g., `dark`, `light`)
- Choose your preferred **font color** (hex code)
- Preferences are persisted per user in the database

### About Me / User Stats
- View your account opening date
- See your last successful and failed login details
- Track total operation usage and per-operation usage counts
- See your most used and last used operation

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI Framework | [PyQt6](https://pypi.org/project/PyQt6/) |
| Database | [PostgreSQL 15](https://www.postgresql.org/) |
| DB Driver | [psycopg2](https://pypi.org/project/psycopg2/) |
| Containerization | [Docker](https://www.docker.com/) + [Docker Compose](https://docs.docker.com/compose/) |
| Language | Python 3.10+ |

---

## Prerequisites

Before you start, make sure you have the following installed on your system:

1. **Python 3.10+** — [Download](https://www.python.org/downloads/)
2. **Docker Desktop** (or Docker Engine + Docker Compose) — [Download](https://www.docker.com/products/docker-desktop/)
3. **Git** — [Download](https://git-scm.com/)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/selimutkusonmez/Laplace-s-Demon.git
cd Laplace-s-Demon
```

### 2. Create and activate a virtual environment

```bash
# Create
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

### 3. Install Python dependencies

```bash
pip install PyQt6 psycopg2-binary bcrypt
```

> **Note:** A `requirements.txt` will be added to the repository to formalize these dependencies. Until then, use the command above.

### 4. Configure environment variables (recommended)

The default Docker Compose file uses hardcoded credentials for convenience. For any use beyond local testing, copy the example env file and edit it:

```bash
cp .env.example .env
```

Then edit `.env`:

```env
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=laplace_db
DB_HOST=localhost
DB_PORT=5432
```

> ⚠️ See [Security Notes](#security-notes) for important information about the default credentials.

### 5. Start the database

```bash
docker compose up -d
```

This will:
- Pull the `postgres:15` image if not already present
- Start a container named `laplace_db`
- Mount `init.sql` to automatically create all tables, triggers, and functions on first run
- Create a persistent volume at `./pg_data` so your data survives container restarts

You can verify the database is running with:

```bash
docker compose ps
```

---

## Running the Application

Once the database is up, start the app:

```bash
python main.py
```

On first launch you will see the **Login** screen. Create a new account, then log in to access the Library and Archive.

### Stopping the database

```bash
docker compose down
```

To also remove all stored data (full reset):

```bash
docker compose down -v
```

---

## Project Structure

```
Laplace-s-Demon/
│
├── main.py                  # Entry point — instantiates AppManager
├── config.py                # Path constants (BASE_DIR, STYLE_PATH, JPG_PATH)
├── docker-compose.yml       # PostgreSQL service definition
├── init.sql                 # Full DB schema: tables, triggers, functions
├── requirements.txt         # Python dependencies (to be populated)
├── .gitignore
│
└── src/
    ├── ui/
    │   ├── __init__.py      # Exports: MainUI, LoginUI, LaplaceArchiveUI,
    │   │                    #          DatabaseManager, LaplaceLibraryUI
    │   ├── main_ui.py       # MainUI — tab container, profile menu, signal routing
    │   ├── login_ui.py      # LoginUI — login form, remember-me, new account link
    │   ├── library_ui.py    # LaplaceLibraryUI — operation list
    │   ├── archive_ui.py    # LaplaceArchiveUI — history log, date filter
    │   ├── database.py      # DatabaseManager — all DB interactions
    │   │
    │   ├── profile/
    │   │   ├── __init__.py
    │   │   ├── preferences_ui.py      # Theme, language, font color settings
    │   │   ├── about_me_ui.py         # User stats dashboard
    │   │   └── create_account_ui.py   # New account registration form
    │   │
    │   └── operations/      # Individual mathematical operation UIs
    │       └── ...
    │
    └── assets/
        ├── style/           # QSS stylesheets (dark/light themes)
        └── image/           # JPG/PNG assets used in the UI
```

### Key Design Pattern: AppManager as Mediator

`AppManager` (in `main.py`) owns all top-level components and wires them together. UI modules never talk to each other directly — they emit Qt signals, and `AppManager` routes them to the appropriate handler. This keeps the UI components decoupled from the database and from each other.

```
LoginUI ──signal──► AppManager ──calls──► DatabaseManager
                        │
                        └──────────────► MainUI (adds tab)
```

---

## Database Schema

The database is initialized automatically from `init.sql` when the Docker container first starts.

### Tables

**`users`** — Core account table
| Column | Type | Notes |
|---|---|---|
| id | SERIAL | Primary key |
| username | varchar(50) | Unique |
| password | varchar(255) | Hashed |
| auth_token | varchar(255) | For "remember me" sessions |
| date | TIMESTAMP | Account creation time |

**`operation_history`** — Archive of every calculation
| Column | Type | Notes |
|---|---|---|
| id | SERIAL | Primary key |
| user_id | INTEGER | FK → users |
| date | TIMESTAMP | When the operation was run |
| operation | varchar(50) | Operation name |
| variables | varchar(255) | Variable names used |
| input_data | TEXT | Input values |
| output | TEXT | Result |

**`logs`** — Login attempt audit trail
| Column | Type | Notes |
|---|---|---|
| id | SERIAL | Primary key |
| user_id | INTEGER | FK → users |
| ip_address | varchar(255) | Requester IP |
| mac_address | varchar(255) | Requester MAC |
| attempt | varchar(20) | `'successful'` or `'failed'` |
| date | TIMESTAMP | When the attempt occurred |

**`user_preferences`** — Per-user UI settings
| Column | Type | Default |
|---|---|---|
| user_id | INTEGER | PK, FK → users |
| preferred_language | varchar(10) | `'en'` |
| preferred_theme | varchar(10) | `'dark'` |
| preferred_font_color | varchar(50) | `'#ADBAC7'` |

**`user_stats`** — Usage analytics per user
| Column | Type | Notes |
|---|---|---|
| user_id | INTEGER | PK, FK → users |
| account_opening_date | TIMESTAMP | Auto-set on registration |
| last_successful_login_date | TIMESTAMP | Updated by trigger |
| last_failed_login_date | TIMESTAMP | Updated by trigger |
| total_operation_usage | INTEGER | Incremented by trigger |
| operation_usage_counts | JSONB | Per-operation counts `{"FFT": 5, ...}` |
| most_used_operation | varchar(50) | Derived by trigger |
| last_used_operation | varchar(50) | Updated by trigger |

### Triggers

The schema includes three PostgreSQL triggers that run automatically:

| Trigger | Event | Action |
|---|---|---|
| `after_user_registration` | `INSERT` on `users` | Creates rows in `user_preferences` and `user_stats` |
| `after_login_attempt` | `INSERT` on `logs` | Updates `user_stats` with latest login telemetry |
| `after_operation_insert` | `INSERT` on `operation_history` | Increments usage counts and updates `most_used_operation` |

---

## Configuration

`config.py` exposes two path constants used throughout the application:

```python
STYLE_PATH  # → src/assets/style/   (QSS theme files)
JPG_PATH    # → src/assets/image/   (image assets)
```

These are built with `os.path` so they work correctly on all operating systems.

---

## Security Notes

> ⚠️ **Default credentials are not secure.** The `docker-compose.yml` ships with `POSTGRES_USER=admin` and `POSTGRES_PASSWORD=1234` for convenience during development. **Do not use these in any environment where the machine is accessible to others.** Replace them with strong credentials via a `.env` file before sharing or deploying.

Additional security considerations:

- Passwords should be stored hashed (e.g., using `bcrypt`) — never as plain text
- Auth tokens should be generated with a cryptographically secure random function (e.g., `secrets.token_hex(32)`)
- The `logs` table collects IP and MAC addresses — be mindful of applicable data privacy regulations if this data is ever shared or stored remotely

---

## Known Issues & Roadmap

### Known Issues
- `requirements.txt` is currently empty — dependencies must be installed manually
- `handle_tab_close` in `AppManager` is a stub and does not yet clean up resources when a tab is closed
- `LaplaceLibraryUI` is instantiated without its preferences argument in one code path (`handle_login_without_token`), which may cause inconsistent theming

### Potential Improvements
- [ ] Populate `requirements.txt`
- [ ] Move DB credentials to `.env` / environment variables
- [ ] Add password strength validation on account creation
- [ ] Implement tab close cleanup logic
- [ ] Add unit tests for `DatabaseManager`
- [ ] Add a `--reset-db` CLI flag for easy local resets
- [ ] Export archive records to CSV

---

## Contributing

Contributions are welcome. To get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add your feature"`
4. Push to your fork: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please open an issue first for significant changes so the approach can be discussed.

---

*Named after the 19th-century thought experiment by Pierre-Simon Laplace, which imagines an intellect that knows the state of every particle in the universe and can therefore compute the entire future — and past — of reality.*
