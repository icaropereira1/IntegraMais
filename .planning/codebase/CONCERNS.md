# Codebase Concerns

**Analysis Date:** 2024-10-24

## Tech Debt

**Hardcoded Secrets:**
- Issue: The Excel protection password is hardcoded in the configuration file.
- Files: `config.py`
- Impact: If the codebase is shared or committed to a public repository, the password for generated files is exposed.
- Fix approach: Move secrets to environment variables (e.g., using a `.env` file and `python-dotenv`).

**Fragile Web Scraper:**
- Issue: Integration with the Vuca system relies on scraping HTML using `BeautifulSoup`.
- Files: `services/vuca.py`
- Impact: Any UI change in the Vuca platform (e.g., class name changes, structural changes) will break the integration.
- Fix approach: If available, use a private API; otherwise, implement more robust error handling and potentially a way to easily update selectors.

**Missing Test Suite:**
- Issue: There are no unit or integration tests in the codebase.
- Files: Project-wide
- Impact: High risk of regressions when making changes, especially given the fragile nature of the Vuca scraper and the iFood API interactions.
- Fix approach: Implement a testing framework like `pytest` and add tests for data processing, Excel generation, and (mocked) API calls.

## Security Considerations

**Credential Exposure:**
- Risk: While Streamlit's `type="password"` hides input in the UI, the application handles sensitive credentials (API keys, login passwords) without encryption in memory.
- Files: `app.py`, `services/ifood.py`, `services/vuca.py`
- Current mitigation: Streamlit `password` input type for UI masks.
- Recommendations: Ensure the application is deployed over HTTPS and consider using a more secure way to manage short-lived tokens.

**Excel Protection:**
- Risk: The hardcoded password `xicaroehfoda` in `config.py` is easily discoverable.
- Files: `config.py`, `utils/excel.py`
- Current mitigation: Basic Excel sheet protection.
- Recommendations: Allow users to provide their own password or use a securely stored secret.

## Performance Bottlenecks

**N+1 Query Pattern in Vuca Scraper:**
- Problem: The Vuca scraper makes a separate HTTP request for every product to fetch its optional items.
- Files: `services/vuca.py`
- Cause: The `extrair_detalhes_adicionais` function is called inside a loop over all items in `extrair_cardapio_vuca`.
- Improvement path: Investigate if the Vuca platform allows fetching all items and options in a single request or implement parallel requests (with care for rate limits).

**Sequential iFood Updates:**
- Problem: Updating codes in iFood is done sequentially with a fixed 0.4s sleep between requests.
- Files: `app.py`
- Cause: Simple loop with `time.sleep(0.4)`.
- Improvement path: Implement a dynamic rate-limiting strategy that adjusts based on response headers or hits and consider using asynchronous requests (e.g., `aiohttp`) if the API allows higher concurrency.

## Fragile Areas

**HTML Parsing (Vuca):**
- Files: `services/vuca.py`
- Why fragile: Relies on specific class names like `js-categorias`, `js-tr-`, and `box-registros`. It also assumes the first class of an element contains the ID (`edita_vuca_semformatacao[0]`).
- Safe modification: Encapsulate selector logic or use a more descriptive parsing strategy.
- Test coverage: None.

**Excel Parsing (iFood Update):**
- Files: `app.py`
- Why fragile: Assumes the uploaded Excel file has specific column names like `ID iFood` and `Código PDV (externalCode)`.
- Safe modification: Add validation for column existence before processing the DataFrame.
- Test coverage: None.

## Missing Critical Features

**Retry Logic for Network Failures:**
- Problem: Most network requests (except for iFood's 429) do not have retry logic.
- Blocks: Transient network errors can cause the entire process (especially long updates) to fail.
- Files: `services/ifood.py`, `services/vuca.py`

**Comprehensive Logging:**
- Problem: The application relies on Streamlit UI for status reporting but lacks persistent or detailed logs.
- Blocks: Debugging production issues or tracking historical performance/errors is difficult.
- Files: Project-wide

## Test Coverage Gaps

**Data Processing Logic:**
- What's not tested: Parsing of iFood's catalog tree, formatting of Vuca item codes, and Excel generation.
- Files: `services/ifood.py`, `services/vuca.py`, `utils/excel.py`
- Risk: Formatting errors can lead to incorrect PDV codes being pushed to iFood.
- Priority: High

**API Integration:**
- What's not tested: Handling of various API error codes (401, 403, 404, 500).
- Files: `services/ifood.py`
- Risk: Application crashes or silently fails when iFood's API behaves unexpectedly.
- Priority: Medium

---

*Concerns audit: 2024-10-24*
