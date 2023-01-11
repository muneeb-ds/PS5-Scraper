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

    parser.add_argument("--email", help="email on which scrapped data is received")

    parser.add_argument("--postal_code", help="postal code to check nearby stores")

    args = parser.parse_args()
    return args
