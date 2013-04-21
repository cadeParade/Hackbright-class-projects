from flask import Flask, render_template, redirect, request, flash, url_for, g
from flask import session as fsession
import model
import datetime

app = Flask(__name__)


# @app.before_request
# def set_up_db():
#     g.db = model.connect_db()

# @app.teardown_request
# def disconnect_db(e):
#     g.db.close()

@app.route("/authenticate", methods=["POST"])
def authenticate():
    email = request.form["email"]
    password = request.form["password"]
    user_id = model.authenticate(email, password) #(g.db, email, password)?
    # DOESN'T WORK IF AREN'T IN DB??!
    if user_id:
    	fsession["user_id"] = user_id
    	fsession["email"] = email
    	return redirect("/view_user")
    else:
    	flash("I'm sorry, either that password or email is not in our database.")
    	return redirect("/")


@app.route('/logout', methods=["POST"])
def logout():
    # remove the username from the session if it's there
    fsession.pop('user_id', None)
    fsession.pop('email', None)
	# flash('You have logged out.')
    return redirect(url_for('index'))

@app.route("/")
def index():
	# do sign up stuff here
	return render_template("index.html")

@app.route("/sign_up")
def sign_up():
	return render_template("sign_up.html")

def email_exists(email):
	email_exists = model.session.query(model.User).filter_by(email = email).first()
	if email_exists:
		return True
	else:
		return False

@app.route("/new_user", methods=["POST", 'GET'])
def new_user():
	error = None
	#retrieves form information
	new_email = request.form["email"]
	new_password = request.form["password"]
	new_occ = request.form["occupation"]
	new_age = request.form["age"]
	new_gender = request.form["gender"]
	new_zip =request.form["zipcode"]


	#test if new_email exists
	if email_exists(new_email) == True:
		error = "Sorry, that email was already used. Please use another."
		return render_template("sign_up.html", error = error)

	else:
		#enters info into database
		new_user = model.User(email=new_email, password=new_password, age=None, gender=None, occupation=None, zipcode=None)
		model.session.add(new_user)
		model.session.commit()

		#getting user id
		users = model.session.query(model.User).filter_by(email=new_email).all()
		return redirect("/view_user/" + str(users[0].id))

@app.route("/new_movie", methods=["POST"])
def new_rating():
	error = None
	#retrieves form information
	new_movie = request.form["new_movie"]
	new_rating = request.form["new_rating"]

	#test if new_rating is between 1-5

	# test if the movie exists in db
	movie_exists = model.session.query(model.Movies).filter_by(movie_title=new_movie).first()
	
	# movie_exists = model.session.query(model.Ratings).filer(Ratings.movie_title.like('%new_movie%')).first()
	
	if movie_exists:
		movie_id = movie_exists.id
		release_date = movie_exists.release_date
		video_release_date = movie_exists.video_release_date
		now = datetime.datetime.now()
		imdb_url = movie_exists.imdb_url

		new_rating_item = model.Ratings(user_id=fsession["user_id"], movie_id=movie_id, rating=new_rating, timestamp=now)

		model.session.add(new_rating_item)
		model.session.commit()
		return redirect("/view_user")

	else:
		# make a new PAGE so you can make new movie
		return redirect("/new_movie")
	

@app.route("/add_movie", methods=["POST"])
def add_movie():
	# TAKE ALL THE FORM INFO
	error = None
	#retrieves form information
	new_title = request.form["new_title"]
	movie_release = request.form["movie_release"]
	
	movie_release = datetime.datetime.strptime(movie_release, "%Y") # format: 1962-01-01 00:00:00

	video_release = request.form["video_release"]
	imdb_url = request.form["imdb_url"]
	rating = request.form["rating"]
	
	if video_release == '':
		video_release = None

	# make a new movie item
	new_movie_item = model.Movies(movie_title=new_title, release_date=movie_release, video_release_date=video_release, imdb_url=imdb_url)

	model.session.add(new_movie_item)
	model.session.commit()

	# query id for that movie item
	query = model.session.query(model.Movies).filter_by(movie_title=new_title).first()

	# make a new rating with the user id from the session
	now = datetime.datetime.now()
	query_id = query.id
	new_rating_item = model.Ratings(user_id=fsession["user_id"], movie_id=query_id, rating=rating, timestamp=now)
	
	#test if new_rating is between 1-5

	# test if the movie exists in db
	
	model.session.add(new_rating_item)
	model.session.commit()
	return redirect("/view_user")


