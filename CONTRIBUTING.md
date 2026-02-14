# Contributing to Pyodide Patterns Cookbook

We welcome contributions! This project is a curated collection of architectural wisdom for Pyodide developers.

## Engineering Standards

To keep the cookbook high-quality and reliable, we adhere to the following standards:

1.  **Strict Typing**: All Python code in `src/` must be fully type-hinted and pass `mypy`.
2.  **Linting**: We use `ruff` for linting and formatting.
3.  **Pre-commit**: Please install the pre-commit hooks before making changes:
    ```bash
    pip install pre-commit
    pre-commit install
    ```
4.  **Verified Patterns**: Every new pattern in `docs/patterns/` must be accompanied by a working example in `examples/` and a verification test in `tests/patterns/`.

## Pattern Schema

All narrative patterns must follow this schema:
*   **Context**: When does this situation arise?
*   **Problem**: What is the specific challenge?
*   **Forces**: What are the competing constraints (performance, security, DX)?
*   **Solution**: The high-level architectural strategy.
*   **Implementation**: Snippets and links to code.
*   **Resulting Context**: The new state, trade-offs, and next steps.

## Getting Started

1.  **Environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    playwright install chromium
    ```
2.  **Run Tests**:
    ```bash
    pytest tests/patterns
    ```

## Creating a Pull Request

1.  Create a branch (`git checkout -b feat/my-pattern`).
2.  Implement the code, example, and test.
3.  Write the narrative documentation in `docs/patterns/`.
4.  Ensure `pre-commit run --all-files` passes.
5.  Open a PR with a description of the "Forces" your pattern addresses.
