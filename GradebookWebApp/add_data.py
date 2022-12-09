from db import db, User, Teacher, Student, Course, Enrollment

# Data that will prepoulated the database upon creation

teachers = [
	("Sage Gowry", "sgowry", "helloworld123"), 
	("Lord Mohgwyn", "lmohgwyn", "helloworld123"),
	("Master Azur", "mazur", "helloworld123")
]

for teacher_info in teachers:
	name = teacher_info[0]
	username = teacher_info[1]
	password = teacher_info[2]
	
	u = User(username=username, password=password)
	t = Teacher(name=name, user=u)
	db.session.add(u)
	db.session.add(t)


students = [
	("Jose Santos", "jsantos", "helloworld123"),
	("Betty Brown", "bbrown", "helloworld123"),
	("John Stuart", "jstuart", "helloworld123"),
	("Li Cheng", "lcheng", "helloworld123"),
	("Nancy Little", "nlittle", "helloworld123"),
	("Mindy Norris", "mnorris", "helloworld123"),
	("Aditya Ranganeth", "aranganeth", "helloworld123"),
	("Yi Wen Chen", "ychen", "helloworld123")
]

for student_info in students:
	name = student_info[0]
	username = student_info[1]
	password = student_info[2]

	u = User(username=username, password=password)
	s = Student(name=name, user=u)
	db.session.add(u)
	db.session.add(s)


courses = [
	("Glintstone Sorcery", 1, 4, 8, "MWF 10:00-10:50 AM"),
	("Blood Incantations", 2, 5, 10, "TR 11:00-11:50 AM"),
	("Primeval Currents", 3, 4, 10, "MWF 2:00-2:50 PM"),
	("The History of the Stars", 3, 4, 4, "TR 3:00-3:50 PM")
]

for course_info in courses:
	course_name = course_info[0]
	teacher_id = course_info[1]
	number_enrolled = course_info[2]
	capacity = course_info[3]
	time = course_info[4]

	t = Teacher.query.filter_by(id=teacher_id).first()
	c = Course(
		course_name=course_name, 
		teacher_id=teacher_id, 
		teacher=t, 
		number_enrolled=number_enrolled, 
		capacity=capacity, 
		time=time
	)

	db.session.add(c)

enrollment_info = [
	(1, 1, 92),
	(2, 1, 65),
	(3, 1, 86),
	(4, 1, 77),
	(5, 2, 53),
	(4, 2, 85),
	(6, 2, 94),
	(3, 2, 91),
	(2, 2, 88),
	(7, 3, 93),
	(8, 3, 85),
	(5, 3, 57),
	(6, 3, 68),
	(7, 4, 99),
	(5, 4, 87),
	(8, 4, 92),
	(3, 4, 67)
]

for info in enrollment_info:
	student_id = info[0]
	course_id = info[1]
	grade = info[2]

	c = Course.query.filter_by(id=course_id).first()
	s = Student.query.filter_by(id=student_id).first()
	e = Enrollment(grade=grade, student=s, course=c)
	db.session.add(e)

db.session.commit()