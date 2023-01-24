--login query
select u_username, u_password
from users
where
    u_username = 'lyingHare0'
    AND u_password = 'fwmmnzufmx';


--print courses (for "Add Courses" tab, slide 5)
select c_name, t_name, c_time, c_numenrolled ||"/"|| c_capacity as students_enrolled
from classes,
     teachers
where 
    c_teacherid = t_teacherid
-- order by c_name asc


--print courses student is enrolled in
select c_name, t_name, c_time, c_numenrolled ||"/"|| c_capacity as students_enrolled
from classes,
     teachers,
     students,
     enrollment
where 
    s_studentid = e_studentid
    AND e_classid = c_classid
    AND c_teacherid = t_teacherid
-- order by c_name asc


--enroll student in class
update enrollment
set e_enrollmentid = row_number(),
    e_classid = 1,
    e_studentid = '',--FIX ME: Figure out how to enter this query
    e_grade = ''

--Sign up Student into a course
INSERT INTO enrollment
VALUES





--TEST QUERY
select * from users where u_userid = 2;