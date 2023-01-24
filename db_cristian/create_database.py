import names
from random_username.generate import generate_username
import sqlite3
from sqlite3 import Error
import random
from randomClassTimeGenerator import genClassTime
import string

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
    # print("Random string of length", length, "is:", result_str)


def dropTables(_conn):
    sql = """DROP TABLE users"""
    try:
        c = _conn.cursor()
        c.execute(sql)
        print("TABLE users DELETED!!!")
    except Error as e:
        print(e)


    sql = """DROP TABLE students"""
    try:
        c = _conn.cursor()
        c.execute(sql)
        print("TABLE students DELETED!!!")
    except Error as e:
        print(e)


    sql = """DROP TABLE teachers"""
    try:
        c = _conn.cursor()
        c.execute(sql)
        print("TABLE teachers DELETED!!!")
    except Error as e:
        print(e)


    sql = """DROP TABLE classes"""
    try:
        c = _conn.cursor()
        c.execute(sql)
        print("TABLE classes DELETED!!!")
    except Error as e:
        print(e)


    sql = """DROP TABLE enrollment"""
    try:
        c = _conn.cursor()
        c.execute(sql)
        print("TABLE enrollment DELETED!!!")
    except Error as e:
        print(e)


def createTables(_conn):
    # Creating users table
    create_table_sql = """CREATE TABLE users(
                    u_userid integer primary_key,
                    u_username char(100) not null,
                    u_password char(100) not null
                    )"""
    try:
        c = _conn.cursor()
        c.execute(create_table_sql)
        print("TABLE users CREATED!!!")
    except Error as e:
        print(e)

    # Creating students table
    create_table_sql = """CREATE TABLE students(
                    s_studentid integer primary_key,
                    s_name char(100) not null,
                    s_userid integer not null
                    )"""
    try:
        c = _conn.cursor()
        c.execute(create_table_sql)
        print("TABLE students CREATED!!!")
    except Error as e:
        print(e)

    # Creating teachers table
    create_table_sql = """CREATE TABLE teachers(
                    t_teacherid integer primary_key,
                    t_name char(100) not null,
                    t_userid integer not null
                    )"""
    try:
        c = _conn.cursor()
        c.execute(create_table_sql)
        print("TABLE teachers CREATED!!!")
    except Error as e:
        print(e)


    # Creating classes table
    create_table_sql = """CREATE TABLE classes(
                    c_classid integer primary_key,
                    c_name char(100) not null,
                    c_teacherid integer not null,
                    c_numenrolled integer not null,
                    c_capacity integer not null,
                    c_time time not null
                    )"""
    try:
        c = _conn.cursor()
        c.execute(create_table_sql)
        print("TABLE classes CREATED!!!")
    except Error as e:
        print(e)

    # Creating enrollment table
    create_table_sql = """CREATE TABLE enrollment(
                    e_enrollmentid integer primary_key,
                    e_classid integer not null,
                    e_studentid integer not null,
                    e_grade decimal(3,2) not null
                    )"""
    try:
        c = _conn.cursor()
        c.execute(create_table_sql)
        print("TABLE enrollment CREATED!!!")
    except Error as e:
        print(e)



def populateTables(_conn):
    errors = False
    for i in range(1000):
        # Populating users table
        username = generate_username()
        password = get_random_string(10)
        sql = """INSERT INTO users (u_userid, u_username, u_password)
            VALUES (?, ?, ?)"""
        user = (i+1, username[0], password)
        
        try:
            c = _conn.cursor()
            c.execute(sql, user)
            _conn.commit()
        except Error as e:
            errors = True
            print(e)
        
        # Populating  students table
        if i < 500:
            s_name = names.get_full_name()
            sql = """INSERT INTO students (s_studentid, s_name, s_userid)
                VALUES (?, ?, ?)"""
            student = (i+1, s_name, user[0])

            try:
                c = _conn.cursor()
                c.execute(sql, student)
                _conn.commit()
            except Error as e:
                errors = True
                print(e)
        
        # Populating teachers table
        else:
            t_name = names.get_full_name()
            t_teacherid = i-500+1
            sql = """INSERT INTO teachers (t_teacherid, t_name, t_userid)
                VALUES (?, ?, ?)"""
            teacher = (t_teacherid, t_name, user[0])

            try:
                c = _conn.cursor()
                c.execute(sql, teacher)
                _conn.commit()
            except Error as e:
                errors = True
                print(e)

        # Populating classes table
        if i < 200:
            sql = """INSERT INTO classes (c_classid, c_name, c_teacherid, c_numenrolled, c_capacity, c_time)
                    VALUES (?, ?, ?, ?, ?, ?)"""
            classes = ['PHYS ', 'MATH ', 'CSE ', 'CHEM ', 'BIO ']
            c_name = classes[random.randint(0,4)] + str(random.randint(1, 199))
            c_teacherid = random.randint(1,500)
            c_time = genClassTime()
            class_input = (i+1, c_name, c_teacherid, 0, 85, c_time)

            try:
                c = _conn.cursor()
                c.execute(sql, class_input)
                _conn.commit()
            except Error as e:
                errors = True
                print(e)
    if errors:
        print("Some errors ocurred...try again")
    else:
        print("Tables populated Successfully!!!")




def main():
    # api = Api(app)
    db = r"tpch.sqlite"
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)
    
    dropTables(conn)
    createTables(conn)
    populateTables(conn)

main()