#! python3
# app.py - This is the __main__ program file.

import os, sys, shelve
from time import time
from scraper import Scraper
from databaseInserter import Inserter


def main():
    # The shelf keywords
    shelfCMDS = ["add", "delete", "list"]

    # The Database commands.
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
        elif sys.argv[1].lower() == "delete" and len(sys.argv) >= 3:
            if sys.argv[2] in shelf.keys():
                del shelf[sys.argv[2]]
                return None
            else:
                print("You have no downloader for %s" % sys.argv[2])

        # If the user wants to delete all the manga URLs.
        elif sys.argv[1].lower() == "delete" and len(sys.argv) >= 2:
            shelf.clear()

        # Closing the URLs Shelf
        shelf.close()

    except IndexError:
        print("\nadd <manga-name> <manga-URL> : To add a new manga in the shelf")
        print("\nlist : To get a list of all the availiable manga URLs.")
        print("\n\nPlease use the correct syntax: ")
        print("\ndelete <manga-name> : To delete a particular manga")
        print("\ndelete : To delete every URL in the shelf")


def databaseCommandsProcesses():
    # Opening the URL shelf.
    URLsShelf = shelve.open(os.path.join("Shelfs", "URLsShelf"))

    if sys.argv[1] == "insert":
        # If the user wants to download an unregistered manga.
        if sys.argv[2] not in URLsShelf.keys():
            print("You don't currently have a downloader for %s" % sys.argv[2])

            return None

        # Setting up the manga Name and URL.
        mangaName, mangaURL = sys.argv[2], URLsShelf[sys.argv[2]]

        # Scraping through https://tcbscans.org for the manga.
        manga = Scraper(mangaURL)
        mangaDATA = manga.scrape()

        # Inserting the mangaDATA in the Database.
        mangaInserter = Inserter(mangaDATA)
        mangaInserter.insert(mangaName)

    else:
        # Imports
        from environs import Env
        from pymongo import MongoClient
        from pymongo.server_api import ServerApi

        # Reading the .env file.
        env = Env()
        env.read_env()

        # Getting the username and password of MongoDB-Atlas User from the .env-file.
        username = env.str("atlas_username")
        password = env.str("atlas_user_password")

        # Creating a client-Obj for the Atlas-Cluster.
        client = MongoClient(
            f"mongodb+srv://{username}:{password}@maincluster.bwozlbo.mongodb.net/?retryWrites=true&w=majority",
            server_api=ServerApi("1"),
        )

        # Selecting a Database inside the cluster.
        database = client["MangaURLs"]

        # Checking if there isn't a collection for the given manga in the database.
        if sys.argv[2] not in database.list_collection_names():
            print("You don't have a collection for %s, in the database." % sys.argv[2])
            return None

        # Selecting the collection.
        collection = database[sys.argv[2]]

        # Droping the collection.
        collection.drop()

        print("%s Collection Dropped." % sys.argv[2])


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
