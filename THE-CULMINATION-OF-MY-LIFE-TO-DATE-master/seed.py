import model
import csv
from datetime import datetime

def load_users(session):
    ### FROM FILE user id | age | gender | occupation | zip code
    ### PASS INTO ALCHEMY email, password, age, gender, occupation, zipcode
    data = csv_reader("seed_data/u.user", "|")
    for row in data:
        # use zip dictionary
        idNum = int(row[0])
        age = int(row[1])
        gender = row[2]
        occupation = row[3]
        zipcode = row[4]
        user = model.User(id=idNum, email = None, password = None, 
                    age = age, gender = gender, 
                    occupation = occupation, zipcode = zipcode)
        session.add(user)
    session.commit()

def load_movies(session):
    ### FROM FILE movie id | movie title | release date | video release date | IMDb URL 
    #      GENRES: | unknown | Action | Adventure | Animation |
    #      Children's | Comedy | Crime | Documentary | Drama | Fantasy |
    #      Film-Noir | Horror | Musical | Mystery | Romance | Sci-Fi |
    #      Thriller | War | Western |
    ### PASS INTO movie_id, movie_title, release_date, video_release_date, imdb_url
    data = csv_reader("seed_data/u.item", "|")
    for row in data:

        idNum = int(row[0])
        movie_title = row[1].decode("latin-1")
        release_date = row[2]
        video_release_date = row[3]
        imdb_url = row[4]

        if (release_date == ''): 
            release_date = None
        else:
            release_date = datetime.strptime(row[2], "%d-%b-%Y")

        if (video_release_date == ''): 
            video_release_date = None 
        else:
            video_release_date = datetime.strptime(row[3], "%d-%b-%Y")

        movie = model.Movies(movie_id=idNum, movie_title=movie_title, release_date=release_date, video_release_date=video_release_date, imdb_url=imdb_url)
        session.add(movie)
    session.commit()

def load_ratings(session):
    ### FROM FILE user id | item id | rating | timestamp
    ### PASS INTO id, user_id, movie_id, rating, timestamp
    data = csv_reader("seed_data/u.data", "\t")
    for row in data:
        user_id = int(row[0])
        item_id = int(row[1])
        rating = int(row[2])
        timestamp = row[3]
        timestamp = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')
        timestamp =  datetime.strptime(timestamp, '%Y-%m-%d')
        #timestamp = datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d')
        rating = model.Ratings(user_id=user_id, movie_id=item_id, rating=rating, timestamp=timestamp)
        session.add(rating)
    session.commit()


def csv_reader(fileName, delim):
    open_file = open(fileName, "rb")
    read_file = csv.reader(open_file, delimiter = delim)
    return read_file

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)
    load_movies(session)
    load_ratings(session)

if __name__ == "__main__":
    s= model.connect()
    main(s)
