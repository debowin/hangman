"""
Contains the code for building the hangman game database
and adding more entries from IMDB lists.
"""

# TODO Multi Page List Support
import BSXPath
import json
import requests
import sqlite3

__author__ = 'Debojeet_Chatterjee'

HOST = "http://www.omdbapi.com/"
TOP_URL = "http://www.imdb.com/chart/top"  # IMDB Top 250
LIST_URL = "http://www.imdb.com/list/ls071890446/"  # Replace with a URL to any IMDB list.
TOP_MOVIE_XPATH = "//td[@class='titleColumn']"
LIST_MOVIE_XPATH = "//div[@class='hover-over-image zero-z-index']"


def get_movie_list(what):
    """
    returns a list of movie ids
    """
    if what == 'list':
        response = requests.get(LIST_URL)
    else:
        response = requests.get(TOP_URL)
    if response.status_code != 200:
        print 'Check LIST_URL[%s]' % response.status_code
        exit()
    source = response.text.encode('utf-8')
    bsxpath_eval = BSXPath.BSXPathEvaluator(source)
    if what == 'list':
        movie_link_tags = bsxpath_eval.getItemList(LIST_MOVIE_XPATH)
        movie_list = [link_tag['data-const'] for link_tag in movie_link_tags]
    else:
        movie_link_tags = bsxpath_eval.getItemList(TOP_MOVIE_XPATH)
        movie_list = [link_tag.a['href'].split('/')[2] for link_tag in movie_link_tags]
    return movie_list


def create_table_db():
    """
    attempts to create the MOVIES table in the DB.
    """
    CONN.execute('''CREATE TABLE MOVIES
       (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
       TITLE TEXT NOT NULL,
       YEAR INTEGER NOT NULL,
       GENRE TEXT,
       ACTORS TEXT,
       SUMMARY TEXT);''')


def parse_movie(movie_id):
    """
    make a call to the OMDB API with IMDB ID
    parse the retrieved info.
    """
    if not check_unique(movie_id):
        print "\tMovie data already exists."
        return
    title = ""
    year = ""
    genre = ""
    description = ""
    actors = ""
    payload = {
        'i': movie_id
    }
    response = requests.get(HOST, params=payload)
    if response.status_code != 200:
        print '\tCheck movie id[%s].' % response.status_code
        return None
    try:
        json_obj = json.loads(response.text)
        language = json_obj['Language']
        if language.find("English") == -1:
            print "Not an ENGLISH movie. Moving on."
            return None
        title = json_obj['Title']
        year = json_obj['Year']
        genre = json_obj['Genre']
        description = json_obj['Plot'].replace('"', "'")
        actors = json_obj['Actors']
    except Exception, ex:
        print ex, response.url
    print "\t%s[%s]" % (title, year)
    return movie_id, title, year, genre, description, actors


def check_unique(movie_id):
    """
    check if the movie is already present in the DB.
    """
    sql = ''' SELECT * FROM MOVIES
            WHERE id = "%s"
            ''' % movie_id
    cursor = CONN.execute(sql)
    if len(cursor.fetchall()) > 0:
        return False
    return True


def add_to_db(movie_data):
    """
    add a row to the db with movie info.
    """
    sql = '''
            INSERT INTO MOVIES(ID, TITLE, YEAR, GENRE, SUMMARY, ACTORS)
            VALUES("%s", "%s", %s, "%s", "%s", "%s")
            ''' % tuple(movie_data)
    try:
        CONN.execute(sql)
        CONN.commit()
    except sqlite3.OperationalError, ex:
        print ex, sql


def main():
    """
    main function
    """
    try:
        create_table_db()
    except sqlite3.DatabaseError, ex:
        print ex
    movie_list = get_movie_list('list')
    for movie_id in movie_list:
        print "Fetching data for %s." % movie_id
        movie_data = parse_movie(movie_id)
        if movie_data is None:
            continue
        add_to_db(movie_data)


if __name__ == "__main__":
    CONN = sqlite3.connect('im.db')
    main()
