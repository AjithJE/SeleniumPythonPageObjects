import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pytest
from webdriver_manager.firefox import GeckoDriverManager

from Utilities import configReader


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture()
def log_on_failure(request, get_browser):
    yield
    item = request.node
    driver = get_browser
    if item.rep_call.failed:
        allure.attach(driver.get_screenshot_as_png(), name="dologin", attachment_type=AttachmentType.PNG)


@pytest.fixture(params=["chrome", "firefox"], scope="function")
def get_browser(request):
    global driver
    if request.param == "chrome":
        driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    if request.param == "firefox":
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    request.cls.driver = driver
    driver.get(configReader.readConfig("basic info", "testsiteurl"))
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()
