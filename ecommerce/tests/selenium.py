import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="module")  # it means it's only created once for the module
def chrome_browser_instance(request):
    options = Options()
    options.headless = False  # enables us see the chrome
    browser = webdriver.Chrome(chrome_options=options)
    yield browser
    browser.close()
