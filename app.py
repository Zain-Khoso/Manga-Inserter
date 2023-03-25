#! python3
# app.py - This is the __main__ program file.

import os, sys, shelve
from time import time
from scraper import Scraper
from dbClient import Client


def main():
    # The Shelf keywords.
    shelfCMDS = ["add", "delete", "list"]

    # The Database keywords.
    databaseCMDS = ["insert", "drop"]

    # Handling the shelf queries.
    if sys.argv[1].lower() in shelfCMDS:
        shelfCommandsProcesses()
        return None

    # Handling the database queries.
    if sys.argv[1].lower() in databaseCMDS:
        databaseCommandsProcesses()
        return None

    print("Syntax Error: Please use one of the keywords;")
    print("\t1. add")
    print("\t2. delete")
    print("\t3. list")
    print("\t4. insert")
    print("\t5. drop")

    return None


def shelfCommandsProcesses():
    # Creating the Shelf Directory.
    os.makedirs("Shelfs", exist_ok=True)

    try:
        # Opening the URLs Shelf
        shelf = shelve.open(os.path.join("Shelfs", "URLsShelf"))

        match sys.argv[1].lower():
            # If the user wants to add a manga URL.
            case "add":
                shelf[sys.argv[2]] = sys.argv[3]
                print("Added %s." % sys.argv[2])

            # If the user wants to get a list of the availiable manga URLs
            case "list":
                # If the user has no downloaders
                if len(shelf.keys()) == 0:
                    print("You have no downloaders.")

                for index, key in enumerate(shelf.keys()):
                    print(f"\n{index+1}. {key}")

            # If the user wants to delete manga URLs.
            case "delete":
                # If the user wants to delete a particular manga URL.
                if len(sys.argv) >= 3:
                    if sys.argv[2] in shelf.keys():
                        del shelf[sys.argv[2]]
                        print("%s has been removed from the Shelf." % sys.argv[2])
                    else:
                        print("You have no downloader for %s" % sys.argv[2])
                else:
                    # If the user wants to delete all the manga URLs.
                    shelf.clear()
                    print("The Shelf has been cleared.")

        # Closing the URLs Shelf
        shelf.close()

    except IndexError:
        print("\n\nPlease use the correct syntax: ")
        print("\nadd <manga-name> <manga-URL> : To add a new manga in the shelf")
        print("\nlist : To get a list of all the availiable manga URLs.")
        print("\ndelete <manga-name> : To delete a particular manga")
        print("\ndelete : To delete every URL in the shelf")


def databaseCommandsProcesses():
    # Creating a Client Instance that will be working with our Database.
    mangaClient = Client()

    match sys.argv[1]:
        case "insert":
            # Opening the URL shelf.
            URLsShelf = shelve.open(os.path.join("Shelfs", "URLsShelf"))

            # If the user wants to download an unregistered manga.
            if sys.argv[2] not in URLsShelf.keys():
                print("You don't currently have a downloader for %s" % sys.argv[2])

                return None

            # Getting the manga Name and URL from the command-line-arguments.
            mangaName, mangaURL = sys.argv[2], URLsShelf[sys.argv[2]]

            # Scraping through https://tcbscans.org for the manga.
            mangaData = Scraper(mangaURL).scrape()

            # Inserting the mangaDATA in the Database.
            mangaClient.insert(mangaName, mangaData)

            # CLosing the URLs Shelf.
            URLsShelf.close()

        case "drop":
            # Getting the manga name from the command-line-arguments.
            mangaName = sys.argv[2]

            # Dropping the specified collection.
            mangaClient.drop(mangaName)


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
