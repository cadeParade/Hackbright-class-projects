import model
import datetime

db = model.connect_db()
user_id = model.new_user(db, "chriszf@gmail.com", "securepassword", "Christian")
task = model.new_task(db, "A task for Christian", user_id, datetime.datetime.now(),
					  None, "category3", None, 4, "Tuesday")
task = model.new_task(db, "The best task OH MY FREAKING GOD", user_id, datetime.datetime.now(),
					  None, "category3", None, 5, "Next year")
user_id = model.new_user(db, "gulnara@gmail.com", "awesomepassword", "Gulnara")
task = model.new_task(db, "let's drink", user_id, datetime.datetime.now(),
					  None, "category3", None, 1, "in an hour")
task = model.new_task(db, "go to sleep", user_id, datetime.datetime.now(),
					  None, "category4", None, 2, "in 2 hours")
user_id = model.new_user(db, "lindsay@gmail.com", "yeahyeahyeah", "Lindsay")
task = model.new_task(db, "go hiking", user_id, datetime.datetime.now(),
					  None, "category78", None, 3, "sunday")
task = model.new_task(db, "read a few books", user_id, datetime.datetime.now(),
					  None, "category54", None, 4, "this weekend")