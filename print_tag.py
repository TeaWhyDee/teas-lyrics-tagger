import argparse
from typing import List

import music_tag


def parse_arguments():
    parser = argparse.ArgumentParser(description="Print all tags or a specified tag.")

    parser.add_argument("files", nargs="+", help="Path(s) to file(s)")
    parser.add_argument("-t", "--tag", type=str, help="Tag to print")
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Don't print filename"
    )

    args = parser.parse_args()

    return args


def main():
    args = parse_arguments()

    files = args.files
    for filepath in files:
        f = music_tag.load_file(filepath)

        if not args.quiet:
            print(filepath)

        if args.tag:
            try:
                print(f[args.tag])
            except KeyError:
                print(f'Tag "{args.tag}" not found')
        else:
            print(f)


if __name__ == "__main__":
    main()
