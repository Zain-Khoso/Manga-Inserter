# Manga-Inserter.
#### This application scrapes **tcbscans** to get the requested manga. And stores that data into **MongoDB-Atlas**


## Instalation.

### 1. How to get the source code.
#### Use **git-bash** to download the source code.

### 2. Rename the **app.py** file to **mangaInserter.py**.

### 3. Add the application's root directory in the environment variables.

### 4. How to connect to the __Database__.
#### Create a **.env** file in the application's root directory. Then create two varialbes inside the **.env** file: 
#### A. `atlas_username = <your-username>` 
#### B. `atlas_user_password = <your-password>`


## Usage.

### 1. `mangaInserter.py add <manga-name> <first-chapter-url>`
#### To add a manga in the __downloaders list__.

### 2. `mangaInserter.py list`
#### To get a list of all the availiable downloaders.

### 3. `mangaInserter.py delete <manga-name>`
#### To remove a downloader from the __downloaders list__.

### 4. `mangaInserter.py delete`
#### To clear the downloaders list.

### 5. `mangaInserter.py insert <manga-name>`
#### To insert a particular manga (using one the downloaders in the __downloaders list__) in the **Database**.

### 6. `mangaInserter.py drop <manga-name>`
#### To drop a particular manga collection from the **Database**.