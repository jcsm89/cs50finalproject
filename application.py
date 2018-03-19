from flask import Flask, render_template, request, jsonify
import sqlite3
from helpers import dictionarize

# connect to the movies sql db
conn = sqlite3.connect('movies.db')
c = conn.cursor()

# configure web app
app = Flask(__name__)

# workaround some strange flask related bug
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = False

# define main page route
@app.route("/")
def index():
    return render_template("index.html")

# route for movie info search given the name input in the form
@app.route("/search")
def search():
    name = request.args.get("name")

    cursor = c.execute("SELECT imdb_rating AS rat, poster_url AS poster FROM movies WHERE title=?", (name,))

    # convert output to dictionary
    rows = dictionarize(cursor)[0]

    return jsonify(rows)

@app.route("/autocomplete")
def autocomplete():
    """ search for movies that match query """

    # get argument from the URL
    q = request.args.get("q") + "%"

    # check if argument exists
    if not q:
        raise RuntimeError('No q argument!')

    else:

        # search db for movies corresponding to query
        cursor = c.execute("SELECT title FROM movies WHERE title LIKE ?", (q,))

        # convert output to dictionary
        rows = dictionarize(cursor)

    # print(f"{rows}")

    # return json object of the corresponding places
    return jsonify(rows)
