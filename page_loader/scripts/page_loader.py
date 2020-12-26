from page_loader.cli import take_apart_params
from page_loader.page_loader import download


def main():
    args = take_apart_params()
    download(args.url, args.output)


if __name__ == "__main__":
    main()
