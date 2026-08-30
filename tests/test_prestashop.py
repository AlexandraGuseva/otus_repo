import time

def test_title(browser):
    browser.get('http://localhost:8080/')
    time.sleep(5)
    assert 'PrestaShop' in browser.title