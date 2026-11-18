"""Global configuration, pytest hooks and global fixtures"""

import pytest
import allure
import time
import os
from rich import print
from playwright.sync_api import Page
from config import timestamp_format


def pytest_addoption(parser):
    """Register new CLIs"""
    # CLI for screenshot generation
    parser.addoption(
        '--gen-screenshots',
        action='store_true',
        default=False,
        help='Generate screenshots for playwright tests'
    )
    # CLI for printing execution time
    parser.addoption(
        '--time',
        action='store_true',
        help='Adds execution time into output. Works only with --capture=no (-s)'
    )
    parser.addoption(
        '--env',
        action='store',
        default='prod',
        choices=['dev', 'stage', 'prod'],
        help='Set environment to run tests against: dev, stage, prod. Default value is prod'
    )


def pytest_configure(config):
    """Save selected --env value into environment variable to use it for right URL selection"""
    os.environ['TEST_ENV'] = config.getoption('--env')


def pytest_report_header(config):
    """Adds some additional info into pytest header"""
    mode = 'screenshot generation' if config.getoption('--gen-screenshots') else 'test'
    return [
        f'environment: {config.getoption('--env')}',
        f'mode: {mode}',
        f'timestamp: {time.strftime('%d %b %X', time.localtime())}',
    ]


def pytest_collection_modifyitems(config, items):
    """Manages tests and leaves only tests marked with 'visual'
    in case if pytest is started in screenshot generation mode"""
    if config.getoption("--gen-screenshots"):
        selected = []
        deselected = []

        for item in items:
            if item.get_closest_marker("visual"):
                selected.append(item)
            else:
                deselected.append(item)

        items[:] = selected
        config.hook.pytest_deselected(items=deselected)


@pytest.hookimpl(hookwrapper=True)
def pytest_fixture_setup(fixturedef, request):
    """Record diagnostics for every Page returned by a test fixture."""
    # Let pytest create the fixture before inspecting its returned value
    outcome = yield

    # Stop hook execution if fixture has failed
    if outcome.excinfo is not None:
        return

    # save fixture result
    page = outcome.get_result()

    # Check if fixture result is page object
    if isinstance(page, Page):
        # Install listeners once per page, even if multiple fixtures return it
        if not hasattr(page, '_console_errors'):
            page._console_errors = []
            page._failed_requests = []

            # Start browser console listener which saves errors into _console_errors
            page.on('console',
                lambda msg: page._console_errors.append(
                    f'[{time.strftime(timestamp_format, time.localtime())}] '
                    f'[{msg.type}]: {msg.text}'
                ) if msg.type == 'error' else None
            )

            # Start listener which saves HTTP error responses (HTTP code 400 or higher)
            page.on(
                'response',
                lambda resp: page._failed_requests.append(
                    f'[{time.strftime(timestamp_format, time.localtime())}] '
                    f'METHOD: {resp.request.method} | URL: {resp.url} '
                    f'| STATUS: {resp.status}\n'
                ) if resp.status >= 400 else None
            )

            # Start listener which saves HTTP requests that fail at transport level
            page.on(
                'requestfailed',
                lambda req: page._failed_requests.append(
                    f'[{time.strftime(timestamp_format, time.localtime())}] '
                    f'METHOD: {req.method} | URL: {req.url} '
                    f'| ERROR: {req.failure}\n'
                )
            )

        # Save each unique page so the pytest_runtest_makereport hook can attach its logs on failure.
        pages = getattr(request.node, '_diagnostic_pages', [])
        if all(existing_page is not page for existing_page in pages):
            pages.append(page)
        request.node._diagnostic_pages = pages



@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Collect and attach logs and screenshot to Allure report if test failed"""""

    # save test result which is sent by Pytest via .send() method
    outcome = yield

    # extract result
    report = outcome.get_result()

    # check if we are on executing stage and test failed
    if report.when == "call" and report.failed:

        # Include pages returned by fixtures (including custom auth fixtures).
        pages = list(getattr(item, '_diagnostic_pages', []))
        for fixture_name in ('page', 'auth_page_test', 'auth_page_zooplus'):
            candidate = item.funcargs.get(fixture_name)
            if isinstance(candidate, Page) and all(candidate is not p for p in pages):
                pages.append(candidate)

        # Attach screenshot and collected browser diagnostics for each page.
        for index, page in enumerate(pages, start=1):
            allure.attach(
                page.screenshot(full_page=True),
                name="Screenshot" if index == 1 else f"Screenshot ({index})",
                attachment_type=allure.attachment_type.PNG
            )

            console_errors = getattr(page, '_console_errors', [])
            if console_errors:
                allure.attach(
                    '\n'.join(console_errors),
                    name=f"Browser console errors ({index})",
                    attachment_type=allure.attachment_type.TEXT
                )

            failed_requests = getattr(page, '_failed_requests', [])
            if failed_requests:
                allure.attach(
                    '\n'.join(failed_requests),
                    name=f"Failed API requests ({index})",
                    attachment_type=allure.attachment_type.TEXT
                )


@pytest.fixture(autouse=True)
def time_function_scope(pytestconfig):
    """Report test durations after each function into STDOUT if pytest started with --time CLI"""
    if pytestconfig.getoption('--time'):
        start = time.time()
    yield
    if pytestconfig.getoption('--time'):
        stop = time.time()
        delta = stop - start
        print(f'\n[yellow]test duration[/yellow] : {delta:0.3} seconds')


@pytest.fixture(autouse=True, scope='session')
def time_session_scope(pytestconfig):
    """Report the time at the end of a session into STDOUT if pytest started with --time CLI"""
    if pytestconfig.getoption('--time'):
        start = time.time()
    yield
    if pytestconfig.getoption('--time'):
        now = time.time()
        delta = now - start
        print(f'\n[yellow]{'-'*30}[/yellow]')
        print(f'[yellow]Total duration[/yellow] : {delta:0.3} seconds')
        print(f"[yellow]Started[/yellow] : {time.strftime(timestamp_format, time.localtime(start))}")
        print(f"[yellow]Finished[/yellow] : {time.strftime(timestamp_format, time.localtime(now))}")
        print(f'[yellow]{'-'*30}[/yellow]')
