from argparse import ArgumentParser

def argument_parser():
    parser = ArgumentParser(description="input parameters")

    parser.add_argument("--email", help="email on which scrapped data is received")
    parser.add_argument("--password", help="password for email")
    parser.add_argument("--postal_code", help="postal code to check nearby stores")
    
    args = parser.parse_args()
    
    return args