@app.route("/view_movie/<int:id>", methods=["GET"])
def view_movie(id):
    movie = model.session.query(model.Movies).get(id)
    print movie, "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa"
    ratings = movie.ratings
    print ratings, "ratings"
    rating_nums = []
    user_rating = None
    for r in ratings:
        if r.user_id == fsession['user_id']:
            user_rating = r
        rating_nums.append(r.rating)
    print rating_nums, "Printing numbs"
    avg_rating = float(sum(rating_nums))/len(rating_nums)
    print avg_rating, "Average rating"

    # Prediction code: only predict if the user hasn't rated it.
    user = model.session.query(model.User).get(fsession['user_id'])
    prediction = None
    if not user_rating:
        prediction = user.predict_rating(movie)
    # End prediction

    return render_template("view_movie.html", movie=movie, 
            average=avg_rating, user_rating=user_rating,
            prediction=prediction)


@app.route("/new_movie")
def new_movie():
	
	return render_template("new_movie.html")



@app.route("/user_list")
def user_list():
	# queries all the users, returns in a list
	user_list = model.session.query(model.User).limit(5).all()
	# "redirects" to user_list.html, feeding argument of list of user objects
	return render_template("user_list.html", users=user_list)

# @app.route("/user_ratings")
# def user_ratings():
# 	user_ratings = model.session.query(model.Ratings).all()

@app.route("/view_user") # <int:user_id>")
def view_user():
	user_id = fsession.get("user_id", None)
	# query for all ratings made by the given user_id
	# can access id, user_id, movie_id, rating and timestamp with rating_info.*
	rating_info = model.session.query(model.Ratings).filter_by(user_id=user_id).all()
	# make dictionary to hold all movie/rating information per movie_id
	if rating_info:
		rating_list = []
		for i, rating in enumerate(rating_info):
			# returns int movie_id
			temp_movie_id = rating.user.ratings[i].movie_id
			temp_movie_title = rating.movie.movie_title
			temp_imdb_url = rating.movie.imdb_url
			rating_list.append([temp_movie_id, temp_movie_title, 
								rating.rating, rating.user.occupation, 
								temp_imdb_url])
			# rating_dict[rating.movie_id] = model.session.query(model.Movies).get(rating.movie_id)
		return render_template("view_user.html", user_id = user_id, ratings = rating_list)
	return render_template("view_user.html", user_id = user_id)


@app.route("/view_user/<int:user_id>")
def view_public_user(user_id):
	# query for all ratings made by the given user_id
	# can access id, user_id, movie_id, rating and timestamp with rating_info.*
	rating_info = model.session.query(model.Ratings).filter_by(user_id=user_id).all()
	# make dictionary to hold all movie/rating information per movie_id
	if rating_info:
		rating_list = []
		for i, rating in enumerate(rating_info):
			# returns int movie_id
			temp_movie_id = rating.user.ratings[i].movie_id
			temp_movie_title = rating.movie.movie_title
			temp_imdb_url = rating.movie.imdb_url
			rating_list.append([temp_movie_id, temp_movie_title, 
								rating.rating, rating.user.occupation, 
								temp_imdb_url])
			# rating_dict[rating.movie_id] = model.session.query(model.Movies).get(rating.movie_id)
		return render_template("view_public_user.html", ratings = rating_list)
	return render_template("view_public_user.html")



@app.route("/super_secret")
def super_secret():
	return render_template("super_secret.html")

"""
@app.route("/save_task", methods = ["POST"])
def save_task():
	task_title = request.form["task_title"]
	db = model.connect_db()
	#Assumer that all tasks are attached to user 1.
	task_id = model.new_task(db, task_title, 1)
	return redirect("/tasks"
"""

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == "__main__":
	app.run(debug = True)