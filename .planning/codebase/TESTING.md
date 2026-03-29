# Testing Patterns

**Analysis Date:** 2025-02-14

## Test Framework

**Runner:**
- Not detected.

**Assertion Library:**
- Not applicable.

**Run Commands:**
```bash
# No test runner configured.
```

## Test File Organization

**Location:**
- No tests exist in the current codebase.

**Naming:**
- Not applicable.

**Structure:**
```
[No test files detected]
```

## Test Structure

**Suite Organization:**
```python
# No test suite detected.
```

**Patterns:**
- No test patterns (Setup, Teardown, Assertions) are currently implemented.

## Mocking

**Framework:** None detected.

**Patterns:**
```python
# No mocking patterns found.
```

**What to Mock:**
- API calls (requests) to iFood and Vuca endpoints.
- Pandas operations that depend on external files or API data.

**What NOT to Mock:**
- Pure logic for data transformation.
- Excel generation helpers in `utils/excel.py` (though verification of the resulting byte streams may be complex).

## Fixtures and Factories

**Test Data:**
```python
# No test data fixtures or factories detected.
```

**Location:**
- Not applicable.

## Coverage

**Requirements:** None enforced.

**View Coverage:**
```bash
# Not applicable.
```

## Test Types

**Unit Tests:**
- Not applicable.

**Integration Tests:**
- Not applicable.

**E2E Tests:**
- Not applicable.

## Common Patterns

**Async Testing:**
- No async testing patterns found.

**Error Testing:**
- No error testing patterns found.

## Recommendations

The codebase currently lacks an automated testing suite. Given the Python stack, it is highly recommended to introduce **pytest** for unit and integration testing.

- Use **pytest-mock** to mock `requests` calls in `services/ifood.py` and `services/vuca.py`.
- Implement unit tests for `utils/excel.py` to ensure Excel generation logic remains stable.
- Add regression tests for data mapping functions in `services/ifood.py` (e.g., `extrair_cardapio_ifood`).

---

*Testing analysis: 2025-02-14*
