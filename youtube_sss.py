import os
from argparse import ArgumentParser

from webdriver_setup import get_webdriver_for

from config import logger
from search_page import SearchPage


def get_arg_parser():
    """Get argument parser

    :rtype: ArgumentParser
    :returns: ArgumentParser object
    """

    arg_parser = ArgumentParser()
    arg_parser.add_argument("-q", "--query", help="Search query")
    arg_parser.add_argument("-b", "--browser", default="firefox",
                            help="Browser to use")

    return arg_parser


def main():

    arg_parser = get_arg_parser()
    args = arg_parser.parse_args()

    if not args.query:
        logger.error("Run with search query!")
        raise SystemExit()

    # disable WDM logs
    os.environ["WDM_LOG_LEVEL"] = "0"

    try:
        driver = get_webdriver_for(args.browser)
    except ValueError as err:
        logger.error(err)
        raise SystemExit()

    search_page = SearchPage(driver)
    search_page.search_for_query(args.query)

    # close the browser
    driver.quit()


if __name__ == "__main__":

    main()
