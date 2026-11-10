# Playwright Test Project

Python browser UI tests built with pytest and Playwright. The suite includes basic Playwright examples, Zooplus scenarios, Page Objects, authenticated browser fixtures, API response mocking, screenshot checks, and Allure reporting.

## Requirements and setup

- Python 3.8 or newer
- Java (required by the Allure command-line report tool)
- The Allure command-line tool

Create and activate a virtual environment, install the project, then install the browser binaries:

```bash
python -m venv .venv
source .venv/bin/activate             # Windows: .venv\Scripts\activate
python -m pip install -e .
playwright install
```

Install Java and the Allure command-line tool using the instructions for your operating system from [Allure Report](https://allurereport.org/docs/install/). `allure-pytest` is installed with the project, but it does not install the separate `allure` command-line tool.

Create a `.env` file in the project root for the test accounts used by the fixtures:

```dotenv
TEST_USER=your_demoblaze_username
TEST_PASS=your_demoblaze_password
ZOOPLUS_USERNAME=your_zooplus_email
ZOOPLUS_PASSWORD=your_zooplus_password
```

Keep real credentials private; `.env` and the generated `.auth_states/` directory are ignored by Git. The session-scoped, autouse `generate_auth_state_demoblaze` fixture runs for every pytest session and creates `.auth_states/test_state.json` if it is missing by logging in to Demoblaze. This means `TEST_USER` and `TEST_PASS` must be set even when running tests that do not use the Demoblaze authenticated page. The Zooplus authenticated context logs in when a test requests `auth_context_zooplus` or `auth_page_zooplus`.

## Running tests

Run the full suite or select tests with normal pytest selectors:

```bash
pytest
pytest tests/tests_playwright/
pytest tests/tests_zooplus/test_shopping_cart.py
pytest -k "visual"
```

`pytest.ini` enables these pytest-playwright options by default:

- `--screenshot=only-on-failure` saves a browser screenshot on failure.
- `--full-page-screenshot` captures the full page for those screenshots.
- `--tracing=retain-on-failure` retains a Playwright trace on failure.

Override a default option by passing its replacement on the command line, for example `pytest --screenshot=off`. Other pytest-playwright options such as browser selection are available, for example `pytest --browser firefox` (after installing that browser with `playwright install firefox`).

### Test execution timing

The custom `--time` option prints each test's duration and a session summary. Pytest captures output by default, so use `-s` to display the timing as the run progresses:

```bash
pytest --time -s
```

### Allure reports

Tests use Allure labels such as epic, feature, and severity, and `allure.step(...)` to group actions. When a test fails during its call phase, the project hook also attaches a full-page PNG screenshot to the Allure result when it can find the test's `page`, `auth_page_test`, or `auth_page_zooplus` fixture.

Write raw results to a directory, then serve the report locally:

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

`allure serve` builds a temporary report and opens it in a browser. To generate a persistent report directory instead, run `allure generate allure-results --clean -o allure-report`, then open it with `allure open allure-report`. The Allure CLI and Java must be installed for these commands.

### Visual screenshot checks

The visual tests in `tests/tests_playwright/test_screenshot.py` compare current Demoblaze screenshots to baseline images under `screenshots/demoblaze/`. Generate or replace those baselines by running the visual tests with `--gen-screenshots`:

```bash
pytest tests/tests_playwright/test_screenshot.py --gen-screenshots
```

In generation mode the tests save the baseline and skip the comparison. Review and keep the generated baseline changes when the visual appearance change is expected. Without that option, the tests create `*_current.png` images and compare them against the baselines; a missing baseline fails with instructions to generate one.

The `compare_images` fixture returns a comparison function:

```python
def test_visual(page, compare_images):
    page.screenshot(path="current.png")
    assert compare_images("baseline.png", "current.png", 98)
```

Its optional third argument is the minimum percentage of identical pixels (default `95`). Different image dimensions raise `AssertionError`; otherwise, the function returns `True` when the threshold is met and `False` when it is not. The helper requires Pillow, which is installed as a project dependency.

## Project fixtures and structure

- `tests/conftest.py` contains shared fixtures and pytest hooks.
- `page` is provided by pytest-playwright.
- `zooplus_homepage` opens the Zooplus homepage and accepts necessary cookies.
- `auth_context_zooplus` creates a session-scoped signed-in Zooplus browser context; `auth_page_zooplus` creates and closes a page in that context.
- `auth_page_test` creates a Demoblaze page using the saved storage state.
- `product_page`, `zooplus_homepage_pom`, `zooplus_loginpage_pom`, and `zooplus_dryfoodpage_pom` provide Page Objects.
- `mock_backend_error` registers a route mock that fulfills a matching request with a selected error status and JSON error message. Supported statuses are 400, 401, 403, 404, 500, 503, and 504.
- `compare_images` performs the pixel comparison described above.
- `tests/tests_playwright/` contains Playwright examples and visual tests.
- `tests/tests_zooplus/` contains Zooplus UI and API-error scenarios.
- `pages/` contains Page Object classes.
- `screenshots/` contains screenshot examples and visual baselines.

## Dependencies

Project dependencies are declared in `pyproject.toml` and include pytest, Playwright, pytest-playwright, python-dotenv, allure-pytest, Pillow, and Rich. Install optional development tools with `python -m pip install -e ".[dev]"`.
