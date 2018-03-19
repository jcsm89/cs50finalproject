import sqlite3
import csv

# poster link prefix
POSTER_PREFIX = 'https://image.tmdb.org/t/p/original'

# auxiliary variables for company name parsing
COMPANY_PREFIX = "'name': '"
COMPANY_SUFFIX = ","

# connect to the movies sql db
conn = sqlite3.connect('movies.db')
c = conn.cursor()

# open csv file containing movie data
with open('movies_db/movies_metadata.csv') as csv_movies:

    # read file to dictionary, for easy access to each row's data
    reader = csv.DictReader(csv_movies)

    # extract info of interest for each row
    for row in reader:

        try:
            title = row["title"]
            imdb_rating = row["vote_average"]

            # check for movies with no poster
            if not(row["poster_path"]):
                poster_url = row["poster_path"]
            else:
                poster_url = POSTER_PREFIX + row["poster_path"]

            # company name is parsed as string, need to correct it
            aux_company = row["production_companies"]

            # check for movies with no COMPANY_PREFIX
            if not(aux_company):
                company = aux_company
            else:
                company = aux_company[aux_company.find(COMPANY_PREFIX) + len(COMPANY_PREFIX): aux_company.find(COMPANY_SUFFIX) - len(COMPANY_SUFFIX)]

            # db schema for now:
            # CREATE TABLE 'movies' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'title' TEXT NOT NULL, 'imdb_rating' REAL, 'poster_url' TEXT, 'company' TEXT)

            # Insert a row of data
            c.execute("INSERT INTO movies(title, imdb_rating, company, poster_url) VALUES (?, ?, ?, ?)",
                       (title, imdb_rating, company, poster_url) )

            # commit the changes
            conn.commit()

        except:
            # if some unexpected error is presented to sqlite3 pass to the next movie
            pass

# close connection to db
conn.close()
