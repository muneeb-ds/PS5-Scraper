import pandas as pd
from argparse import ArgumentParser
from selenium.webdriver.common.by import By

from src.scrap import WebScrap

def get_products_data(product_dict):
    scrapped_info_df = pd.DataFrame(product_dict)
    scrapped_info_df = scrapped_info_df.reset_index()
    df_mod = scrapped_info_df.T
    df_mod.columns = df_mod.iloc[0]
    df_mod = df_mod.reset_index()
    df_mod = df_mod.drop(index=0)
    df_mod = (
        df_mod.reset_index()
        .rename(columns={"index": "product"})
        .drop(columns=["level_0"])
        .set_index(["product", "price"])
        .reset_index()
    )
    loc_cols = df_mod.columns[~df_mod.columns.isin(["product", "price", "link"])]
    other_cols = df_mod.columns[df_mod.columns.isin(["product", "price", "link"])]
    product_info_df = df_mod.melt(
        id_vars=other_cols,
        value_vars=loc_cols,
        value_name="status",
        var_name="location",
    )
    product_info_df.to_csv("scrapped_data.csv", index=False)

    return product_info_df

def argument_parser():
    parser = ArgumentParser(description="input parameters")

    parser.add_argument("--email",
                        help='email on which scrapped data is received')

    parser.add_argument("--postal_code",
                        help = "postal code to check nearby stores")

    args = parser.parse_args()
    return args

def scrap_data(website_url):
    scrap_driver = WebScrap(website_url)

    scrap_driver.wait_until_element_exist(By.CLASS_NAME, "productList_31W-E")

    product_info = {}
    product_container = scrap_driver.get_element(By.CLASS_NAME, "productList_31W-E", method = "first")
    links = product_container.find_elements(By.CLASS_NAME, "link_3hcyN")
    link_text = [link.get_attribute("href") for link in links]

    for link in link_text:
        scrap_driver.driver.get(link)

        scrap_driver.wait_until_element_exist(By.CLASS_NAME, "productName_2KoPa")
        product_name = scrap_driver.get_element(By.CLASS_NAME, "productName_2KoPa", method = "first").text
        button1 = scrap_driver.check_exists(By.LINK_TEXT, "Check other stores")
        if not button1:
            continue

        button1.click()
        scrap_driver.wait_until_element_exist(By.ID, "postalCode")

        postal_code = scrap_driver.get_element(By.ID, "postalCode", method = 'first')
        postal_code.send_keys("R2M")
        button_xpath = "//*[@id='root']/div/div[3]/div/div/div/div[3]/div[2]/div/div/button[1]"
        scrap_driver.wait_until_element_exist(By.XPATH,button_xpath)
        scrap_driver.get_element(
            By.XPATH,
            button_xpath
        ).click()

        scrap_driver.wait_until_element_exist(By.CLASS_NAME, "storeListItem_3piwR")

        button_see_more = (
            "//*[@id='root']/div/div[3]/div/div/div/div[4]/div/div[2]/div/button"
        )
        while scrap_driver.check_exists(By.XPATH, button_see_more):
            scrap_driver.get_element(By.XPATH, button_see_more).click()
        store_lists = scrap_driver.get_element(By.CLASS_NAME, "storeListItem_3piwR", method = 'all')

        product_info[product_name] = {}
        product_info[product_name]["price"] = scrap_driver.driver.find_element(
            By.XPATH,
            "//*[@id='root']/div/div[3]/div/div/div/div[2]/a/div/div/div[2]/div[3]/span/div/div",
        ).text
        product_info[product_name]["link"] = link

        for store in store_lists:
            scrap_driver.wait_until_element_exist(By.CLASS_NAME, "availabilityMessage_1waQP")
            store_name = store.find_element(By.CLASS_NAME, "name_1zPVg").text
            product_info[product_name][store_name] = store.find_element(
                By.CLASS_NAME, "availabilityMessage_1waQP"
            ).text

    scrap_driver.driver.quit()

    return product_info

