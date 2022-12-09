from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_cors import CORS
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

# SQLAlchemy config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Flask Admin
app.config['FLASK_ADMIN_SWATCH'] = 'Cyborg'
app.config['SECRET_KEY'] = 'TheCakeIsALie'

db = SQLAlchemy(app)
admin = Admin(app)
login = LoginManager(app)
cors = CORS(app)

from db import User, Teacher, Student, Course, Enrollment

# -------- Admin ---------- (localhost:5000/admin)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Teacher, db.session))
admin.add_view(ModelView(Student, db.session))
admin.add_view(ModelView(Course, db.session))
admin.add_view(ModelView(Enrollment, db.session))

# -------- Login ---------- (localhost:5000/login)
login.login_view = 'login'

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/", methods = ["POST", "GET"])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"] 

        user = User.query.filter_by(username=username).first() # Get user from database

        if user is None or not user.check_password(password): # if user doesn't exist or password is wrong
                return render_template("login.html") # reload the page

        login_user(user) # log in the user

        if user.student_id is None: # if user is a teacher
            teacher = Teacher.query.filter_by(id=user.teacher_id).first()
            return redirect(url_for('instructor', name = teacher.name))
        else: # if user is a student
            student = Student.query.filter_by(id=user.student_id).first()
            return redirect(url_for('student', name=student.name))

    else:
        if current_user.is_authenticated:
            if current_user.student_id is None: 
                teacher = Teacher.query.filter_by(id=current_user.teacher_id).first()
                return redirect(url_for('instructor', name = teacher.name))
            else:
                student = Student.query.filter_by(id=current_user.student_id).first()
                return redirect(url_for('student', name=student.name))

        return render_template("login.html")


@app.route('/logout') # localhost:5000/logout
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/student/<name>", methods = ['POST', 'GET']) # localhost:5000/student/<name>
# @login_required
def student(name):
    student_name = name
    thedata = []
        
    # get all courses the student is enrolled in
    if request.method == 'GET':
        studentQuery = Student.query.filter_by(name=student_name).first() # get student from database
        studentQC = studentQuery.courses # get courses from student

        for i in range(len(studentQC)): # for each course 
            temp = { # create a dictionary
                'name':studentQC[i].course.course_name,
                'instructor':studentQC[i].course.teacher.name,
                'time':studentQC[i].course.time,
                'enrollment':(str(studentQC[i].course.number_enrolled) + "/" + str(studentQC[i].course.capacity))
            }
            thedata.append(temp) # add dictionary to list
        
    # add or remove a course
    elif request.method == 'POST': 
        course_name = request.form.get('course_name') # get course name from form 
        enroll_option = request.form.get('enroll_option') # get enroll option from form
        studentQuery = Student.query.filter_by(name=student_name).first() # get student from database
        courseReqNm = course_name # course name to be requested
        courseReq = Course.query.filter_by(course_name = courseReqNm).first() # get course from database

        if enroll_option == 'add':
            # update the enrollment count
            Course.query.filter_by(course_name = courseReqNm).update({'number_enrolled': (Course.number_enrolled + 1)}) # update enrollment count
            newCourseStu = Enrollment(student_id = studentQuery.id, course_id = courseReq.id, grade = "") # create new enrollment
            db.session.add(newCourseStu) # add enrollment to database

        elif enroll_option == 'remove':
            Course.query.filter_by(course_name = courseReqNm).update({'number_enrolled': (Course.number_enrolled - 1)}) # update enrollment count
            enrollmentReq = Enrollment.query.filter_by(student_id = studentQuery.id, course_id = courseReq.id).first() # get enrollment from database
            db.session.delete(enrollmentReq) # delete enrollment from database

        db.session.commit() # commit changes to database
    
    return render_template("student.html", student_name = student_name, data = thedata)


@app.route("/instructor/<name>") # localhost:5000/instructor/<name>
# @login_required
def instructor(name):
    instructor_name = name
    teacherdata = []
    teacherQuery = Teacher.query.filter_by(name=instructor_name).first() 
    teacherQC = Course.query.filter_by(teacher_id = teacherQuery.id).all()

    for i in range(len(teacherQC)): # for each course
        temp = { # create a dictionary
            'name':teacherQC[i].course_name,
            'instructor':instructor_name,
            'time':teacherQC[i].time,
            'enrollment':(str(teacherQC[i].number_enrolled) + "/" + str(teacherQC[i].capacity))
        }
        teacherdata.append(temp) # add dictionary to list
    
    return render_template("instructor.html", instructor_name = instructor_name, data = teacherdata) 

@app.route("/instructor/<name>/<course>", methods = ['GET', 'POST']) # localhost:5000/instructor/<name>/<course>
def specific_course(name, course, student = None):
    instructor_name = name
    instructor_course = course
    teachCourseData = []
    teacherQuery = Teacher.query.filter_by(name=instructor_name).first()
    teacherQC = Course.query.filter_by(teacher_id = teacherQuery.id, course_name = instructor_course).first()

    print(teacherQC)

    if request.method == 'GET':
        # Displays grades for a specific course
        for j in range(len(teacherQC.students)): # for each student
            temp1 = { # create a dictionary
                'name':teacherQC.students[j].student.name,
                'grade':teacherQC.students[j].grade
            }
            teachCourseData.append(temp1) # add dictionary to list

    if request.method == 'POST':
        student_id = Student.query.filter_by(name = request.args.get('student')).first().id # get student id from database
        course_id = Course.query.filter_by(course_name = instructor_course).first().id # get course id from database

        Enrollment.query.filter_by(student_id = student_id, course_id = course_id).update({'grade': (request.form.get('new_grade'))}) # update grade
        db.session.commit()

        for j in range(len(teacherQC.students)): # for each student
            temp1 = {
                'name':teacherQC.students[j].student.name,
                'grade':teacherQC.students[j].grade
            }
            teachCourseData.append(temp1)

    return render_template("specificCourse.html", instructor_name = instructor_name, instructor_course = instructor_course, data = teachCourseData)

@app.route("/enrolled/<name>") # localhost:5000/enrolled/<name>
def enrolled(name, methods = ['POST', 'GET']):
    student_name = name
    thedata = []
    if request.method == 'GET':
        studentQuery = Student.query.filter_by(name=student_name).first()
        studentQC = studentQuery.courses

        for i in range(len(studentQC)):
            temp = {
                'name':studentQC[i].course.course_name,
                'instructor':studentQC[i].course.teacher.name,
                'time':studentQC[i].course.time,
                'enrollment':(str(studentQC[i].course.number_enrolled) + "/" + str(studentQC[i].course.capacity))
            }
            thedata.append(temp)
    
    return jsonify(thedata)

@app.route("/courses") 
def courses():
    thedata = []
    courseQ = Course.query.all()
    for i in range(len(courseQ)):
        temp = {
            'name':courseQ[i].course_name,
            'instructor':courseQ[i].teacher.name,
            'time':courseQ[i].time,
            'enrollment':(str(courseQ[i].number_enrolled) + "/" + str(courseQ[i].capacity))
        }
        thedata.append(temp)
    return jsonify(thedata)

if __name__ == "__main__":
    app.run(debug=True)