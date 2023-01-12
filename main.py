from src.scrap import WebScrap
from src.products import Products
from src.utils import argument_parser

# import logging


def main():

    walmart_site = "https://www.bestbuy.ca/en-ca/category/ps5-consoles/17583383"
    args = argument_parser()
    products_dict = WebScrap(walmart_site).run()
    Products(products_dict).email_stock_info(args.email, args.password)


if __name__ == "__main__":
    main()
