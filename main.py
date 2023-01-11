from src.scrap import WebScrap
from src.utils import get_products_data, argument_parser

# import logging


def main():

    walmart_site = "https://www.bestbuy.ca/en-ca/category/ps5-consoles/17583383"
    args = argument_parser()
    products_dict = WebScrap(walmart_site).run()
    scrapped_data = get_products_data(products_dict)


if __name__ == "__main__":
    main()
