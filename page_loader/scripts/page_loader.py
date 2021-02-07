import sys
import logging
from page_loader.cli import take_apart_params
from page_loader.page_loader import download


def main():
    # Config logger
    logger = logging.getLogger('main')
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler('loader.log')
    fh.setLevel(logging.INFO)
    fmtstr = '[%(asctime)s] [%(name)s] [%(levelname)s] => %(message)s'
    fmtdate = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(fmtstr, fmtdate)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    # Get command line args
    args = take_apart_params()
    # Start download
    logger.info('=' * 50)
    logger.info('START page download')
    try:
        path_local_html = download(args.url, args.output)
        logger.info('Download of page was COMPLETED')
        print(path_local_html)
    except Exception:
        logger.error(f'Loader error! Loading {args.url} was fail.')
        sys.stderr.write(f'\nGet error: {sys.exc_info()[1]}\n')
        sys.exit(1)


if __name__ == "__main__":
    main()
