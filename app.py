import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error


# ============================================================
# DATABASE CONFIGURATION
# ============================================================
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR DATABASE PASSWORD",
    "database": "student_management"
}


# ============================================================
# MODERN THEME
# ============================================================
BG = "#F6F8FC"
CARD = "#FFFFFF"
PRIMARY = "#5664F5"
PRIMARY_DARK = "#4351E8"
TEXT = "#172554"
MUTED = "#64748B"
BORDER = "#E2E8F0"
SUCCESS = "#16A34A"
DANGER = "#DC2626"
WARNING = "#D97706"
HEADER_BG = "#EEF1FF"
TAB_ACTIVE = "#5664F5"
TAB_TEXT = "#475569"


class Database:
    def __init__(self):
        self.conn = None
        self.connect()

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**DB_CONFIG)
        except Error as e:
            messagebox.showerror(
                "Database Connection Error",
                "Unable to connect to MySQL.\n\n"
                f"{e}\n\n"
                "Make sure MySQL is running and update DB_CONFIG in app.py."
            )

    def execute(self, query, params=(), fetch=False):
        if not self.conn or not self.conn.is_connected():
            self.connect()

        if not self.conn:
            return None

        cursor = self.conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params)

            if fetch:
                return cursor.fetchall()

            self.conn.commit()
            return cursor.lastrowid

        except Error:
            self.conn.rollback()
            raise
        finally:
            cursor.close()

    def close(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()


class ModernStudentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1450x850")
        self.root.minsize(1150, 700)
        self.root.configure(bg=BG)

        self.db = Database()

        self.selected_student_id = None
        self.selected_course_id = None

        self.setup_styles()
        self.build_header()
        self.build_notebook()
        self.build_students_tab()
        self.build_courses_tab()
        self.build_grades_tab()
        self.build_attendance_tab()
        self.build_status_bar()

        if self.db.conn:
            self.refresh_all()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    # ========================================================
    # STYLING
    # ========================================================

    def setup_styles(self):
        style = ttk.Style(self.root)

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            ".",
            background=BG,
            foreground=TEXT,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Modern.TNotebook",
            background=BG,
            borderwidth=0
        )

        style.configure(
            "Modern.TNotebook.Tab",
            background="#FFFFFF",
            foreground=TAB_TEXT,
            padding=(24, 12),
            font=("Segoe UI Semibold", 10),
            borderwidth=0
        )

        style.map(
            "Modern.TNotebook.Tab",
            background=[("selected", "#FFFFFF")],
            foreground=[("selected", PRIMARY)]
        )

        style.configure(
            "Modern.Treeview",
            background=CARD,
            fieldbackground=CARD,
            foreground=TEXT,
            rowheight=40,
            borderwidth=0,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Modern.Treeview.Heading",
            background="#EEF1FF",
            foreground="#34439B",
            relief="flat",
            font=("Segoe UI Semibold", 10)
        )

        style.map(
            "Modern.Treeview",
            background=[("selected", "#E7EAFF")],
            foreground=[("selected", TEXT)]
        )

        style.configure(
            "Modern.TCombobox",
            fieldbackground=CARD,
            background=CARD,
            foreground=TEXT,
            bordercolor=BORDER,
            padding=7
        )

        style.configure(
            "Modern.Vertical.TScrollbar",
            background="#E2E8F0",
            troughcolor="#F8FAFC",
            bordercolor="#F8FAFC",
            arrowcolor="#94A3B8"
        )

    # ========================================================
    # GENERAL UI HELPERS
    # ========================================================

    def card(self, parent, padding=18):
        frame = tk.Frame(
            parent,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1,
            bd=0
        )
        inner = tk.Frame(frame, bg=CARD)
        inner.pack(fill="both", expand=True, padx=padding, pady=padding)
        return frame, inner

    def label(self, parent, text, size=10, bold=False, color=TEXT):
        return tk.Label(
            parent,
            text=text,
            bg=CARD if parent.cget("bg") == CARD else parent.cget("bg"),
            fg=color,
            font=("Segoe UI", size, "bold" if bold else "normal")
        )

    def entry(self, parent, variable, placeholder=""):
        wrapper = tk.Frame(
            parent,
            bg="#FFFFFF",
            highlightbackground=BORDER,
            highlightthickness=1
        )
        entry = tk.Entry(
            wrapper,
            textvariable=variable,
            bg="#FFFFFF",
            fg=TEXT,
            insertbackground=PRIMARY,
            relief="flat",
            bd=0,
            font=("Segoe UI", 10)
        )
        entry.pack(fill="both", expand=True, padx=12, pady=9)

        if placeholder:
            self.add_placeholder(entry, placeholder)

        return wrapper

    def add_placeholder(self, entry, text):
        def on_focus_in(_):
            if entry.get() == text:
                entry.delete(0, "end")
                entry.config(fg=TEXT)

        def on_focus_out(_):
            if not entry.get():
                entry.insert(0, text)
                entry.config(fg="#94A3B8")

        entry.insert(0, text)
        entry.config(fg="#94A3B8")
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def button(self, parent, text, command, bg=PRIMARY, fg="white", width=None):
        kwargs = {
            "text": text,
            "command": command,
            "bg": bg,
            "fg": fg,
            "activebackground": PRIMARY_DARK if bg == PRIMARY else bg,
            "activeforeground": fg,
            "relief": "flat",
            "bd": 0,
            "cursor": "hand2",
            "font": ("Segoe UI Semibold", 10),
            "padx": 18,
            "pady": 9
        }

        if width:
            kwargs["width"] = width

        btn = tk.Button(parent, **kwargs)
        return btn

    def section_title(self, parent, text):
        frame = tk.Frame(parent, bg=CARD)
        frame.pack(fill="x", pady=(0, 14))

        tk.Frame(
            frame,
            bg=PRIMARY,
            width=4,
            height=22
        ).pack(side="left", padx=(0, 10))

        tk.Label(
            frame,
            text=text,
            bg=CARD,
            fg=PRIMARY_DARK,
            font=("Segoe UI Semibold", 13)
        ).pack(side="left")

        return frame

    def form_label(self, parent, text):
        tk.Label(
            parent,
            text=text,
            bg=CARD,
            fg=TEXT,
            font=("Segoe UI Semibold", 9)
        ).pack(anchor="w", pady=(0, 6))

    def empty_message(self, parent, text):
        tk.Label(
            parent,
            text=text,
            bg=CARD,
            fg=MUTED,
            font=("Segoe UI", 11)
        ).place(relx=0.5, rely=0.5, anchor="center")

    # ========================================================
    # HEADER
    # ========================================================

    def build_header(self):
        header = tk.Frame(self.root, bg=HEADER_BG, height=105)
        header.pack(fill="x")
        header.pack_propagate(False)

        content = tk.Frame(header, bg=HEADER_BG)
        content.pack(fill="both", expand=True, padx=32)

        logo = tk.Canvas(
            content,
            width=62,
            height=62,
            bg=HEADER_BG,
            highlightthickness=0
        )
        logo.pack(side="left", pady=20)
        logo.create_oval(2, 2, 60, 60, fill=PRIMARY, outline="")
        logo.create_text(
            31, 31,
            text="◆",
            fill="white",
            font=("Segoe UI", 23, "bold")
        )

        title_area = tk.Frame(content, bg=HEADER_BG)
        title_area.pack(side="left", padx=18)

        tk.Label(
            title_area,
            text="Student Management System",
            bg=HEADER_BG,
            fg=TEXT,
            font=("Segoe UI", 25, "bold")
        ).pack(anchor="w")

        tk.Label(
            title_area,
            text="Manage students, courses, grades and attendance",
            bg=HEADER_BG,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(2, 0))

    # ========================================================
    # NOTEBOOK
    # ========================================================

    def build_notebook(self):
        wrapper = tk.Frame(self.root, bg=BG)
        wrapper.pack(fill="both", expand=True, padx=24, pady=(18, 10))

        self.notebook = ttk.Notebook(
            wrapper,
            style="Modern.TNotebook"
        )
        self.notebook.pack(fill="both", expand=True)

        self.student_tab = tk.Frame(self.notebook, bg=BG)
        self.course_tab = tk.Frame(self.notebook, bg=BG)
        self.grade_tab = tk.Frame(self.notebook, bg=BG)
        self.attendance_tab = tk.Frame(self.notebook, bg=BG)

        self.notebook.add(self.student_tab, text="  Students  ")
        self.notebook.add(self.course_tab, text="  Courses  ")
        self.notebook.add(self.grade_tab, text="  Grades  ")
        self.notebook.add(self.attendance_tab, text="  Attendance  ")

    # ========================================================
    # STUDENTS
    # ========================================================

    def build_students_tab(self):
        top, form = self.card(self.student_tab)
        top.pack(fill="x", pady=(0, 15))

        self.section_title(form, "Student Details")

        grid = tk.Frame(form, bg=CARD)
        grid.pack(fill="x")

        self.roll_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.dept_var = tk.StringVar()
        self.year_var = tk.StringVar()

        fields = [
            ("Roll No", self.roll_var, "Enter roll number"),
            ("Name", self.name_var, "Enter student name"),
            ("Email", self.email_var, "Enter email address"),
            ("Phone", self.phone_var, "Enter phone number"),
            ("Department", self.dept_var, "Enter department"),
            ("Year", self.year_var, "Enter year")
        ]

        for i, (name, var, placeholder) in enumerate(fields):
            row = i // 2
            col = i % 2

            cell = tk.Frame(grid, bg=CARD)
            cell.grid(
                row=row,
                column=col,
                sticky="ew",
                padx=(0 if col == 0 else 16, 16 if col == 0 else 0),
                pady=(0, 13)
            )

            self.form_label(cell, name)
            self.entry(cell, var, placeholder).pack(fill="x")

        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        actions = tk.Frame(form, bg=CARD)
        actions.pack(fill="x", pady=(2, 0))

        self.button(
            actions, "＋  Add Student",
            self.add_student
        ).pack(side="left", padx=(0, 10))

        self.button(
            actions, "✎  Update",
            self.update_student,
            bg=SUCCESS
        ).pack(side="left", padx=10)

        self.button(
            actions, "♲  Delete",
            self.delete_student,
            bg=DANGER
        ).pack(side="left", padx=10)

        self.button(
            actions, "×  Clear",
            self.clear_student_form,
            bg="#E2E8F0",
            fg=TEXT
        ).pack(side="left", padx=10)

        table_card, table = self.card(self.student_tab, padding=14)
        table_card.pack(fill="both", expand=True)

        search_row = tk.Frame(table, bg=CARD)
        search_row.pack(fill="x", pady=(0, 12))

        tk.Label(
            search_row,
            text="Search",
            bg=CARD,
            fg=TEXT,
            font=("Segoe UI Semibold", 10)
        ).pack(side="left", padx=(0, 10))

        self.student_search_var = tk.StringVar()
        search_wrapper = self.entry(
            search_row,
            self.student_search_var,
            "Search by name, roll no, email, department..."
        )
        search_wrapper.pack(side="left", fill="x", expand=False)
        search_wrapper.configure(width=400)

        self.button(
            search_row,
            "⟳  Refresh",
            self.load_students,
            bg=PRIMARY
        ).pack(side="right")

        tree_frame = tk.Frame(table, bg=CARD)
        tree_frame.pack(fill="both", expand=True)

        columns = (
            "id", "roll", "name", "email",
            "phone", "department", "year"
        )

        self.student_tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            style="Modern.Treeview",
            selectmode="browse"
        )

        headings = {
            "id": "ID",
            "roll": "ROLL NO",
            "name": "NAME",
            "email": "EMAIL",
            "phone": "PHONE",
            "department": "DEPARTMENT",
            "year": "YEAR"
        }

        widths = {
            "id": 60,
            "roll": 140,
            "name": 190,
            "email": 250,
            "phone": 150,
            "department": 170,
            "year": 80
        }

        for col in columns:
            self.student_tree.heading(col, text=headings[col])
            self.student_tree.column(
                col,
                width=widths[col],
                anchor="center"
            )

        yscroll = ttk.Scrollbar(
            tree_frame,
            orient="vertical",
            command=self.student_tree.yview,
            style="Modern.Vertical.TScrollbar"
        )

        xscroll = ttk.Scrollbar(
            tree_frame,
            orient="horizontal",
            command=self.student_tree.xview
        )

        self.student_tree.configure(
            yscrollcommand=yscroll.set,
            xscrollcommand=xscroll.set
        )

        self.student_tree.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")

        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        self.student_tree.bind(
            "<<TreeviewSelect>>",
            self.on_student_select
        )

        self.student_search_var.trace_add(
            "write",
            lambda *_: self.search_students()
        )

    def validate_student(self):
        values = [
            self.roll_var.get().strip(),
            self.name_var.get().strip(),
            self.email_var.get().strip(),
            self.phone_var.get().strip(),
            self.dept_var.get().strip(),
            self.year_var.get().strip()
        ]

        roll, name, email, phone, dept, year = values

        if not roll or not name or not email or not dept or not year:
            messagebox.showwarning(
                "Validation",
                "Roll No, Name, Email, Department and Year are required."
            )
            return None

        if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
            messagebox.showwarning(
                "Validation",
                "Please enter a valid email address."
            )
            return None

        try:
            year = int(year)
            if year < 1 or year > 8:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Validation",
                "Year must be a number between 1 and 8."
            )
            return None

        if phone:
            allowed = "0123456789+-() "
            if any(ch not in allowed for ch in phone):
                messagebox.showwarning(
                    "Validation",
                    "Phone number contains invalid characters."
                )
                return None

        return roll, name, email, phone, dept, year

    def add_student(self):
        data = self.validate_student()
        if not data:
            return

        try:
            self.db.execute(
                """
                INSERT INTO students
                (roll_no, name, email, phone, department, year_level)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                data
            )

            messagebox.showinfo(
                "Success",
                "Student added successfully."
            )

            self.clear_student_form()
            self.refresh_all()

        except Error as e:
            self.show_db_error(e)

    def update_student(self):
        if not self.selected_student_id:
            messagebox.showwarning(
                "Selection",
                "Please select a student from the table first."
            )
            return

        data = self.validate_student()
        if not data:
            return

        try:
            self.db.execute(
                """
                UPDATE students
                SET roll_no=%s,
                    name=%s,
                    email=%s,
                    phone=%s,
                    department=%s,
                    year_level=%s
                WHERE student_id=%s
                """,
                data + (self.selected_student_id,)
            )

            messagebox.showinfo(
                "Success",
                "Student updated successfully."
            )

            self.clear_student_form()
            self.refresh_all()

        except Error as e:
            self.show_db_error(e)

    def delete_student(self):
        if not self.selected_student_id:
            messagebox.showwarning(
                "Selection",
                "Please select a student first."
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Delete this student?\n\n"
            "Related grades and attendance records will also be deleted."
        )

        if not confirm:
            return

        try:
            self.db.execute(
                "DELETE FROM students WHERE student_id=%s",
                (self.selected_student_id,)
            )

            messagebox.showinfo(
                "Success",
                "Student deleted successfully."
            )

            self.clear_student_form()
            self.refresh_all()

        except Error as e:
            self.show_db_error(e)

    def clear_student_form(self):
        self.selected_student_id = None

        for var in (
            self.roll_var,
            self.name_var,
            self.email_var,
            self.phone_var,
            self.dept_var,
            self.year_var
        ):
            var.set("")

        for item in self.student_tree.selection():
            self.student_tree.selection_remove(item)

    def load_students(self):
        if not self.db.conn:
            return

        try:
            rows = self.db.execute(
                """
                SELECT student_id,
                       roll_no,
                       name,
                       email,
                       phone,
                       department,
                       year_level
                FROM students
                ORDER BY student_id DESC
                """,
                fetch=True
            ) or []

            self.clear_tree(self.student_tree)

            for row in rows:
                self.student_tree.insert(
                    "",
                    "end",
                    values=(
                        row["student_id"],
                        row["roll_no"],
                        row["name"],
                        row["email"],
                        row["phone"] or "",
                        row["department"],
                        row["year_level"]
                    )
                )

            self.update_status(
                f"{len(rows)} student record(s)"
            )

        except Error as e:
            self.show_db_error(e)

    def search_students(self):
        if not self.db.conn:
            return

        term = self.student_search_var.get().strip()

        placeholder = "Search by name, roll no, email, department..."
        if term == placeholder:
            term = ""

        try:
            rows = self.db.execute(
                """
                SELECT student_id,
                       roll_no,
                       name,
                       email,
                       phone,
                       department,
                       year_level
                FROM students
                WHERE roll_no LIKE %s
                   OR name LIKE %s
                   OR email LIKE %s
                   OR department LIKE %s
                ORDER BY name
                """,
                (
                    f"%{term}%",
                    f"%{term}%",
                    f"%{term}%",
                    f"%{term}%"
                ),
                fetch=True
            ) or []

            self.clear_tree(self.student_tree)

            for row in rows:
                self.student_tree.insert(
                    "",
                    "end",
                    values=(
                        row["student_id"],
                        row["roll_no"],
                        row["name"],
                        row["email"],
                        row["phone"] or "",
                        row["department"],
                        row["year_level"]
                    )
                )

            self.update_status(
                f"{len(rows)} matching student record(s)"
            )

        except Error as e:
            self.show_db_error(e)

    def on_student_select(self, _event=None):
        selected = self.student_tree.selection()

        if not selected:
            return

        values = self.student_tree.item(
            selected[0],
            "values"
        )

        self.selected_student_id = int(values[0])

        self.roll_var.set(values[1])
        self.name_var.set(values[2])
        self.email_var.set(values[3])
        self.phone_var.set(values[4])
        self.dept_var.set(values[5])
        self.year_var.set(values[6])

    # ========================================================
    # COURSES
    # ========================================================

    def build_courses_tab(self):
        top, form = self.card(self.course_tab)
        top.pack(fill="x", pady=(0, 15))

        self.section_title(form, "Course Details")

        self.course_code_var = tk.StringVar()
        self.course_name_var = tk.StringVar()
        self.credits_var = tk.StringVar()

        grid = tk.Frame(form, bg=CARD)
        grid.pack(fill="x")

        fields = [
            ("Course Code", self.course_code_var, "Enter course code"),
            ("Course Name", self.course_name_var, "Enter course name"),
            ("Credits", self.credits_var, "Enter credits")
        ]

        for i, (name, var, placeholder) in enumerate(fields):
            cell = tk.Frame(grid, bg=CARD)
            cell.grid(
                row=0,
                column=i,
                sticky="ew",
                padx=(0, 16 if i < 2 else 0)
            )
            self.form_label(cell, name)
            self.entry(cell, var, placeholder).pack(fill="x")

        for i in range(3):
            grid.columnconfigure(i, weight=1)

        actions = tk.Frame(form, bg=CARD)
        actions.pack(fill="x", pady=(15, 0))

        self.button(
            actions, "＋  Add Course",
            self.add_course
        ).pack(side="left", padx=(0, 10))

        self.button(
            actions, "✎  Update",
            self.update_course,
            bg=SUCCESS
        ).pack(side="left", padx=10)

        self.button(
            actions, "♲  Delete",
            self.delete_course,
            bg=DANGER
        ).pack(side="left", padx=10)

        self.button(
            actions, "×  Clear",
            self.clear_course_form,
            bg="#E2E8F0",
            fg=TEXT
        ).pack(side="left", padx=10)

        table_card, table = self.card(self.course_tab, padding=14)
        table_card.pack(fill="both", expand=True)

        self.course_tree = ttk.Treeview(
            table,
            columns=("id", "code", "name", "credits"),
            show="headings",
            style="Modern.Treeview",
            selectmode="browse"
        )

        for col, title, width in [
            ("id", "ID", 80),
            ("code", "COURSE CODE", 200),
            ("name", "COURSE NAME", 500),
            ("credits", "CREDITS", 120)
        ]:
            self.course_tree.heading(col, text=title)
            self.course_tree.column(
                col,
                width=width,
                anchor="center"
            )

        self.course_tree.pack(fill="both", expand=True)
        self.course_tree.bind(
            "<<TreeviewSelect>>",
            self.on_course_select
        )

    def validate_course(self):
        code = self.course_code_var.get().strip()
        name = self.course_name_var.get().strip()
        credits = self.credits_var.get().strip()

        if not code or not name or not credits:
            messagebox.showwarning(
                "Validation",
                "All course fields are required."
            )
            return None

        try:
            credits = int(credits)
            if credits < 1 or credits > 10:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Validation",
                "Credits must be between 1 and 10."
            )
            return None

        return code, name, credits

    def add_course(self):
        data = self.validate_course()
        if not data:
            return

        try:
            self.db.execute(
                """
                INSERT INTO courses
                (course_code, course_name, credits)
                VALUES (%s, %s, %s)
                """,
                data
            )

            messagebox.showinfo(
                "Success",
                "Course added successfully."
            )

            self.clear_course_form()
            self.refresh_all()

        except Error as e:
            self.show_db_error(e)

    def update_course(self):
        if not self.selected_course_id:
            messagebox.showwarning(
                "Selection",
                "Please select a course first."
            )
            return

        data = self.validate_course()
        if not data:
            return

        try:
            self.db.execute(
                """
                UPDATE courses
                SET course_code=%s,
                    course_name=%s,
                    credits=%s
                WHERE course_id=%s
                """,
                data + (self.selected_course_id,)
            )

            messagebox.showinfo(
                "Success",
                "Course updated successfully."
            )

            self.clear_course_form()
            self.refresh_all()

        except Error as e:
            self.show_db_error(e)

    def delete_course(self):
        if not self.selected_course_id:
            messagebox.showwarning(
                "Selection",
                "Please select a course first."
            )
            return

        if not messagebox.askyesno(
            "Confirm Delete",
            "Delete this course?\n\n"
            "Related grades and attendance records will also be deleted."
        ):
            return

        try:
            self.db.execute(
                "DELETE FROM courses WHERE course_id=%s",
                (self.selected_course_id,)
            )

            messagebox.showinfo(
                "Success",
                "Course deleted successfully."
            )

            self.clear_course_form()
            self.refresh_all()

        except Error as e:
            self.show_db_error(e)

    def clear_course_form(self):
        self.selected_course_id = None
        self.course_code_var.set("")
        self.course_name_var.set("")
        self.credits_var.set("")

    def load_courses(self):
        if not self.db.conn:
            return

        try:
            rows = self.db.execute(
                """
                SELECT course_id,
                       course_code,
                       course_name,
                       credits
                FROM courses
                ORDER BY course_id DESC
                """,
                fetch=True
            ) or []

            self.clear_tree(self.course_tree)

            for row in rows:
                self.course_tree.insert(
                    "",
                    "end",
                    values=(
                        row["course_id"],
                        row["course_code"],
                        row["course_name"],
                        row["credits"]
                    )
                )

        except Error as e:
            self.show_db_error(e)

    def on_course_select(self, _event=None):
        selected = self.course_tree.selection()

        if not selected:
            return

        values = self.course_tree.item(
            selected[0],
            "values"
        )

        self.selected_course_id = int(values[0])
        self.course_code_var.set(values[1])
        self.course_name_var.set(values[2])
        self.credits_var.set(values[3])

    # ========================================================
    # GRADES
    # ========================================================

    def build_grades_tab(self):
        top, form = self.card(self.grade_tab)
        top.pack(fill="x", pady=(0, 15))

        self.section_title(form, "Grade Entry")

        self.grade_student_var = tk.StringVar()
        self.grade_course_var = tk.StringVar()
        self.grade_var = tk.StringVar()
        self.marks_var = tk.StringVar()

        grid = tk.Frame(form, bg=CARD)
        grid.pack(fill="x")

        self.grade_student_combo = self.create_combo(
            grid, "Student", self.grade_student_var, 0, 0
        )

        self.grade_course_combo = self.create_combo(
            grid, "Course", self.grade_course_var, 0, 1
        )

        self.grade_combo = self.create_combo(
            grid, "Grade", self.grade_var, 1, 0,
            values=("A+", "A", "B+", "B", "C", "D", "F")
        )

        marks_cell = tk.Frame(grid, bg=CARD)
        marks_cell.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(16, 0),
            pady=(0, 13)
        )

        self.form_label(marks_cell, "Marks")
        self.entry(
            marks_cell,
            self.marks_var,
            "Enter marks (0-100)"
        ).pack(fill="x")

        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        actions = tk.Frame(form, bg=CARD)
        actions.pack(fill="x", pady=(2, 0))

        self.button(
            actions,
            "✓  Save / Update Grade",
            self.save_grade
        ).pack(side="left", padx=(0, 10))

        self.button(
            actions,
            "♲  Delete",
            self.delete_grade,
            bg=DANGER
        ).pack(side="left", padx=10)

        self.button(
            actions,
            "×  Clear",
            self.clear_grade_form,
            bg="#E2E8F0",
            fg=TEXT
        ).pack(side="left", padx=10)

        table_card, table = self.card(self.grade_tab, padding=14)
        table_card.pack(fill="both", expand=True)

        self.grade_tree = ttk.Treeview(
            table,
            columns=("id", "student", "course", "grade", "marks"),
            show="headings",
            style="Modern.Treeview",
            selectmode="browse"
        )

        for col, title, width in [
            ("id", "ID", 80),
            ("student", "STUDENT", 330),
            ("course", "COURSE", 380),
            ("grade", "GRADE", 120),
            ("marks", "MARKS", 120)
        ]:
            self.grade_tree.heading(col, text=title)
            self.grade_tree.column(
                col,
                width=width,
                anchor="center"
            )

        self.grade_tree.pack(fill="both", expand=True)
        self.grade_tree.bind(
            "<<TreeviewSelect>>",
            self.on_grade_select
        )

    def create_combo(
        self,
        parent,
        title,
        variable,
        row,
        column,
        values=()
    ):
        cell = tk.Frame(parent, bg=CARD)
        cell.grid(
            row=row,
            column=column,
            sticky="ew",
            padx=(0 if column == 0 else 16, 16 if column == 0 else 0),
            pady=(0, 13)
        )

        self.form_label(cell, title)

        combo = ttk.Combobox(
            cell,
            textvariable=variable,
            values=values,
            state="readonly",
            style="Modern.TCombobox"
        )
        combo.pack(fill="x")

        return combo

    def save_grade(self):
        student_id = self.combo_id(
            self.grade_student_var.get()
        )
        course_id = self.combo_id(
            self.grade_course_var.get()
        )
        grade = self.grade_var.get().strip()
        marks_text = self.marks_var.get().strip()

        if not student_id or not course_id or not grade:
            messagebox.showwarning(
                "Validation",
                "Student, course and grade are required."
            )
            return

        try:
            marks = float(marks_text) if marks_text else None

            if marks is not None and not 0 <= marks <= 100:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Validation",
                "Marks must be between 0 and 100."
            )
            return

        try:
            self.db.execute(
                """
                INSERT INTO grades
                (student_id, course_id, grade, marks)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    grade=%s,
                    marks=%s
                """,
                (
                    student_id,
                    course_id,
                    grade,
                    marks,
                    grade,
                    marks
                )
            )

            messagebox.showinfo(
                "Success",
                "Grade saved successfully."
            )

            self.clear_grade_form()
            self.load_grades()

        except Error as e:
            self.show_db_error(e)

    def delete_grade(self):
        selected = self.grade_tree.selection()

        if not selected:
            messagebox.showwarning(
                "Selection",
                "Please select a grade record first."
            )
            return

        grade_id = self.grade_tree.item(
            selected[0],
            "values"
        )[0]

        if not messagebox.askyesno(
            "Confirm Delete",
            "Delete this grade record?"
        ):
            return

        try:
            self.db.execute(
                "DELETE FROM grades WHERE grade_id=%s",
                (grade_id,)
            )

            self.load_grades()
            self.clear_grade_form()

        except Error as e:
            self.show_db_error(e)

    def clear_grade_form(self):
        self.grade_student_var.set("")
        self.grade_course_var.set("")
        self.grade_var.set("")
        self.marks_var.set("")

    def load_grades(self):
        if not self.db.conn:
            return

        try:
            rows = self.db.execute(
                """
                SELECT
                    g.grade_id,
                    CONCAT(s.roll_no, ' - ', s.name) AS student,
                    CONCAT(c.course_code, ' - ', c.course_name) AS course,
                    g.grade,
                    g.marks
                FROM grades g
                JOIN students s
                    ON g.student_id = s.student_id
                JOIN courses c
                    ON g.course_id = c.course_id
                ORDER BY g.grade_id DESC
                """,
                fetch=True
            ) or []

            self.clear_tree(self.grade_tree)

            for row in rows:
                self.grade_tree.insert(
                    "",
                    "end",
                    values=(
                        row["grade_id"],
                        row["student"],
                        row["course"],
                        row["grade"],
                        "" if row["marks"] is None else row["marks"]
                    )
                )

        except Error as e:
            self.show_db_error(e)

    def on_grade_select(self, _event=None):
        selected = self.grade_tree.selection()

        if not selected:
            return

        grade_id = self.grade_tree.item(
            selected[0],
            "values"
        )[0]

        try:
            rows = self.db.execute(
                """
                SELECT student_id,
                       course_id,
                       grade,
                       marks
                FROM grades
                WHERE grade_id=%s
                """,
                (grade_id,),
                fetch=True
            )

            if not rows:
                return

            row = rows[0]

            self.select_combo_by_id(
                self.grade_student_combo,
                row["student_id"]
            )

            self.select_combo_by_id(
                self.grade_course_combo,
                row["course_id"]
            )

            self.grade_var.set(row["grade"])
            self.marks_var.set(
                "" if row["marks"] is None else str(row["marks"])
            )

        except Error as e:
            self.show_db_error(e)

    # ========================================================
    # ATTENDANCE
    # ========================================================

    def build_attendance_tab(self):
        top, form = self.card(self.attendance_tab)
        top.pack(fill="x", pady=(0, 15))

        self.section_title(form, "Attendance Entry")

        self.att_student_var = tk.StringVar()
        self.att_course_var = tk.StringVar()
        self.held_var = tk.StringVar()
        self.attended_var = tk.StringVar()

        grid = tk.Frame(form, bg=CARD)
        grid.pack(fill="x")

        self.att_student_combo = self.create_combo(
            grid,
            "Student",
            self.att_student_var,
            0,
            0
        )

        self.att_course_combo = self.create_combo(
            grid,
            "Course",
            self.att_course_var,
            0,
            1
        )

        held_cell = tk.Frame(grid, bg=CARD)
        held_cell.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 16),
            pady=(0, 13)
        )

        self.form_label(held_cell, "Classes Held")
        self.entry(
            held_cell,
            self.held_var,
            "Enter total classes"
        ).pack(fill="x")

        attended_cell = tk.Frame(grid, bg=CARD)
        attended_cell.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(16, 0),
            pady=(0, 13)
        )

        self.form_label(attended_cell, "Classes Attended")
        self.entry(
            attended_cell,
            self.attended_var,
            "Enter attended classes"
        ).pack(fill="x")

        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        actions = tk.Frame(form, bg=CARD)
        actions.pack(fill="x", pady=(2, 0))

        self.button(
            actions,
            "✓  Save / Update",
            self.save_attendance
        ).pack(side="left", padx=(0, 10))

        self.button(
            actions,
            "♲  Delete",
            self.delete_attendance,
            bg=DANGER
        ).pack(side="left", padx=10)

        self.button(
            actions,
            "×  Clear",
            self.clear_attendance_form,
            bg="#E2E8F0",
            fg=TEXT
        ).pack(side="left", padx=10)

        table_card, table = self.card(
            self.attendance_tab,
            padding=14
        )
        table_card.pack(fill="both", expand=True)

        self.att_tree = ttk.Treeview(
            table,
            columns=(
                "id",
                "student",
                "course",
                "held",
                "attended",
                "percentage"
            ),
            show="headings",
            style="Modern.Treeview",
            selectmode="browse"
        )

        for col, title, width in [
            ("id", "ID", 80),
            ("student", "STUDENT", 320),
            ("course", "COURSE", 370),
            ("held", "HELD", 100),
            ("attended", "ATTENDED", 120),
            ("percentage", "PERCENTAGE", 140)
        ]:
            self.att_tree.heading(col, text=title)
            self.att_tree.column(
                col,
                width=width,
                anchor="center"
            )

        self.att_tree.pack(fill="both", expand=True)

        self.att_tree.bind(
            "<<TreeviewSelect>>",
            self.on_attendance_select
        )

    def save_attendance(self):
        student_id = self.combo_id(
            self.att_student_var.get()
        )
        course_id = self.combo_id(
            self.att_course_var.get()
        )

        if not student_id or not course_id:
            messagebox.showwarning(
                "Validation",
                "Student and course are required."
            )
            return

        try:
            held = int(self.held_var.get().strip())
            attended = int(self.attended_var.get().strip())

            if held < 0 or attended < 0 or attended > held:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Validation",
                "Classes held and attended must be valid numbers, "
                "and attended cannot exceed held."
            )
            return

        try:
            self.db.execute(
                """
                INSERT INTO attendance
                (student_id, course_id, classes_held, classes_attended)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    classes_held=%s,
                    classes_attended=%s
                """,
                (
                    student_id,
                    course_id,
                    held,
                    attended,
                    held,
                    attended
                )
            )

            messagebox.showinfo(
                "Success",
                "Attendance saved successfully."
            )

            self.clear_attendance_form()
            self.load_attendance()

        except Error as e:
            self.show_db_error(e)

    def delete_attendance(self):
        selected = self.att_tree.selection()

        if not selected:
            messagebox.showwarning(
                "Selection",
                "Please select an attendance record first."
            )
            return

        attendance_id = self.att_tree.item(
            selected[0],
            "values"
        )[0]

        if not messagebox.askyesno(
            "Confirm Delete",
            "Delete this attendance record?"
        ):
            return

        try:
            self.db.execute(
                "DELETE FROM attendance WHERE attendance_id=%s",
                (attendance_id,)
            )

            self.load_attendance()
            self.clear_attendance_form()

        except Error as e:
            self.show_db_error(e)

    def clear_attendance_form(self):
        self.att_student_var.set("")
        self.att_course_var.set("")
        self.held_var.set("")
        self.attended_var.set("")

    def load_attendance(self):
        if not self.db.conn:
            return

        try:
            rows = self.db.execute(
                """
                SELECT
                    a.attendance_id,
                    CONCAT(s.roll_no, ' - ', s.name) AS student,
                    CONCAT(c.course_code, ' - ', c.course_name) AS course,
                    a.classes_held,
                    a.classes_attended,
                    CASE
                        WHEN a.classes_held = 0 THEN 0
                        ELSE ROUND(
                            (a.classes_attended / a.classes_held) * 100,
                            2
                        )
                    END AS percentage
                FROM attendance a
                JOIN students s
                    ON a.student_id = s.student_id
                JOIN courses c
                    ON a.course_id = c.course_id
                ORDER BY a.attendance_id DESC
                """,
                fetch=True
            ) or []

            self.clear_tree(self.att_tree)

            for row in rows:
                self.att_tree.insert(
                    "",
                    "end",
                    values=(
                        row["attendance_id"],
                        row["student"],
                        row["course"],
                        row["classes_held"],
                        row["classes_attended"],
                        f'{row["percentage"]}%'
                    )
                )

        except Error as e:
            self.show_db_error(e)

    def on_attendance_select(self, _event=None):
        selected = self.att_tree.selection()

        if not selected:
            return

        attendance_id = self.att_tree.item(
            selected[0],
            "values"
        )[0]

        try:
            rows = self.db.execute(
                """
                SELECT
                    student_id,
                    course_id,
                    classes_held,
                    classes_attended
                FROM attendance
                WHERE attendance_id=%s
                """,
                (attendance_id,),
                fetch=True
            )

            if not rows:
                return

            row = rows[0]

            self.select_combo_by_id(
                self.att_student_combo,
                row["student_id"]
            )

            self.select_combo_by_id(
                self.att_course_combo,
                row["course_id"]
            )

            self.held_var.set(row["classes_held"])
            self.attended_var.set(row["classes_attended"])

        except Error as e:
            self.show_db_error(e)

    # ========================================================
    # COMMON HELPERS
    # ========================================================

    def combo_id(self, value):
        if not value:
            return None

        try:
            return int(value.split("|")[0].strip())
        except (ValueError, IndexError):
            return None

    def select_combo_by_id(self, combo, record_id):
        prefix = f"{record_id} |"

        for value in combo["values"]:
            if value.startswith(prefix):
                combo.set(value)
                return

    def clear_tree(self, tree):
        for item in tree.get_children():
            tree.delete(item)

    def load_student_combos(self):
        if not self.db.conn:
            return

        try:
            rows = self.db.execute(
                """
                SELECT student_id, roll_no, name
                FROM students
                ORDER BY name
                """,
                fetch=True
            ) or []

            values = [
                f'{r["student_id"]} | {r["roll_no"]} | {r["name"]}'
                for r in rows
            ]

            self.grade_student_combo["values"] = values
            self.att_student_combo["values"] = values

        except Error as e:
            self.show_db_error(e)

    def load_course_combos(self):
        if not self.db.conn:
            return

        try:
            rows = self.db.execute(
                """
                SELECT course_id, course_code, course_name
                FROM courses
                ORDER BY course_code
                """,
                fetch=True
            ) or []

            values = [
                f'{r["course_id"]} | {r["course_code"]} | {r["course_name"]}'
                for r in rows
            ]

            self.grade_course_combo["values"] = values
            self.att_course_combo["values"] = values

        except Error as e:
            self.show_db_error(e)

    def refresh_all(self):
        self.load_students()
        self.load_courses()
        self.load_student_combos()
        self.load_course_combos()
        self.load_grades()
        self.load_attendance()

    def show_db_error(self, error):
        messagebox.showerror(
            "Database Error",
            str(error)
        )

    # ========================================================
    # STATUS BAR
    # ========================================================

    def build_status_bar(self):
        self.status_frame = tk.Frame(
            self.root,
            bg="#FFFFFF",
            height=36,
            highlightbackground=BORDER,
            highlightthickness=1
        )
        self.status_frame.pack(fill="x", side="bottom")
        self.status_frame.pack_propagate(False)

        self.status_var = tk.StringVar(
            value="Ready"
        )

        tk.Label(
            self.status_frame,
            textvariable=self.status_var,
            bg="#FFFFFF",
            fg=MUTED,
            font=("Segoe UI", 9)
        ).pack(side="left", padx=24)

        tk.Label(
            self.status_frame,
            text="Student Management System",
            bg="#FFFFFF",
            fg="#94A3B8",
            font=("Segoe UI", 9)
        ).pack(side="right", padx=24)

    def update_status(self, text):
        if hasattr(self, "status_var"):
            self.status_var.set(text)

    def on_close(self):
        self.db.close()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernStudentManagementSystem(root)
    root.mainloop()
