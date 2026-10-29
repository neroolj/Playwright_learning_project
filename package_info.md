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

### Core Components:
- `tests/conftest.py` - Pytest fixtures and configuration
- `generate_auth_data.py` - Script to generate authentication state files
- `pages/product_page.py` - Page Object Model implementation
- `tests/POM_example.py` - Example of Page Object Model usage

### Test Suites:
- `tests/tests_playwright/` - Playwright tests
- `tests/tests_zooplus/` - Zooplus specific tests

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
- pillow>=13.0.0

## Usage

After installation:

1. Set up environment variables in a `.env` file
2. Install Playwright browsers: `playwright install`
3. Run tests: `pytest`

The package includes an entry point to generate authentication data:
```bash
install-playwright
```