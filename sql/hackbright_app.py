import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    if row:
        print """\
        Student: %s %s
        Github account: %s"""%(row[0], row[1], row[2])
    else:
        print "NOPE"

def get_a_project_by_title(title):
    query = """SELECT title, description, max_grade FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    if row:
        print """\
        title: %s
        description: %s 
        max score: %s """%(row[0], row[1], row[2])
    else:
        print "no project with %s title" % title

def get_students_grade_of_project(first_name, title):
    query = """SELECT Students.first_name, Projects.title, Grades.grade 
               FROM Students INNER JOIN Grades ON
               Students.github = Grades.student_github INNER JOIN Projects ON
               Grades.project_title = Projects.title 
               WHERE Students.first_name = ? and Projects.title = ?"""
    DB.execute(query, (first_name, title))
    #row = DB.fetchone()
    row = DB.fetchall()
    if row:
        print "Student name: %s" % first_name
        for i in range(len(row)):
            print """\
            project name: %s
            student grade: %s \n\n"""%(row[i][1], row[i][2])
    else:
        print "no grade for %s for %s project" % (first_name, project)

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("my_database.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?,?,?)"""
    DB.execute (query, (first_name,  last_name, github))
    CONN.commit()
    print "Successfully added students: %s %s"%(first_name, last_name)

def make_new_project(title, description, max_grade):
    query = """INSERT into Projects values (?,?,?)"""
    DB.execute (query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added project: %s a.k.a. %s"%(title, description)

def give_grade(student_github, project_title, grade):
    query = """INSERT into Grades values (?,?,?)"""
    DB.execute (query, (student_github, project_title, grade))
    CONN.commit()
    print "Grade for %s on %s is: %s" %(student_github, project_title, grade)

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            print "new_student"
            make_new_student(*args)
        elif command == "new_project":
            make_new_project(*args)
        elif command == "project":
            get_a_project_by_title(*args)
        elif command == "student_grade":
            get_students_grade_of_project(*args)
        elif command == "enter_grade":
            give_grade(*args)

    CONN.close()

if __name__ == "__main__":
    main()
