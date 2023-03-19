# scrper.py - Scrapes https://tcbscans.org for a particular manga and returns the whole manga.

import re, requests as req
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError, HTTPError


class Scraper:
    def __init__(self, firstChapterURL) -> None:
        # URL of the first chapter.
        self.cURL = firstChapterURL

        # Regex for the URL.
        self.URLRegex = self.getURLRegex()

        # Getting the name of the Manga.
        self.mangaName = self.getMangaName()

        # State of the scraper.
        self.running = True

        # List for storing URLs.
        self.STORAGE = []

    def getURLRegex(self):
        # Returns a Regex object to parse the URL.
        return re.compile(
            r"""
            (.*?/)              # Group1 - Root URL of the site.
            (manga/)            # Group2 - "manga"
            (.*?/)              # Group3 - Manga name.
            (
                (.*?-)          # Group5 - "chapter-"
                ((\d|\.)+)      # Group6 - Chapter Number
            )    
            """,
            re.VERBOSE,
        )

    def getMangaName(self):
        # Parsing the URL to get manga name.
        mangaNameWords = self.URLRegex.search(self.cURL).group(3)[:-1].split("-")

        # Apropriat MangaName.
        mangaName = ""

        for word in mangaNameWords:
            mangaName += " %s" % word.capitalize()

        return mangaName.strip()

    def getNextURL(self):
        # Selecting the next btn
        nextBtn = self.DOM.select_one("a.next_page")

        # Getting the next chapter URL.
        if nextBtn == None:
            self.downloading = False
        else:
            self.cURL = nextBtn.get("href")

    def scrape(self):
        # Loops through all the chapters.
        while self.running:
            # Getting the Chapter Number.
            self.chpNum = self.URLRegex.search(self.cURL).group(6)

            # Initializing a place for the current chapter in STORAGE.
            self.STORAGE.append([])

            # Downloading the chapter DOM.
            try:
                res = req.get(self.cURL)
                res.raise_for_status()

            # Handeling Connection or HTTPError.
            except ConnectionError or HTTPError as err:
                print(
                    "Was not able to download Chapter_%s\nAt: %s\nBecause of: %s"
                    % (self.chpNum, self.cURL, err)
                )

            # If there was no Exception.
            else:
                print("Chapter_%s " % self.chpNum, end="")

                # Creating DOM.
                self.DOM = BeautifulSoup(res.text, "lxml")

                # Call to getEveryPagesURL method, which gets the url of all the manga
                # pages in this chapter.
                self.getEveryPagesURL()

            # Weither an error occurs or not.
            finally:
                self.getNextURL()

        return self.STORAGE

    def getEveryPagesURL(self):
        # Selects all the manga-pages.
        pageElems = self.DOM.select("img.wp-manga-chapter-img")

        # Createing threads to download each page.
        for elem in pageElems:
            # Storing the current page URL in the STORAGE.
            self.STORAGE[-1].append(elem.get("src"))

        print("Downloaded.")
