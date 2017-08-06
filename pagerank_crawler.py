import sys
import getopt
import json

from web_crawler import is_valid_url, Crawler
from matrix_generator import generate_from_map
from ranker import rank


def main(argv):
    try:
        url, depth, domain, rankfile, mapfile, matrixfile, crawldata = process_args(argv)
    except AssertionError:
        return

    if not crawldata:
        print("Running crawl on '{}' with depth {} (domain={})...".format(url, depth, domain))
        crawler = Crawler(url, depth, domain)
        page_map = crawler.get_map()
        dump_to_file(mapfile, page_map)
    else:
        print("Loading crawl data from {}...".format(crawldata))
        with open(crawldata, 'r') as datfile:
            page_map = json.load(datfile)

    print("Generating matrix from page map...")
    matrix, indexes = generate_from_map(page_map)
    dump_to_file(matrixfile, {'matrix':matrix.tolist(), 'indexes':indexes})

    print("Ranking pages...")
    rank_map = rank(matrix, indexes)
    dump_to_file(rankfile, rank_map)

    i = 1
    for page, score in reversed(sorted(rank_map.items(), key=lambda x: x[1])):
        print("\t[{}]: {}".format(i, page))
        i += 1


def dump_to_file(path, obj):
    if not path:
        return
    with open(path, 'w') as outf:
        json.dump(obj, outf, indent=4)


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

    domain = False
    rankfile = None
    mapfile = None
    matrixfile = None
    crawldata = None

    try:
        opts, args = getopt.getopt(argv[3:], "", ["domain", "rankfile=", "mapfile=",
                                                    "matrixfile=", "crawldata="])
    except getopt.GetoptError:
        print("Invalid options")
        print_usage()
        raise AssertionError

    for opt, arg in opts:
        if opt == "--domain":
            domain = True
        elif opt == "--rankfile":
            rankfile = arg
        elif opt == "--mapfile":
            mapfile = arg
        elif opt == "--matrixfile":
            matrixfile = arg
        elif opt == "--crawldata":
            crawldata = arg
        else:
            print("Invalid option: '{}'".format(opt))
            print_usage()
            raise AssertionError

    return url, depth, domain, rankfile, mapfile, matrixfile, crawldata


if __name__ == "__main__":
    main(sys.argv)
