# Playwright Test Project

This is a Playwright test project using pytest for automated web testing.

## Features

- End-to-end testing with Playwright
- Test automation with pytest framework
- Page Object Model pattern implementation
- Authentication state management
- Cross-browser testing capabilities

## Installation

### Prerequisites

- Python 3.8 or higher
- Node.js (for Playwright browser installation)
- Allure
- Java

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd playwright-test-project
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package in development mode:
```bash
pip install -e .
```

4. Install Playwright browsers:
```bash
playwright install
```

5. Set up environment variables by creating a `.env` file with your credentials:
```bash
USERNAME=your_email@example.com
PASSWORD=your_password
TEST_USER=test_user
TEST_PASS=test_password
```

## Running Tests

### Run all tests:
```bash
pytest
```

### Run tests with specific options:
```bash
# Run tests with screenshots on failure
pytest --screenshot=only-on-failure

# Run tests with full page screenshots
pytest --full-page-screenshot

# Run tests with tracing
pytest --tracing=retain-on-failure
```

## Project Structure

- `tests/tests_playwright/` - Playwright tests
- `tests/tests_zooplus/` - Zooplus specific tests  
- `pages/` - Page Object Model classes
- `tests/conftest.py` - Pytest fixtures and configuration
- `generate_auth_data.py` - Script to generate authentication state files
- `.env` - Environment variables (not committed to git)

## Dependencies

This project requires the following dependencies:

- pytest
- playwright
- pytest-playwright
- python-dotenv
- allure-pytest

The package will automatically install these when you run `pip install -e .`