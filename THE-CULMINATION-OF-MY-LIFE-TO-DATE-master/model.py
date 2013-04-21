from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Date
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
import correlation

engine = create_engine("sqlite:///ratings.db", echo = False)
session = scoped_session(sessionmaker(bind=engine, autocommit = False, autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

def authenticate(email, password):
	print "0000000000000000000000000000000000000000000000"
	user_info = session.query(User).filter_by(email=email, password=password).one()
	print user_info.email, "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
	print user_info.password, "BBBBBBBBBBBBBBBBBBBBBBBBBBB"
	print user_info
	return user_info.id

	# if result:
	# 	fields = ["id", "email", "password", "username"]
	# 	print "You've been authorized!"
	# 	return dict(zip(fields, result))
	# else:
	# 	return None


### Class declarations go here

class User(Base):
	# informs SQLAlchemy that instances of this class will be stored in table named users
	__tablename__ = "users"


	def similarity(self, other):
		u_ratings = {}
		paired_ratings = []
		for r in self.ratings:
			u_ratings[r.movie_id] = r

		for r in other.ratings:
			u_r = u_ratings.get(r.movie_id)
			if u_r:
				paired_ratings.append( (u_r.rating, r.rating) )

		if paired_ratings:
			return correlation.pearson(paired_ratings)
		else:
			return 0.0


	def predict_rating(self, movie):
		# get the ratings of the given user
		ratings = self.ratings
		# make list of ALL RATINGS by every user who's rated that movie (object)
		other_ratings = movie.ratings
		# makes list of tuples (similarity score, rating) for all the ratings that other users 
		# have made of that movie (passed in in argument)
		similarities = [ (self.similarity(other_rating.user), other_rating) \
			for other_rating in other_ratings ]
		# sort list of tuples by reversed similarity correlation (1 --> -1)
		similarities.sort(reverse = True)
		similarities = [ sim for sim in similarities if sim[0] > 0 ]
		if not similarities:
		    return None
		numerator = sum([ r.rating * similarity for similarity, r in similarities ])	
		denominator = sum([ similarity[0] for similarity in similarities ])	 
		return numerator/denominator


	# tells SQLAlchemy to add column to table named "id" as primary key
	id = Column(Integer, primary_key = True)
	# nullable = True means that the information isn't required
	email = Column(String(64), nullable = True)
	password = Column(String(64), nullable = True)
	age = Column(Integer, nullable = True)
	gender = Column(String(15), nullable = True)
	occupation = Column(String(64), nullable = True)
	zipcode = Column(String(15), nullable = True)


class Movies(Base):
	__tablename__ = "movies"


	id = Column(Integer, primary_key = True)
	# OH MY GOD WHY DO WE HAVE THIS TOO?! THAT'S DUPE IDS AHAHAHA
	# Must delete ratings.db when we have the energy to start over
	movie_id = Column(Integer)
	movie_title = Column(String(64))
	release_date = Column(Date)
	video_release_date = Column(Date, nullable = True)
	imdb_url = Column(String(128))



class Ratings(Base):
	__tablename__ = "ratings"

	id = Column(Integer, primary_key = True)
	# declaring it to be a ForeignKey = references another column in another table (the users.id column)
	user_id = Column(Integer, ForeignKey('users.id'))
	movie_id = Column(Integer, ForeignKey('movies.id'))# DOES NOT WORK Why?
	rating = Column(Integer)
	timestamp = Column(Date)


	user = relationship("User", backref=backref("ratings", order_by=id))
	movie = relationship("Movies", backref = backref("ratings", order_by = id))

### End class declarations


def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()



# import correlation
# rating_pairs = [(5,5), (3,3), (2,3)]
# print correlation.pearson(rating_pairs)
# 	0.944911182523


# o= other_users[0]
# u_ratings = {}
# for r in u.ratings:
#     u_ratings[ r.movie_id ] = r

# paired_ratings = []
# for o_rating in o.ratings:
#     u_rating = u_ratings.get(o_rating.movie_id)
#     if u_rating:
#             pair = (u_rating.rating, o_rating.rating)
#             paired_ratings.append(pair)
