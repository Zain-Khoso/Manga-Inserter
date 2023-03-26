# databaseInserter.py - This file inserts all the img URLS (collected by <scraper.py>) on MongoDB-Atlas.

from environs import Env
from pymongo import MongoClient
from pymongo.server_api import ServerApi


class Client:
    def __init__(self) -> None:
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

        # Creating a Database inside the cluster.
        self.Database = client["MangaURLs"]

    def insert(self, mangaName, URLData) -> None:
        print("\nInsertion Began.\n")
        # Creating a collection for the Manga in the DataBase.
        collection = self.Database[mangaName]

        # The list of all the chapter documents.
        chapters = []

        # Looping through the URLData and adding it to the Collection.
        for chapter in URLData:
            # Getting the chapterImgURLs in appropriate format for insertion in some steps.

            # 1 - The local Chapter Document.
            chapterDict = {}

            # 2 - A default array in the local-Document.
            chapterDict.setdefault("ChapterNum", str(chapter[0]))
            chapterDict.setdefault(f"pages", [])

            # 3 - Adding all the imgURLs in the local-Document.
            for page in chapter[1:]:
                chapterDict[f"pages"].append(page)

            # Appending this chapter document to the list of chapters.
            chapters.append(chapterDict)

        # Inserting the documents to the Database.
        collection.insert_many(chapters)

        print("Insertion Ended.")

    def drop(self, mangaName) -> None:
        # Checking if there isn't a collection for the given manga in the database.
        if mangaName not in self.Database.list_collection_names():
            print("You don't have a collection for %s, in the database." % mangaName)
            return None

        # Selecting the collection.
        collection = self.Database[mangaName]

        # Droping the collection.
        collection.drop()

        print("%s Collection Dropped." % mangaName)
