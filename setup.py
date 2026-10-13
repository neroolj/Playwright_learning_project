from setuptools import setup, find_packages

setup(
    name="playwright-test-project",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Playwright test project with pytest",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/playwright-test-project",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pytest>=7.0.0",
        "playwright>=1.40.0",
        "pytest-playwright>=0.3.0",
        "python-dotenv>=0.19.0",
        "allure-pytest>=2.16.2"
    ],
    entry_points={
        "console_scripts": [
            "install-playwright=generate_auth_data:main",
        ],
    },
    extras_require={
        "dev": [
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ]
    },
    include_package_data=True,
    package_data={
        "": ["auth_states/*", "screenshots/*", ".env*"],
    },
)