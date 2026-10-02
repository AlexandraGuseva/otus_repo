import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
import logging
import allure

# ========== НАСТРОЙКА ЛОГИРОВАНИЯ ==========
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


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

    logger.info(f"Запуск браузера: {browser_name}")

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

    logger.info("Закрытие браузера")
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


# ========== ALLURE: СКРИНШОТЫ ПРИ ПАДЕНИИ ==========
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        if "browser" in item.fixturenames:
            browser = item.funcargs["browser"]
            try:
                screenshot = browser.get_screenshot_as_png()
                allure.attach(
                    screenshot,
                    name="screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
                logger.error(f"Тест {item.name} упал. Скриншот добавлен.")
            except Exception as e:
                logger.error(f"Не удалось сделать скриншот: {e}")