import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome",
                     help="Выберите браузер: chrome, safari")
    parser.addoption("--headless", action="store_true",
                     help="Запустить браузер в безголовом режиме")
    parser.addoption("--base_url", default="http://localhost:8080",
                     help="Базовый URL тестируемого приложения")


@pytest.fixture
def browser(request):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    base_url = request.config.getoption("--base_url")
    request.config.base_url = base_url

    if browser_name == 'chrome':
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        browser = webdriver.Chrome(options=options)
    elif browser_name == 'safari':
        browser = webdriver.Safari()
    else:
        raise ValueError(f'Неподдерживаемый браузер: {browser_name}')

    browser.maximize_window()
    browser.implicitly_wait(5)

    yield browser
    browser.quit()


@pytest.fixture
def base_url(request):
    return request.config.getoption("--base_url")


@pytest.fixture
def pages(browser, base_url):
    from pages.admin_login_page import AdminLoginPage

    return {
        "administration": AdminLoginPage(browser, base_url),
    }