# Playwright Test Project Package Structure

## Files Included

### Core Package Files:
- `setup.py` - Traditional Python package setup script
- `pyproject.toml` - Modern Python packaging configuration  
- `README.md` - Project documentation
- `requirements.txt` - Requirements file for pip installation
- `test_package.py` - Test script to verify package structure

### Configuration Files:
- `pytest.ini` - Pytest configuration
- `.env` - Environment variables template (not committed to git)
- `.gitignore` - Git ignore rules
- `.codex/agents` - Configuration for Codex subagents
- `.github/workflows/tests.yml` - Configuration for Github Actions


### Core Components:
- `pages/` - Page Object Model implementation for test examples
- `conftest.py` - Pytest config, pytest hooks, and pytest fixtures for global usage
- `tests/conftest.py` - Pytest fixtures shared for all tests


### Test Suites:
- `tests/tests_playwright_examples/` - Playwright tests examples and specific pytest fixtures for this set of tests
- `tests/tests_zooplus/` - Tests implementation for real complex website and specific pytest fixtures for this set of tests

## Installation

Users can install this package in development mode:

```bash
pip install -e .
```

This will automatically install all dependencies including:
- pytest>=7.0.0
- playwright>=1.40.0  
- pytest-playwright>=0.3.0
- python-dotenv>=0.19.0
- allure-pytest>=2.16.2
- pillow>=13.0.0
- rich>=15.0.0

## Usage

After installation:

1. Set up environment variables in a `.env` file
2. Install Playwright browsers: `playwright install`
3. Run tests: `pytest`