#!/var/gopher/cgi-bin/venv/bin/python3.7

import os
from sys import stdin
from imdb import IMDb
from pyfiglet import Figlet
from gopher_server.menu import Menu, MenuItem, InfoMenuItem

# Configuration: Change this to your needs
host = "jan.bio"
selector = "/cgi-bin/gmdb.py"
port = 70

def p(str):
    """ Renders a string (possibly containting newlines) to a
    gopher menu item """
    s = str.split("\n")
    for line in s:
        print(InfoMenuItem(line).serialize())

ia = IMDb()

# Print a fancy title:
f = Figlet(font='slant')
logo = f.renderText('GMDb')
for line in logo.split("\n"):
    p("    " + line)

p("         - The Gopher Movie Database\n")
p("# A Gopher connector to the Internet Movie Database\n")
p("Version 0.0.1\n\n")

movie_name = os.environ['SEARCHREQUEST']

if movie_name:
    movies = ia.search_movie(movie_name)
    movie = movies[0]

    if len(movies) == 0:
        p("Movie not found\n\n")
        # TODO: New Search
        exit

    p(" ".join([movie['canonical title'],
    "".join(["(", str(movie['year']), ")"]),
    "".join(['#', movie['kind']])])+"\n")

    ia.update(movie, ['vote details'])
    dem = movie.get('demographics')
    if dem:
        rating = movie.get('demographics')['imdb users']['rating']
        p(" ".join(["Rating: ", int(rating)*"*", str(rating), "/ 10"]))

    p("")
    # Staring
    ia.update(movie, ['full credits'])
    cast = movie.get('cast')
    if cast:
        p("Starring:\n")
        i = 0
        for person in cast:
            if i > 5: break
            p(" - " + person['name'])
            i = i + 1
        if len(cast) > 5:
            p("  [more...]")
    p("\n\n")
    print(MenuItem("1", " Back to main page", selector, host, port).serialize() + "\n\n")
else:
    p("  Welcome to the Gopher Movie Database!")
    p("  Since this is an alpha version, there is not much to see.")
    p("  Right now, this gives you the year, title, rating and some of the actors.\n\n")
    p("  You can search for movies here:\n")

print(MenuItem("7", " New Search", selector, host, port).serialize())
print(MenuItem("1", " Back to jan.bio", "/", host, port).serialize())
