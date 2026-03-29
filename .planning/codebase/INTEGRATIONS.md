# External Integrations

**Analysis Date:** 2025-01-24

## APIs & External Services

**Delivery Platforms (iFood):**
- iFood Merchant API - Used to extract the current catalog and update external codes for menu items and options.
  - SDK/Client: `requests`
  - Auth: OAuth 2.0 (Client ID and Secret provided by user via UI)
  - Endpoints (defined in `config.py`):
    - `https://merchant-api.ifood.com.br/authentication/v1.0/oauth/token` (Auth)
    - `https://merchant-api.ifood.com.br/catalog/v1.0/merchants` (Catalog v1)
    - `https://merchant-api.ifood.com.br/catalog/v2.0/merchants` (Catalog v2)

**Management Portal (Vuca Solution):**
- Vuca Solution - Web scraping to extract menu data from the management portal.
  - SDK/Client: `requests` (Session-based) and `BeautifulSoup4`
  - Auth: Session login (Username and Password provided by user via UI)
  - Base URL: `https://[instancia].vucasolution.com.br/retaguarda/`
  - Supported Platforms via Vuca:
    - iFood
    - Accon
    - Anota AI
    - Delivery Direto
    - 99Food (nnfood)
    - Cardápio Web
    - Keeta

## Data Storage

**Databases:**
- None detected. Data is processed in-memory using Pandas.

**File Storage:**
- Local memory (BytesIO) used to generate and serve Excel files (`.xlsx`) to the user. `utils/excel.py`

**Caching:**
- None detected.

## Authentication & Identity

**Auth Provider:**
- Custom / Third-party (iFood and Vuca).
  - Implementation: API tokens for iFood and Session-based login for Vuca. `services/ifood.py`, `services/vuca.py`

## Monitoring & Observability

**Error Tracking:**
- None (Streamlit's default error handling and `st.error` blocks).

**Logs:**
- No dedicated logging framework detected. Simple stdout/console logs might be used during Streamlit's runtime.

## Environment Configuration

**Required input data (Runtime):**
- iFood Client ID
- iFood Client Secret
- iFood Merchant ID
- Vuca Instance
- Vuca Unidade ID
- Vuca Login
- Vuca Password

**Secrets location:**
- No `.env` or secrets manager detected. Secrets are entered by the user in the UI at runtime and are not persisted.

## Webhooks & Callbacks

**Incoming:**
- None.

**Outgoing:**
- None.

---

*Integration audit: 2025-01-24*
