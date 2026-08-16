# Student Management System — Modern UI

A complete desktop Student Management System using Python, Tkinter and MySQL.

## UI changes

The new version:
- Removes the "Python • Tkinter • MySQL" text from the top-right.
- Uses a clean blue/purple modern color palette.
- Adds a modern application header.
- Uses card-style sections.
- Improves spacing and typography.
- Uses clearer Add, Update, Delete and Clear actions.
- Keeps the original functional modules.

## Modules

### Students
- Add
- Update
- Delete
- Clear
- Real-time search
- Student table

### Courses
- Add
- Update
- Delete
- Clear
- Course table

### Grades
- Save/update grade
- Delete grade
- Grade and marks
- Student/course relationship

### Attendance
- Save/update attendance
- Delete attendance
- Attendance percentage
- Student/course relationship

## Database

The project uses four normalized tables:

1. students
2. courses
3. grades
4. attendance

Foreign-key constraints, unique constraints and indexes are included.

## Installation

1. Install Python 3.10+.
2. Install MySQL Server.
3. Run `database.sql` in MySQL Workbench.
4. Open `app.py`.
5. Change:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_MYSQL_PASSWORD",
    "database": "student_management"
}
```

6. Install the dependency:

```bash
pip install -r requirements.txt
```

7. Start the application:

```bash
python app.py
```

## Important

Do not upload your actual MySQL password to GitHub. For a production application, use environment variables or a secure configuration file.
