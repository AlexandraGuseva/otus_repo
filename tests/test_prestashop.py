import time


def test_title(browser, base_url):
    browser.get(base_url + "/")
    time.sleep(5)
    assert 'PrestaShop' in browser.title
