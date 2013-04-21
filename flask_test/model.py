import sqlite3
import datetime

def connect_db():
#def connect_db():
	return sqlite3.connect("tipsy.db")

def new_user(db, email, password, name):
	c = db.cursor()
	query = """INSERT INTO Users VALUES (NULL, ?, ?, ?)"""
	result = c.execute(query, (email, password, name))
	db.commit()
	print """\
New User: email:  %s, password: %s, name: %s"""%(email, password, name)
	return result.lastrowid
	


def authenticate(db, email, password):
	c = db.cursor()
	query = """ SELECT * from Users WHERE email = ? AND password = ?"""
	c.execute(query, (email, password))
	result = c.fetchone()
	if result:
		fields = ["id", "email", "password", "username"]
		print fields
		return dict(zip(fields, result))

	return None


def new_task (db, title, user_id, created_at, completed_at, category, 
		     completed_t_f, priority,due_date ):
	# category = raw_input("category?")
	# priority = raw_input("How important is this on a scale from 1-5 (1 is most important)?")
	# due_date = raw_input ("When is this due?")
	completed_t_f = None
	created_at = datetime.datetime.now()
	completed_at = None


	#create new task!!!
	c = db.cursor()
	query = """ INSERT INTO Tasks VALUES (NULL, ?,?, ?,?,?,?,?,?)"""
	result = c.execute(query, (title, user_id, created_at, 
		    				   completed_at, category, 
		     				   completed_t_f, priority,
		     				   due_date)) 
	db.commit()
	print """New task entered: Task name: %s
	user id: %s
	created_at: %s
	completed_at: %s
	category: %s
	completed true or false: %s
	priority: %s
	due_date: %s""" % (title, user_id, created_at, 
		    				   completed_at, category, 
		     				   completed_t_f, priority,
		     				   due_date)
	return result.lastrowid

def get_user(db, id):
	# user_id = int(user_id)
	# print user_id
	c = db.cursor()
	query = """SELECT * from Users WHERE id = ?"""
	c.execute(query, (id,))
	result=c.fetchone()
	if result:
		fields= ["id", "email", "password", "username"]
		print fields
		return dict(zip(fields, result))

	return None

def complete_task(db, task_id):
	current_date = datetime.datetime.now()
	c = db.cursor()
	query = """UPDATE Tasks SET completed_at = ?, completed_t_f = 1
			   WHERE id = ?"""
	c.execute(query, (current_date,task_id))
	db.commit()
	c.execute("""SELECT title, completed_at FROM Tasks WHERE id = ?""", (task_id,))
	results = c.fetchone()
	#print fields_we_get
	print """Task name: %s
	completed at: %s"""%(results[0],results[1])

# def get_tasks(db, user_id = None):
# 	c = db.cursor()
# 	if user_id:
# 		query = """SELECT * FROM Tasks WHERE user_id=?"""
# 		c.execute(query, (user_id,))
# 		results = c.fetchall()
# 		return results
# 	else:
# 		query = """SELECT * FROM Tasks"""
# 		c.execute(query)
# 		results = c.fetchall()
# 		print """No user ID given.
# 		%s""" % results
# 		return results

def get_tasks(db, user_id = None):
	c = db.cursor()
	if user_id:
		query = """SELECT * FROM Tasks WHERE user_id=?"""
		c.execute(query, (user_id,))
	else:
		query = """SELECT * FROM Tasks"""
		c.execute(query)
 	tasks = []
	rows = c.fetchall()
	for row in rows:
		task = dict(zip(["id", "title", "user_id", "date created", "date completed", 
				  "category", "completed_t_f", "priority", "due date"], row))
		tasks.append(task)

	return tasks
# 		print """No user ID given.
# 		%s""" % results
# 		return results

def get_task(db,task_id):
	c = db.cursor()
	query = """ SELECT * from Tasks WHERE id = ?"""
	c.execute(query, (task_id,))
	result = c.fetchone()
	if result:
		fields = ["id", "title", "user_id", "date created", "date completed", 
				  "category", "completed_t_f", "priority", "due date"]
		print fields
		print_return = dict(zip(fields, result))
		print print_return
		#for item in print_return:
		#	print item
		return dict(zip(fields, result))

	return None

def get_all_users():
	c = db.cursor()
	query = """SELECT * FROM Users"""
	c.execute(query)
	result = c.fetchall()
	print result

def get_all_tasks():
	c = db.cursor()
	query = """SELECT * FROM Tasks"""
	c.execute(query)
	result = c.fetchall()
	print result


# def main():
#     connect_db()
#     command = None
#     while command != "quit":
#         input_string = raw_input("todo Database> ")
#         tokens = input_string.split()
#         command = tokens[0]
#         args = tokens[1:]

#         if command == "new_user":
#             new_user(*args) 
#         elif command == "authenticate":
#             authenticate(*args)

#     CONN.close()

# if __name__ == "__main__":
#     main()