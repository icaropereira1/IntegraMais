# Architecture

**Analysis Date:** 2026-03-28

## Pattern Overview

**Overall:** Layered Service Architecture with Streamlit UI.

**Key Characteristics:**
- **Modular Services:** Integration logic for external platforms (iFood, Vuca) is encapsulated in dedicated service modules.
- **Stateful UI:** Uses Streamlit for managing application state and user interactions in a reactive manner.
- **Data-Centric Exchange:** Excel files (`.xlsx`) are used as the primary medium for user-facing data manipulation and batch updates.

## Layers

**UI Layer:**
- Purpose: Handles user interaction, input validation, and high-level workflow orchestration.
- Location: `app.py`
- Contains: Streamlit components, tab definitions, and call-to-action handlers.
- Depends on: `services/`, `utils/`, `config.py`
- Used by: End users.

**Service Layer:**
- Purpose: Encapsulates communication logic with external platforms (APIs or Web Scraping).
- Location: `services/`
- Contains: API client functions, web scraping logic, and platform-specific data formatting.
- Depends on: `config.py`, external libraries (`requests`, `beautifulsoup4`).
- Used by: `app.py`

**Utility Layer:**
- Purpose: Provides shared, non-business specific functionality.
- Location: `utils/`
- Contains: Excel generation and formatting logic.
- Depends on: `config.py`, `pandas`, `xlsxwriter`.
- Used by: `app.py`

## Data Flow

**iFood Menu Extraction:**
1. User provides iFood credentials in `app.py`.
2. `app.py` calls `services/ifood.py:get_token()` for authentication.
3. `app.py` calls `services/ifood.py:extrair_cardapio_ifood()` to fetch categories and items.
4. Data is returned as a `pandas.DataFrame`.
5. `app.py` calls `utils/excel.py:gerar_excel_em_memoria()` to format the data into a protected Excel file.
6. User downloads the file via `st.download_button`.

**iFood PDV Update:**
1. User uploads a modified Excel file in `app.py`.
2. `app.py` reads the file using `pandas`.
3. `app.py` calls `services/ifood.py:mapear_codigos_atuais()` to detect changes and avoid redundant updates.
4. `app.py` iterates through the rows and calls `services/ifood.py:atualizar_item()` for each change.

**Vuca Menu Extraction:**
1. User provides Vuca credentials and selects a delivery platform in `app.py`.
2. `app.py` calls `services/vuca.py:logar_vuca()` to establish a session.
3. `app.py` calls `services/vuca.py:extrair_cardapio_vuca()` which performs web scraping.
4. Scraped data is converted to a `pandas.DataFrame`.
5. `app.py` calls `utils/excel.py:gerar_excel_em_memoria()` for file generation.

**State Management:**
- Streamlit manages the session state for UI components.
- Platform sessions (e.g., Vuca `requests.Session`) are managed within the service logic during the execution of a request.

## Key Abstractions

**iFood API Client:**
- Purpose: Manages interaction with iFood's Merchant API.
- Examples: `services/ifood.py`
- Pattern: API Wrapper.

**Vuca Scraper:**
- Purpose: Navigates the Vuca Solution back-office to extract menu data.
- Examples: `services/vuca.py`
- Pattern: Web Scraper with Session management.

**Excel Formatter:**
- Purpose: Standardizes the look and feel and protection of generated Excel files.
- Examples: `utils/excel.py`
- Pattern: Utility Helper.

## Entry Points

**Streamlit Web App:**
- Location: `app.py`
- Triggers: Execution via `streamlit run app.py`.
- Responsibilities: Main UI loop, configuration of sidebar, and tab navigation.

## Error Handling

**Strategy:** Bubbling exceptions from services to the UI layer for user notification.

**Patterns:**
- **Service Exceptions:** Raise `Exception` with descriptive messages when API calls or scraping fails (e.g., `services/ifood.py:get_token`).
- **UI Feedback:** Use `st.error()`, `st.warning()`, and `st.success()` in `app.py` to communicate status to the user.
- **Rate Limiting:** Explicit handling of `429` status codes in `app.py` using `time.sleep()`.

## Cross-Cutting Concerns

**Logging:** Minimal logging currently; mostly handled via `st.info()` or `st.text()` in the UI for progress tracking.
**Validation:** Basic credential presence checks in `app.py`.
**Authentication:** Handled per-service (`OAuth2` for iFood, Form-based login for Vuca).

---

*Architecture analysis: 2026-03-28*
