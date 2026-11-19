# Playwright Test Project

Python browser UI automation tests built with pytest and Playwright. The repository contains general Playwright examples, Zooplus scenarios, Page Objects, visual screenshot checks, API response controls, and Allure reporting.

## Requirements and setup

- Python 3.8 or newer
- Playwright browser binaries
- Java and the Allure command-line tool to view Allure reports

Create and activate a virtual environment, install the project, and install the browser binaries:

```bash
python -m venv .venv
source .venv/bin/activate             # Windows: .venv\Scripts\activate
python -m pip install -e .
playwright install
```

Install Java and the Allure command-line tool using the instructions at [Allure Report](https://allurereport.org/docs/install/). `allure-pytest` is installed with the project; the separate `allure` command is needed to build or serve reports.

### Credentials

Create a root `.env` file for the accounts used by the authenticated fixtures:

```dotenv
DEMOBLAZE_USER=your_demoblaze_username
DEMOBLAZE_PASS=your_demoblaze_password
ZOOPLUS_USERNAME=your_zooplus_email
ZOOPLUS_PASSWORD=your_zooplus_password
```

Keep real credentials private. `.env` and `.auth_states/` should not be committed. The session-scoped, autouse `generate_auth_state_demoblaze` fixture creates `.auth_states/test_state.json` if it does not exist, so Demoblaze credentials are required even when selecting tests that do not use the authenticated Demoblaze page. Zooplus credentials are used by its authenticated fixtures. Environment-specific Zooplus URLs, filters, and credentials are defined in `config/zooplus_tests_config.py`; production is selected by default.

## Run tests

```bash
pytest
pytest tests/tests_playwright_examples/
pytest tests/tests_zooplus/test_shopping_cart.py
pytest -k "visual"
```

Select the target configuration with `--env` (`dev`, `stage`, or `prod`; default: `prod`):

```bash
pytest --env stage
pytest --env dev tests/tests_zooplus/
```

The selected value is made available to the configuration package through `TEST_ENV`. The current Zooplus environment configuration supplies URLs and filter labels; credentials for non-production environments are placeholders and need to be configured before using authenticated tests there.

Custom pytest options:

- `--time` prints each test duration and a session summary. Use `-s` to see output during execution: `pytest --time -s`.
- `--gen-screenshots` runs only tests marked `visual`, writes or updates screenshot baselines, and skips their normal image comparisons. Review generated image changes before keeping them.

`pytest.ini` enables these pytest-playwright defaults:

- `--screenshot=only-on-failure`
- `--full-page-screenshot`
- `--tracing=retain-on-failure`

Override a default on the command line, for example `pytest --screenshot=off`. Other pytest-playwright options are available, including `pytest --browser firefox` after installing Firefox with `playwright install firefox`.

The pytest header displays the selected environment, run mode (`test` or `screenshot generation`), and timestamp.

## Allure reports and failure diagnostics

Tests use Allure labels such as epic, feature, and severity, along with `allure.step(...)` to organize actions. Generate and view a report with:

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

To create a persistent report directory instead:

```bash
allure generate allure-results --clean -o allure-report
allure open allure-report
```

When a test fails during its call phase, the global pytest hooks attach a full-page screenshot for each observed page where possible. They also collect browser console errors, HTTP responses with status 400 or higher, and transport-level failed requests, attaching available diagnostics as text to the Allure result. This applies to pages returned by fixtures, including the standard and authenticated page fixtures.

## Fixtures and test helpers

Shared fixtures in `tests/conftest.py` provide:

- `mock_backend_error`: fulfill a matching route with a JSON error response. Supported statuses are 400, 401, 403, 404, 500, 503, and 504.
- `modify_backend_response`: fetch a matching backend response, apply a caller-provided function to its JSON body, and fulfill the route with the modified body.
- `emulate_backend_delay`: delay a matching API route by a specified number of milliseconds.
- `compare_images`: compare two images by pixel differences, with a default minimum similarity of 95%. Different image dimensions raise an assertion error.

Zooplus-specific fixtures in `tests/tests_zooplus/conftest.py` provide cookie-handled and authenticated pages, plus Page Object instances. Playwright example fixtures in `tests/tests_playwright_examples/conftest.py` create Demoblaze authenticated state and a `ProductPage` instance. The built-in pytest-playwright `page` fixture is also used throughout.

## Repository layout

```text
config/                         Environment-aware configuration and shared settings
pages/                          Page Object classes
tests/
  conftest.py                   Shared fixtures and test helpers
  tests_playwright_examples/    Playwright examples, visual tests, and local fixtures
  tests_zooplus/                Zooplus UI/API scenarios and local fixtures
conftest.py                     Pytest options, reporting hooks, diagnostics, and timing
pytest.ini                      Pytest defaults and marker declarations
pyproject.toml                  Project metadata and dependencies
screenshots/                    Screenshot assets and visual baselines, when present
```

The configuration package currently exports `zooplus_config` and `timestamp_format`. The page objects cover Demoblaze product pages and Zooplus home, login, and dry-food pages. Tests exercise common browser interactions, authentication, Zooplus account/cart/login/catalog behavior, API response handling, and visual screenshot workflows.

## Dependencies

Runtime dependencies are declared in `pyproject.toml`: pytest, Playwright, pytest-playwright, python-dotenv, allure-pytest, Pillow, and Rich. Optional development dependencies can be installed with `python -m pip install -e ".[dev]"` when defined in the project metadata.
