from flask import Flask, render_template, request, redirect
import model
import datetime

app = Flask(__name__)

@app.before_request
def before_request():
	print request

@app.route("/")
def index():
	return render_template("index.html", user_name = "GULNARA IS AWESOME", 
							another_field = "TESTING")

@app.route("/tasks", methods=["GET", "POST"])
def list_tasks():
	db = model.connect_db()
	tasks_from_db = model.get_tasks(db, None)
	completed_items = request.form.getlist("completed_t_f", type=int)
	if completed_items:
		for task in completed_items:
			model.complete_task(db, task)

	return render_template("tasks.html", tasks_field = tasks_from_db)


@app.route("/new_task")
def new_task():
	return render_template("new_task.html")

@app.route("/save_task", methods=["POST"])
def save_task():
	# print request.form
	task_title = request.form['task_title']
	category = request.form["category"]
	priority = request.form["priority"]
	due_date = request.form["due_date"]
	
	#due_date = datetime.datetime.now()
	db = model.connect_db()
	created_at = datetime.datetime.now()
	task_id = model.new_task(db, task_title, 1, 
							 created_at, 0, 
							 category, None, priority, due_date)
	# return "Success!"
	return redirect("/tasks")

@app.route("/task_complete")
def completed_task():
	return render_template("completed.html")


if __name__ == "__main__":
	app.run(debug=True)
