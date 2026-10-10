#!/usr/bin/env python3
"""
Test script to verify the package installation and basic functionality.
"""
import os
import sys

def test_package_structure():
    """Verify that all required files are present"""
    required_files = [
        'setup.py',
        'pyproject.toml',
        'README.md',
        'requirements.txt',
        'conftest.py',
        'generate_auth_data.py',
        'pytest.ini',
        '.env',
        'pages/product_page.py',
        'tests_playwright/test_example.py'
    ]

    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)

    if missing_files:
        print(f"Missing files: {missing_files}")
        return False
    else:
        print("All required files are present")
        return True

if __name__ == "__main__":
    success = test_package_structure()
    sys.exit(0 if success else 1)