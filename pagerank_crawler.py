import sys

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from html.parser import HTMLParser
from urllib.request import urlopen
from urllib import parse


def main(argv):
    try:
        url, depth = process_args(argv)
    except:
        return

    pass


def print_usage():
    with open('usage.txt', 'r') as usage:
        print(usage.read())


def is_valid_url(str):
    val = URLValidator()
    try:
        val(str)
    except ValidationError:
        return False
    return True


def process_args(argv):
    if len(argv) < 3:
        print_usage()
        raise AssertionError

    url = argv[1]
    if not is_valid_url(url):
        print("'{}' is not a valid URL.".format(url))
        raise AssertionError

    try:
        depth = int(argv[2])
    except ValueError:
        print("'{}' is not an integer.".format(argv[2]))
        raise AssertionError

    return url, depth


if __name__ == "__main__":
    main(sys.argv)