# Technology Stack

**Analysis Date:** 2025-01-24

## Languages

**Primary:**
- Python 3.x - Backend logic, data processing, and UI (Streamlit).

## Runtime

**Environment:**
- Python Runtime

**Package Manager:**
- pip
- Lockfile: missing (only `requirements.txt` present)

## Frameworks

**Core:**
- Streamlit - Used for the web-based dashboard and user interface. `app.py`

**Data Processing:**
- Pandas - Used for data manipulation, cleaning, and Excel preparation. `app.py`, `services/ifood.py`, `services/vuca.py`, `utils/excel.py`
- BeautifulSoup4 (bs4) - Used for parsing HTML during web scraping of the Vuca portal. `services/vuca.py`

## Key Dependencies

**Critical:**
- `requests` - Handles all HTTP communication with the iFood API and Vuca portal.
- `xlsxwriter` - Engine used by Pandas to generate protected and formatted Excel files. `utils/excel.py`
- `openpyxl` - Used by Pandas to read Excel files uploaded by the user. `app.py`

## Configuration

**Environment:**
- Credentials (Client ID, Secret, Login, Password) are provided via Streamlit sidebar inputs at runtime. `app.py`

**Build:**
- `requirements.txt` - Lists all Python dependencies.
- `config.py` - Contains API endpoints, Excel styling constants, and protection passwords.

## Platform Requirements

**Development:**
- Python 3.10+ recommended.
- Internet access for API calls and scraping.

**Production:**
- Streamlit Cloud, Heroku, or any VPS capable of running Python applications.

---

*Stack analysis: 2025-01-24*
