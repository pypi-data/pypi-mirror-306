import argparse
import sys
from . import fcopy


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file1", help="source file")
    parser.add_argument("file2", help="destination file") # noqa
    args = parser.parse_args()
    fcopy.fc(args.file1, args.file2)


if __name__ == '__main__':
    main()
    sys.exit(0)
