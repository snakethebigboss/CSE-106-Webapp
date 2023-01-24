from flask import Flask, render_template, request, url_for, redirect
from flask_cors import CORS
import sqlite3
from sqlite3 import Error
import json

app = Flask(__name__)
CORS(app)
db = r'tpch.sqlite'
with app.app_context():
 

    #login is startup
    @app.route("/")
    def login():
        print("Request received in LOGIN")
        return render_template("login.html")

    #should make sure that login is correct
    @app.route("/pyauth", methods=['GET','POST'])
    def pyauth():
        print("Request received in PYAUTH")
        ##database stuff
        #if correct user name and password
        #render student or teacher template
        print("CONGRATS!!!!")
        try:
            conn = sqlite3.connect(db)
            c = conn.cursor()
            sql = """select u_username, u_password
                    from users
                    where
                        u_username = ?
                        AND u_password = ?;"""
            
            data = request.form
            print(data['username'])

            username = ''
            password = ''
            args = [username, password]
            return render_template("student.html")
            # c.execute(sql, args)
        except Error as e:
            print(e)
            print("ERROR: Username or Password may be incorrect")
            return "<p>Error: Username or Password may be incorrect</p>"
        

        #or

        # return render_template("student.html")

    #returns classes that students are involved in
    @app.route('/enrolled/<string:name>', methods=['GET'])
    def enrolledtable(name):
        
        #database stuff
        return #enrolledClasses

    #gets all classes that are avalaible to take, doesn't matter if its full or not
    @app.route('/allclasses', methods=['GET'])
    def allclasses(name):
        
        #database stuff
        return #allclasses

    #classes taught by the instructor is returned
    @app.route('/classesTaught/<string:name>', methods=['GET'])
    def tableInstructor(name):
        
        #database stuff
        return #taughtClasses

    #just loads the html for the specific class that is chosen on the instructor page
    @app.route('/loadspecificCourse/')
    def loadspecifcCourse(classname):
        #just loads the html page
        return render_template("specificCourse.html")
    
    #gets that data from the specific class that is chosen
    @app.route('/specificCourse/<string:classname>', methods=['GET'])
    def specifcCourse(classname):
        
        #database stuff
        return #specifcClasses
    


    
    # ######GETS ALL GRADES###########
    # @app.route('/grades', methods=['GET'])
    # def get_grades():
    #     result = Student.query.all()
    #     grades = {}
    #     for r in result:
    #         grades[r.name] = r.grade
    #     return grades

    # ########GET SPECIFIC GRADE#############
    # @app.route('/grades/<string:name>', methods=['GET'])
    # def get_specificgrade(name):
    #     result = Student.query.all()
    #     grades = {}
    #     for r in result:
    #         grades[r.name] = r.grade
    #     return {name: grades[name]}

    # #########ADD USER################
    # @app.route('/grades', methods=['POST'])
    # def addname():
    #     content = request.get_json()
        
    #     db.session.add(Student(name=content['name'], grade = content['grade']))
    #     db.session.commit()

    #     result = Student.query.all()
    #     grades = {}
    #     for r in result:
    #         grades[r.name] = r.grade
    #     return grades

    # #############EDIT##################
    # @app.route('/grades/<string:name>', methods=['PUT'])
    # def editname(name):
    #     content = request.get_json()
        
    #     student = Student.query.filter_by(name=name).first()
    #     student.grade = content['grade']
    #     db.session.commit()

    #     result = Student.query.all()
    #     grades = {}
    #     for r in result:
    #         grades[r.name] = r.grade
    #     return grades

    # ##########DELETE USER###############
    # @app.route('/grades/<string:name>', methods=['DELETE'])
    # def deleteuser(name):
    #     student = Student.query.filter_by(name=name).first()
    #     db.session.delete(student)
    #     db.session.commit()

    #     result = Student.query.all()
    #     grades = {}
    #     for r in result:
    #         grades[r.name] = r.grade
    #     return grades 


    if __name__ == "__main__":
        app.run()