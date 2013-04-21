"""
seed.py
"""
import model

db = model.connect_db()
# user_id = model.new_user(db, "chriszf@gmail.com", "securepassword", "Christian")
# task = model.new_task(db, "Complete this task list", user_id)
user_id = model.new_user(db, "gulnara@gmail.com", "password", "Gulnara")
task = model.new_task(db, "we did it!", user_id)
task = model.new_task(db, "almost done!!", user_id)