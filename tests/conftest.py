import os

import pytest

@pytest.fixture(scope='session')
def ngrok_bin():
    return '/tmp/bin/ngrok'

@pytest.fixture(scope='session')
def splinter_driver_kwargs(splinter_webdriver, splinter_driver_kwargs):
    if splinter_webdriver == 'chrome':
        from selenium import webdriver
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        # https://stackoverflow.com/questions/50642308/webdriverexception-unknown-error-devtoolsactiveport-file-doesnt-exist-while-t
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        splinter_driver_kwargs['options'] = chrome_options
    return splinter_driver_kwargs


@pytest.fixture(scope='session')
def splinter_webdriver(request):
    return request.config.option.splinter_webdriver or 'chrome'


@pytest.fixture(scope='session')
def splinter_webdriver_executable(request, splinter_webdriver):
    """Webdriver executable directory."""
    executable = request.config.option.splinter_webdriver_executable
    if not executable and splinter_webdriver == 'chrome':
        from chromedriver_binary import chromedriver_filename
        executable = chromedriver_filename
    return os.path.abspath(executable) if executable else None


@pytest.fixture(scope='session')
def splinter_window_size(splinter_webdriver, splinter_window_size):
    """
    Prevent pytest-splinter from crashing with Chrome.

    """
    if splinter_webdriver == 'chrome':
        return None

    return splinter_window_size


def pytest_addoption(parser):
    parser.addoption(
        '--skip-webtest',
        action='store_true',
        dest="skip_webtest",
        default=False,
        help="skip marked webtest tests")


def pytest_configure(config):
    mark_expr = []

    if config.option.markexpr:
        mark_expr.append(config.option.markexpr)

    if config.option.skip_webtest:
        mark_expr.append('not webtest')
    if mark_expr:
        setattr(config.option, 'markexpr', ' and '.join(mark_expr))
