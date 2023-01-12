import pandas as pd

from src.email_update import EmailUpdate

class Products:

    def __init__(self, products_dict) -> None:
        self.prods = products_dict

    def modify_and_save_data(self):
        scrapped_info_df = pd.DataFrame(self.prods)
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
        self.products_df = df_mod.melt(
            id_vars=other_cols,
            value_vars=loc_cols,
            value_name="status",
            var_name="location",
        )
        self.products_df.to_csv("scrapped_data.csv", index=False)

    def get_available_prods(self):
        # if "Out of Stock" not in self.products_df['status']:
        available_prods = self.products_df[self.products_df['status'] != "Out of Stock"]
        if available_prods.empty:
            return pd.DataFrame()
        return available_prods

    def email_stock_info(self, email, password):
        self.modify_and_save_data()
        available_prods_df = self.get_available_prods()
        if not available_prods_df.empty:
            EmailUpdate(available_prods_df, email, password).send()
        