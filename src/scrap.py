from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
import time


class WebScrap:
    def __init__(self, web_url):
        self.web_url = web_url

        chrome_options = Options()
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--allow-running-insecure-content")
        user_agent = (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"
        )
        chrome_options.add_argument(f"user-agent={user_agent}")
        driver_path = ChromeDriverManager().install()
        self.driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)

        self.product_info = {}

        self.driver.get(web_url)

    def wait_until_element_exist(self, locator, loc_text):
        WebDriverWait(self.driver, 50, ignored_exceptions=StaleElementReferenceException).until(EC.presence_of_element_located((locator, loc_text)))
        # except TimeoutError:
            # return False
        # return True

    def check_exists(self, locator, loc_text):
        try:
            return self.get_element(locator, loc_text, method="first")
        except NoSuchElementException:
            return False

    def get_element(self, locator, loc_text, method="first"):
        if method == "all":
            return self.driver.find_elements(locator, loc_text)
        elif method == "first":
            return self.driver.find_element(locator, loc_text)

    def home_page(self):
        self.wait_until_element_exist(By.CLASS_NAME, "productList_31W-E")

        product_container = self.get_element(By.CLASS_NAME, "productList_31W-E", method="first")
        links = product_container.find_elements(By.CLASS_NAME, "link_3hcyN")
        links = [link.get_attribute("href") for link in links]

        return links

    def parse_link(self, link):
        self.driver.get(link)

        self.wait_until_element_exist(By.CLASS_NAME, "productName_2KoPa")
        product_name = self.get_element(By.CLASS_NAME, "productName_2KoPa", method="first").text
        button1 = self.check_exists(By.LINK_TEXT, "Check other stores")
        if not button1:
            return False

        button1.click()

        self.product_info[product_name] = {}
        self.product_info[product_name]["link"] = link

        return product_name

    def input_postal_code(self, post_code="R2M"):
        self.wait_until_element_exist(By.CLASS_NAME, "formItem_QE5m9")

        form = self.get_element(By.CLASS_NAME, "formItem_QE5m9", method="first")
        postal_code = form.find_element(By.ID, "postalCode")
        button_xpath = "//*[@id='root']/div/div[3]/div/div/div/div[3]/div[2]/div/div/button[1]"
        self.wait_until_element_exist(By.XPATH, button_xpath)
        postal_code.send_keys(post_code)
        self.get_element(By.XPATH, button_xpath).click()
        # time.sleep(5)

    def get_store_lists(self):
        self.wait_until_element_exist(By.CLASS_NAME, "storeListItem_3piwR")

        button_see_more = "//*[@id='root']/div/div[3]/div/div/div/div[4]/div/div[2]/div/button"
        while self.check_exists(By.XPATH, button_see_more):
            self.get_element(By.XPATH, button_see_more).click()

        store_lists = self.get_element(By.CLASS_NAME, "storeListItem_3piwR", method="all")

        return store_lists

    def availability(self, store):
        self.wait_until_element_exist(By.CLASS_NAME, "name_1zPVg")
        store_name = store.find_element(By.CLASS_NAME, "name_1zPVg").text
        self.driver.get_screenshot_as_file("screenshot.png")
        self.wait_until_element_exist(By.CLASS_NAME, "availabilityMessage_1waQP")
        status = store.find_element(By.CLASS_NAME, "availabilityMessage_1waQP").text

        return store_name, status

    def run(self):
        links = self.home_page()
        for link in links:
            product_ = self.parse_link(link)

            if not product_:
                continue

            self.input_postal_code()
            self.product_info[product_]["price"] = self.driver.find_element(
                By.XPATH,
                "//*[@id='root']/div/div[3]/div/div/div/div[2]/a/div/div/div[2]/div[3]/span/div/div",
            ).text
            stores = self.get_store_lists()

            for store in stores:
                store_name, status = self.availability(store)
                self.product_info[product_][store_name] = status
        self.driver.quit()

        return self.product_info
