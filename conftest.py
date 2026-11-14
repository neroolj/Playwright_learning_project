"""Global configuration, pytest hooks and global fixtures"""

import pytest
import allure
import time
import sys
import os
from rich import print


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
    mode = 'screenshot generation' if config.getoption('--gen-screenshots') else 'test'
    return [
        f'environment: {config.getoption('--env')}',
        f'mode: {mode}',
        f'timestamp: {time.strftime('%d %b %X', time.localtime())}',
    ]


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """This hook collects screenshot and attach it to Allure report if test failed"""""

    # save test result which is sent by Pytest via .send() method
    outcome = yield

    # extract result
    report = outcome.get_result()

    # check if we are on executing stage and test failed
    if report.when == "call" and report.failed:

        # save current page element depending on which fixture is used
        page = item.funcargs.get('page') or item.funcargs.get('auth_page_test') or item.funcargs.get('auth_page_zooplus')

        # if page exists collect screenshot and attach it to Allure report
        if page:
            allure.attach(
                page.screenshot(full_page=True),
                name="Screenshot",
                attachment_type=allure.attachment_type.PNG
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
        print(f"[yellow]Started[/yellow] : {time.strftime('%d %b %X', time.localtime(start))}")
        print(f"[yellow]Finished[/yellow] : {time.strftime('%d %b %X', time.localtime(now))}")
        print(f'[yellow]{'-'*30}[/yellow]')
