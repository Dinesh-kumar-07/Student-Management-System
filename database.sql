CREATE DATABASE IF NOT EXISTS student_management;
USE student_management;

CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    roll_no VARCHAR(30) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    phone VARCHAR(20),
    department VARCHAR(100) NOT NULL,
    year_level INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_code VARCHAR(30) NOT NULL UNIQUE,
    course_name VARCHAR(120) NOT NULL,
    credits INT NOT NULL,
    UNIQUE KEY uq_course_name (course_name)
);

CREATE TABLE IF NOT EXISTS grades (
    grade_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    grade VARCHAR(5) NOT NULL,
    marks DECIMAL(5,2),
    UNIQUE KEY uq_student_course_grade (student_id, course_id),
    CONSTRAINT fk_grade_student
        FOREIGN KEY (student_id)
        REFERENCES students(student_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_grade_course
        FOREIGN KEY (course_id)
        REFERENCES courses(course_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    classes_held INT NOT NULL DEFAULT 0,
    classes_attended INT NOT NULL DEFAULT 0,
    UNIQUE KEY uq_student_course_attendance (student_id, course_id),
    CONSTRAINT fk_att_student
        FOREIGN KEY (student_id)
        REFERENCES students(student_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_att_course
        FOREIGN KEY (course_id)
        REFERENCES courses(course_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE INDEX idx_students_roll_no ON students(roll_no);
CREATE INDEX idx_students_name ON students(name);
CREATE INDEX idx_students_department ON students(department);
CREATE INDEX idx_grades_student ON grades(student_id);
CREATE INDEX idx_attendance_student ON attendance(student_id);
