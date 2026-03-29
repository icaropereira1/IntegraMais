# Coding Conventions

**Analysis Date:** 2025-02-14

## Naming Patterns

**Files:**
- snake_case: `app.py`, `config.py`, `services/ifood.py`, `utils/excel.py`

**Functions:**
- snake_case: `get_token`, `extrair_cardapio_ifood`, `gerar_excel_em_memoria`

**Variables:**
- snake_case: `client_id`, `merchant_id`, `v_instancia`, `df_cardapio`

**Types:**
- Classes are not used in the current codebase.

## Code Style

**Formatting:**
- No automated formatter (like Black) configuration detected.
- Code generally follows PEP 8 style manually.

**Linting:**
- No linting configuration (like Flake8 or Pylint) detected.

## Import Organization

**Order:**
1. Standard library (e.g., `import time`, `import io`)
2. Third-party libraries (e.g., `import streamlit as st`, `import pandas as pd`)
3. Local modules (e.g., `from config import ...`, `from services.ifood import ...`)

**Path Aliases:**
- None detected. Relative/absolute imports from the project root are used: `from services.vuca import ...`

## Error Handling

**Patterns:**
- Extensive use of `try...except` blocks in UI code (`app.py`).
- Functions in services often raise exceptions with descriptive messages when API calls fail.
- Errors are displayed to the user via Streamlit's `st.error()` or `st.warning()`.

## Logging

**Framework:** None (standard `logging` module not used).

**Patterns:**
- Feedback is provided directly to the user interface via `st.info()`, `st.success()`, and `st.spinner()`.
- Error messages are printed or shown in the UI.

## Comments

**When to Comment:**
- Section headers are used in `app.py` to organize the UI layout (e.g., `# --- CONFIGURAÇÃO DA PÁGINA ---`).
- Inline comments are used to explain specific steps or logic (e.g., `# Respeito ao Rate Limit do iFood` in `app.py`).

**JSDoc/TSDoc:**
- Not applicable (Python). Docstrings (PEP 257) are not used in the current codebase.

## Function Design

**Size:**
- Most functions are small and focused (e.g., `get_token` in `services/ifood.py`).
- Some UI logic in `app.py` within Streamlit tabs is relatively long but follows a procedural flow.

**Parameters:**
- Functions use positional and keyword arguments.
- Type hints are not used.

**Return Values:**
- Functions return specific data types (e.g., strings for tokens, DataFrames for data, `io.BytesIO` for files) or the result of a `requests` call.

## Module Design

**Exports:**
- Standard Python exports using `def` at the module level.
- `__init__.py` files are present in `services/` and `utils/` but are empty, indicating no special package-level exports.

**Barrel Files:**
- Not used.

---

*Convention analysis: 2025-02-14*
