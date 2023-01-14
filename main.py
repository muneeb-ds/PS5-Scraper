import os
from datetime import datetime

start = datetime.now()

from src.scrap import WebScrap
from src.products import Products
from src.utils import argument_parser

# import logging

EMAIL = os.environ.get("email")
PASSWORD = os.environ.get("password")

def main():

    walmart_site = "https://www.bestbuy.ca/en-ca/category/ps5-consoles/17583383"
    args = argument_parser()
    products_dict = WebScrap(walmart_site, args.postal_code).run()
    Products(products_dict).email_stock_info(EMAIL, PASSWORD)
    # print(time.time())

if __name__ == "__main__":
    start_time = start.strftime("%H:%M:%S")
    print(start_time)

    main()
    
    end = datetime.now()
    end_time = end.strftime("%H:%M:%S")
    print(end_time)
