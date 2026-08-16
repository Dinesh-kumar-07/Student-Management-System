# Student Management System

A desktop GUI application built with **Python (Tkinter)** and **MySQL** to manage students, courses, grades, and attendance — all from a single, modern-styled interface.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-informational)
![MySQL](https://img.shields.io/badge/Database-MySQL-orange)

## Overview

Student Management System is a CRUD-based desktop application that lets administrators manage core academic records through a clean, tabbed interface with a custom modern theme (cards, styled forms, and a responsive layout). All data is persisted in a MySQL database with proper relational constraints between students, courses, grades, and attendance.

## Features

- **Student Management** — Add, update, delete, and search students by roll number, name, or department, with form validation and a live data table.
- **Course Management** — Maintain a catalog of courses with unique course codes, names, and credit values.
- **Grade Management** — Record and update grades/marks for a student against a specific course, linked via dropdown selectors.
- **Attendance Management** — Track classes held vs. classes attended per student, per course.
- **Data Integrity** — Foreign key constraints with cascading updates/deletes keep grades and attendance in sync with student and course records.
- **Modern UI** — Custom-styled Tkinter interface with a card-based layout, styled tabs, form placeholders, and inline status/error messages.

## Tech Stack

| Layer      | Technology                  |
|------------|------------------------------|
| GUI        | Python `tkinter` / `ttk`     |
| Database   | MySQL                        |
| Connector  | `mysql-connector-python`     |

## Project Structure

```
.
├── app.py            # Main application (GUI + database logic)
├── database.sql      # Database schema (tables, keys, indexes)
├── requirements.txt  # Python dependencies
└── README.md
```

## Database Schema

The `database.sql` file creates a `student_management` database with the following tables:

- **students** — student_id, roll_no, name, email, phone, department, year_level
- **courses** — course_id, course_code, course_name, credits
- **grades** — links a student and course with a grade/marks value
- **attendance** — links a student and course with classes held/attended counts

Foreign keys on `grades` and `attendance` reference `students` and `courses` with `ON DELETE CASCADE` / `ON UPDATE CASCADE`, and indexes are added on commonly queried columns (`roll_no`, `name`, `department`, `student_id`).

## Prerequisites

- Python 3.x
- MySQL Server (running locally or accessible remotely)
- `pip` for installing dependencies

## Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/<repo-name>.git
   cd <repo-name>
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database**

   Log in to MySQL and run the schema file:
   ```bash
   mysql -u root -p < database.sql
   ```
   This creates the `student_management` database and all required tables.

4. **Configure database credentials**

   Open `app.py` and update the `DB_CONFIG` dictionary with your own MySQL credentials:
   ```python
   DB_CONFIG = {
       "host": "localhost",
       "user": "your_mysql_username",
       "password": "your_mysql_password",
       "database": "student_management"
   }
   ```
   > ⚠️ **Note:** Avoid committing real database credentials to version control. Consider loading them from environment variables (e.g. using `python-dotenv`) for anything beyond local/demo use.

5. **Run the application**
   ```bash
   python app.py
   ```

## Usage

- Use the **tabs** at the top of the window to switch between Students, Courses, Grades, and Attendance.
- Fill in the form fields and use **Add / Update / Delete / Clear** actions to manage records.
- Use the **search bar** on the Students tab to quickly filter by roll number, name, or department.
- Grade and Attendance entries are linked to existing students and courses via dropdown selectors, so add students and courses first.

## Future Improvements

- Export student/grade/attendance reports (CSV/PDF)
- Role-based login (admin/faculty)
- Environment-based configuration for DB credentials
- Unit tests for database operations

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

**Dinesh Kumar G**
