import sys

from web_crawler import is_valid_url, Crawler
from matrix_generator import generate_from_map
from ranker import rank


def main(argv):
    try:
        url, depth = process_args(argv)
    except AssertionError:
        return

    print("Running crawl on '{}' with depth {}...".format(url, depth))
    crawler = Crawler(url, depth)
    page_map = crawler.get_map()

    print("Generating matrix from page map...")
    matrix, indexes = generate_from_map(page_map)

    print("Ranking pages...")
    rank_map = rank(matrix, indexes)

    print("Printing ranking...")
    i = 1
    for page, score in reversed(sorted(rank_map.items(), key=lambda x: x[1])):
        print("\t[{}]: {}".format(i, page))
        i += 1


def print_usage():
    with open('usage.txt', 'r') as usage:
        print(usage.read())


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
