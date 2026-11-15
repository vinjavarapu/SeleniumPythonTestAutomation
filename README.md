# SauceDemo UI Automation

Python/Selenium end-to-end coverage for the authentication, inventory, cart, and
checkout scenarios in the supplied test-case document. The suite uses pytest,
page objects, explicit waits, isolated browser sessions, and failure screenshots.

## Requirements

- Python 3.12 or newer
- Chrome (default) or Firefox
- Network access to the configured SauceDemo environment

Selenium Manager resolves the matching browser driver automatically.

## Setup

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

## Run tests

```powershell
python -m pytest
python -m pytest -m smoke
python -m pytest --browser firefox
python -m pytest --headed
python -m pytest --base-url https://www.saucedemo.com
```

The default browser is headless Chrome. `--headed` runs a visible browser.
Available options are `--browser chrome|firefox`, `--base-url URL`, and
`--wait-seconds SECONDS`.

The corresponding environment variables are `SAUCEDEMO_BROWSER`,
`SAUCEDEMO_HEADLESS`, `SAUCEDEMO_BASE_URL`, and `SAUCEDEMO_WAIT_SECONDS`.
`SAUCEDEMO_USERNAME` and `SAUCEDEMO_PASSWORD` configure the standard test user;
the public SauceDemo sample account is used when they are not set. Do not store
real credentials in source control.

## Reports and quality checks

Failed test calls save browser screenshots under `test-results/screenshots/`.
CI also writes a JUnit report to `test-results/junit.xml` and uploads the
test-results directory as a workflow artifact.

```powershell
ruff check .
ruff format --check .
```

The pytest configuration limits collection to `tests/`, so unrelated scripts
at the repository root are not executed as part of this test suite.
