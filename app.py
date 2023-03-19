#! python3
# app.py - This is the __main__ program file.

import os, sys, shelve
from time import time
from scraper import Scraper


def main():
    # The shelf keywords
    shelfCMDS = ["add", "delete", "list"]

    # Handling the shelf queries.
    if sys.argv[1].lower() in shelfCMDS:
        shelfCommandsProcesses()

        return None

    # Opening the URL shelf.
    URLsShelf = shelve.open(os.path.join("Shelfs", "URLsShelf"))

    # If the user wants download an unregisstered manga.
    if sys.argv[1] not in URLsShelf.keys():
        print("You don't currently have a downloader for %s" % sys.argv[1])
        return None

    # Setting up the manga Name and URL.
    mangaName, mangaURL = sys.argv[1], URLsShelf[sys.argv[1]]

    # Scraping through https://tcbscans.org for the manga.
    manga = Scraper(mangaURL)
    mangaDATA = manga.scrape()


def shelfCommandsProcesses():
    # Creating the Shelf Directory.
    os.makedirs("Shelfs", exist_ok=True)

    try:
        # Opening the URLs Shelf
        shelf = shelve.open(os.path.join("Shelfs", "URLsShelf"))

        # If the user wants to add a manga URL.
        if sys.argv[1].lower() == "add":
            shelf[sys.argv[2]] = sys.argv[3]

        # If the user wants to get a list of the alaliable manga URLs
        elif sys.argv[1].lower() == "list":
            # If the user has no downloaders
            if len(shelf.keys()) == 0:
                print("You have no downloaders.")
                return None

            for index, key in enumerate(shelf.keys()):
                print(f"\n{index+1}. {key}")

        # If the user wants to delete a particular manga URL.
        elif sys.argv[1].lower() == "delete" and len(sys.argv) == 3:
            del shelf[sys.argv[2]]

        # If the user wants to delete all the manga URLs.
        elif sys.argv[1].lower() == "delete" and len(sys.argv) == 2:
            shelf.clear()

        # Closing the URLs Shelf
        shelf.close()

    except IndexError:
        print("\n\nPlease use the correct syntax: ")
        print("\ndelete : To delete every URL in the shelf")
        print("\ndelete <manga-name> : To delete a particular manga")
        print("\nadd <manga-name> <manga-URL> : To add a new manga in the shelf")
        print("\nlist : To get a list of all the availiable manga URLs.")


if __name__ == "__main__":
    # Running the main function and starting the timer.
    try:
        startTime = time()
        main()

    # Checks for KeyboardInterruption.
    except KeyboardInterrupt:
        endTime = time()
        print("\nUser Interruuption.", end="\t")

    # Gets the ending time and print "Done." if there was no error.
    else:
        endTime = time()
        print("\nDone.", end="\t")

    # Weither there was an error or not, prints the total time the program was running.
    finally:
        totalTime = endTime - startTime

        hours, reminder = divmod(totalTime, 3600)
        minutes, seconds = divmod(reminder, 60)

        print(f"Time Taken:  {int(hours):02} : {int(minutes):02} : {round(seconds):02}")
