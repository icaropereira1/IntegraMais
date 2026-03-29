# Codebase Structure

**Analysis Date:** 2026-03-28

## Directory Layout

```
IntegraMais/
├── services/          # Business logic and platform integrations
│   ├── ifood.py       # iFood API interaction
│   └── vuca.py        # Vuca scraping logic
├── utils/             # Cross-cutting utility functions
│   └── excel.py       # Excel generation and formatting
├── app.py             # Main UI entry point (Streamlit)
├── config.py          # Global application settings
├── README.md          # Project documentation
└── requirements.txt   # Python dependencies
```

## Directory Purposes

**`services/`:**
- Purpose: Contains the logic for interacting with external services and platforms.
- Contains: Integration modules for iFood and Vuca.
- Key files: `services/ifood.py`, `services/vuca.py`

**`utils/`:**
- Purpose: Provides common utility functions that are not tied to a specific business domain.
- Contains: Logic for Excel manipulation and potentially other helper functions.
- Key files: `utils/excel.py`

**`.planning/`:**
- Purpose: Holds documentation and analysis regarding the codebase structure and evolution.
- Contains: Codebase mapping and architectural documentation.

## Key File Locations

**Entry Points:**
- `app.py`: The primary entry point for the Streamlit application. Run it via `streamlit run app.py`.

**Configuration:**
- `config.py`: Centralized location for URLs, column definitions, and other constants used throughout the app.

**Core Logic:**
- `services/ifood.py`: Handles OAuth2 flow and Merchant API (v1.0 and v2.0) interactions.
- `services/vuca.py`: Handles session-based authentication and HTML parsing for menu extraction.

**Testing:**
- Not detected. No testing directory or files found in the project root.

## Naming Conventions

**Files:**
- Snake Case: `ifood.py`, `app.py`, `excel.py`.

**Directories:**
- Lowercase: `services/`, `utils/`.

## Where to Add New Code

**New Platform Integration:**
- Primary code: Create a new module in `services/` (e.g., `services/rappi.py`).
- Configuration: Add necessary endpoints and column maps to `config.py`.
- UI Integration: Add a new tab or section to `app.py`.

**New UI Feature:**
- Logic: Implement within `app.py`.
- Supporting Functions: Add to existing services in `services/` or a new utility in `utils/`.

**Utilities:**
- Shared helpers: Add new logic to `utils/` (e.g., `utils/csv_helper.py`).

## Special Directories

**`__pycache__/`:**
- Purpose: Contains compiled Python bytecode files.
- Generated: Yes.
- Committed: No.

**`.git/`:**
- Purpose: Contains the git repository metadata.
- Generated: Yes.
- Committed: No.

---

*Structure analysis: 2026-03-28*
