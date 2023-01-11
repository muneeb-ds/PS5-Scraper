from src.utils import get_products_data, argument_parser, scrap_data

# import logging


def main():

    walmart_site = "https://www.bestbuy.ca/en-ca/category/ps5-consoles/17583383"
    args = argument_parser()
    products_dict = scrap_data(walmart_site)
    scrapped_data = get_products_data(products_dict)


if __name__ == "__main__":
    main()
