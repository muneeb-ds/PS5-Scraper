from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException


class WebScrap:
    def __init__(self, web_url):
        self.web_url = web_url

        chrome_options = Options()
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--allow-running-insecure-content')
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
        chrome_options.add_argument(f'user-agent={user_agent}')
        driver_path = ChromeDriverManager().install()
        self.driver = webdriver.Chrome(
            service=Service(driver_path), options=chrome_options
        )

        self.driver.get(web_url)

    def wait_until_element_exist(self, locator, loc_text):
        try:
            WebDriverWait(self.driver, 50).until(
                EC.presence_of_element_located((locator, loc_text))
            )
        except TimeoutError:
            return False
        return True

    def check_exists(self, locator, loc_text):
        try:
            return self.get_element(locator, loc_text, method = 'first')
        except NoSuchElementException:
            return False

    def get_element(self, locator, loc_text, method="first"):
        if method == "all":
            return self.driver.find_elements(locator, loc_text)
        elif method == "first":
            return self.driver.find_element(locator, loc_text)
