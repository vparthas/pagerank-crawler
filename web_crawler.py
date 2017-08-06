from html.parser import HTMLParser

from urllib.request import urlopen
from urllib import parse
from urllib.error import HTTPError, URLError

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class LinkParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (key, value) in attrs:
                if key == 'href':
                    newUrl = parse.urljoin(self.baseUrl, value)
                    if not is_valid_url(newUrl):
                        return
                    self.links.append(newUrl)

    # This is a new function that we are creating to get links
    # that our spider() function will call
    def getLinks(self, url):
        response = urlopen(url)

        self.links = []
        self.baseUrl = response.geturl()

        if response.getheader('Content-Type').find('text/html') > -1:
            html_bytes = response.read()

            html_string = html_bytes.decode("utf-8", errors='ignore').strip()

            self.feed(html_string)
            return self.links
        else:
            return None


class Crawler:

    def __init__(self, url, depth):
        self._url = url
        self._depth = depth
        self._map = {}

    def get_map(self):
        dest = urlopen(self._url).geturl()
        self._crawl(dest, 0)
        return self._map

    def _crawl(self, url, depth):
        self._map[url] = {}
        if depth >= self._depth:
            return

        links = LinkParser().getLinks(url)
        if not links:
            return

        for link in links:
            try:
                dest = urlopen(link).geturl()
            except (HTTPError, URLError):
                continue

            if dest == url:
                continue

            self._map[url].setdefault(dest, 0)
            self._map[url][dest] += 1

        for dest in self._map[url].keys():
            visited = dest in self._map.keys()
            if not visited:
                self._crawl(dest, depth + 1)


def is_valid_url(str):
    val = URLValidator()
    try:
        val(str)
    except ValidationError:
        return False
    return True
