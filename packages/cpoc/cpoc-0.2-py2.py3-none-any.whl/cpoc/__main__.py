import argparse
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file1")
    parser.add_argument("file2")
    args = parser.parse_args()
    print(f"{args.file1} -> {args.file2}")


if __name__ == '__main__':
    main()
    sys.exit(0)
