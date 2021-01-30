import logging
from page_loader.cli import take_apart_params
from page_loader.page_loader import download


def main():
    logger = logging.getLogger('main')
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler('loader.log')
    fh.setLevel(logging.INFO)
    fmtstr = '[%(asctime)s] [%(name)s] [%(levelname)s] => %(message)s'
    fmtdate = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(fmtstr, fmtdate)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    args = take_apart_params()
    logger.info('=' * 50)
    logger.info('START page download')
    print(download(args.url, args.output))
    logger.info('The download page is COMPLETED')


if __name__ == "__main__":
    main()
