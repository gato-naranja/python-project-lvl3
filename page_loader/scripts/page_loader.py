import sys
import logging

from page_loader.cli import take_apart_params
from page_loader.page_loader import download
from page_loader import logger


def main():
    # Config logger
    logger.setup()
    # Get command line args
    args = take_apart_params()
    # Start download
    logging.info('=' * 50)
    logging.info('START page download')
    try:
        path_local_html = download(args.url, args.output)
        logging.info('Download of page was COMPLETED')
        sys.stdout.write(path_local_html)
        # print(path_local_html)
    except Exception as err:
        logging.error(f'Loader error! Loading {args.url} was fail.')
        sys.stderr.write(f'Get error: {err}\n')
        sys.exit(1)


if __name__ == "__main__":
    main()
