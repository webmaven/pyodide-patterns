# Console Log Capturing

## Context
Pyodide applications run in the browser, where standard Python `print()` statements are redirected to the browser's JavaScript console. When writing automated tests, it is often necessary to verify that specific logs were produced (e.g., for debugging or audit trails).

## Problem
In a standard Playwright test, console logs are "emitted" by the browser but are not automatically captured or associated with the test runner's output. If a test fails, you cannot see the browser's logs without manually opening a browser window.

## Forces
*   **Asynchronicity**: Logs can be emitted at any time during the test lifecycle.
*   **Verbosity**: Browsers produce many logs (CSS warnings, network info) that may be irrelevant to the test.
*   **Standard Output**: Developers expect Python `print()` statements to appear in their test reports.

## Solution
Use Playwright's **Event Listeners** to subscribe to the `console` event. Collect these messages into a local list that can be asserted against or printed to stdout upon test failure.

## Implementation

### Capturing Logs in a Test
```python
def test_with_logs(page: Page, http_server):
    logs = []
    page.on("console", lambda msg: logs.append(msg.text))

    page.goto(f"{http_server}/index.html")

    # Perform actions...

    # Assert against logs
    assert any("Pyodide loaded" in log for log in logs)

    # Optional: Print all logs on failure
    # (Pytest will capture this output and show it if the test fails)
    print("
Browser Console Logs:")
    for log in logs:
        print(log)
```

## Resulting Context
*   **Pros**: Provides full visibility into the browser's state during headless testing. Allows for "log-based testing" where you verify system state via internal signals.
*   **Cons**: Can lead to noisy test output if the application is extremely chatty.

## Verification
*   **Test**: `tests/patterns/architectural/test_console_logs.py`
*   **E2E Example**: `tests/patterns/testing/test_e2e.py`
