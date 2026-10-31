import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random

# =====================================
# DATABASE
# =====================================

def connect_db():
    return sqlite3.connect("exam.db")


def create_database():
    con = connect_db()
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS questions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        option1 TEXT,
        option2 TEXT,
        option3 TEXT,
        option4 TEXT,
        answer INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS results(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student TEXT,
        total INTEGER,
        correct INTEGER,
        percentage REAL,
        status TEXT
    )
    """)

    cur.execute("SELECT COUNT(*) FROM questions")

    if cur.fetchone()[0] == 0:

        data = [
            ("What is Python?",
             "Programming Language", "Operating System",
             "Browser", "Database", 1),

            ("Which function displays output?",
             "input()", "print()", "show()", "display()", 2),

            ("Which symbol is used for comments?",
             "//", "#", "/* */", "--", 2),

            ("What is the full form of CPU?",
             "Central Processing Unit", "Computer Personal Unit",
             "Central Program Utility", "Control Processing Unit", 1),

            ("Which language is used for database queries?",
             "HTML", "CSS", "SQL", "Python", 3),

            ("Which data type stores True or False?",
             "String", "Integer", "Boolean", "Float", 3),

            ("Which keyword defines a function in Python?",
             "function", "def", "fun", "define", 2),

            ("Which of these is a loop?",
             "if", "else", "for", "print", 3),

            ("Which protocol is secure for websites?",
             "HTTP", "HTTPS", "FTP", "SMTP", 2),

            ("What does RAM stand for?",
             "Read Access Memory", "Random Access Memory",
             "Run Access Memory", "Read Automatic Memory", 2)
        ]

        cur.executemany("""
        INSERT INTO questions
        (question, option1, option2, option3, option4, answer)
        VALUES (?, ?, ?, ?, ?, ?)
        """, data)

    con.commit()
    con.close()


# =====================================
# MAIN APPLICATION
# =====================================

class OnlineExam:

    def __init__(self, root):

        self.root = root
        self.root.title("Online Examination System")
        self.root.geometry("900x650")
        self.root.configure(bg="#edf2f7")
        self.root.resizable(False, False)

        self.student_name = ""
        self.questions = []
        self.answers = {}
        self.current = 0
        self.remaining = 600
        self.timer_running = False

        self.show_home()

    # =================================
    # CLEAR WINDOW
    # =================================

    def clear(self):

        for widget in self.root.winfo_children():
            widget.destroy()

    # =================================
    # HEADER
    # =================================

    def header(self, title):

        top = tk.Frame(self.root, bg="#183153", height=80)
        top.pack(fill="x")

        tk.Label(
            top,
            text=title,
            font=("Arial", 23, "bold"),
            fg="white",
            bg="#183153"
        ).pack(pady=20)

    # =================================
    # HOME PAGE
    # =================================

    def show_home(self):

        self.clear()
        self.header("ONLINE EXAMINATION SYSTEM")

        frame = tk.Frame(self.root, bg="white", padx=50, pady=40)
        frame.place(relx=0.5, rely=0.55, anchor="center")

        tk.Label(
            frame,
            text="Welcome to Online Examination",
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#183153"
        ).pack(pady=20)

        tk.Label(
            frame,
            text="Enter Student Name",
            font=("Arial", 12),
            bg="white"
        ).pack()

        self.name_entry = tk.Entry(
            frame,
            font=("Arial", 14),
            width=30,
            bd=2
        )
        self.name_entry.pack(pady=15)

        tk.Button(
            frame,
            text="START EXAM",
            font=("Arial", 12, "bold"),
            bg="#2463a6",
            fg="white",
            width=22,
            command=self.start_exam
        ).pack(pady=10)

        tk.Button(
            frame,
            text="ADMIN LOGIN",
            font=("Arial", 12, "bold"),
            bg="#26936b",
            fg="white",
            width=22,
            command=self.admin_login
        ).pack(pady=10)

    # =================================
    # START EXAM
    # =================================

    def start_exam(self):

        name = self.name_entry.get().strip()

        if not name:
            messagebox.showwarning(
                "Warning", "Please enter your name"
            )
            return

        con = connect_db()
        cur = con.cursor()

        cur.execute("SELECT * FROM questions")
        all_questions = cur.fetchall()

        con.close()

        if not all_questions:
            messagebox.showerror(
                "Error", "No questions available"
            )
            return

        self.student_name = name

        self.questions = random.sample(
            all_questions,
            min(10, len(all_questions))
        )

        self.answers = {}
        self.current = 0
        self.remaining = 600

        self.show_question()
        self.timer_running = True
        self.update_timer()

    # =================================
    # EXAMINATION PAGE
    # =================================

    def show_question(self):

        self.clear()

        question = self.questions[self.current]

        top = tk.Frame(self.root, bg="#183153")
        top.pack(fill="x")

        tk.Label(
            top,
            text="ONLINE EXAMINATION",
            font=("Arial", 20, "bold"),
            bg="#183153",
            fg="white"
        ).pack(side="left", padx=25, pady=20)

        self.timer_label = tk.Label(
            top,
            text="10:00",
            font=("Arial", 18, "bold"),
            bg="#183153",
            fg="#ffcc55"
        )
        self.timer_label.pack(side="right", padx=30)

        frame = tk.Frame(
            self.root,
            bg="white",
            padx=35,
            pady=30
        )
        frame.pack(fill="both", expand=True, padx=35, pady=25)

        tk.Label(
            frame,
            text="Student: " + self.student_name,
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#183153"
        ).pack(anchor="w")

        tk.Label(
            frame,
            text=f"Question {self.current + 1} of {len(self.questions)}",
            font=("Arial", 12),
            bg="white"
        ).pack(anchor="w", pady=15)

        tk.Label(
            frame,
            text=question[1],
            font=("Arial", 17, "bold"),
            bg="white",
            wraplength=700,
            justify="left"
        ).pack(anchor="w", pady=25)

        self.selected = tk.IntVar(
            value=self.answers.get(question[0], 0)
        )

        for i in range(1, 5):

            tk.Radiobutton(
                frame,
                text=question[i + 1],
                variable=self.selected,
                value=i,
                font=("Arial", 13),
                bg="white",
                anchor="w",
                padx=15
            ).pack(fill="x", pady=8)

        navigation = tk.Frame(frame, bg="white")
        navigation.pack(side="bottom", fill="x", pady=15)

        if self.current > 0:

            tk.Button(
                navigation,
                text="PREVIOUS",
                bg="#607d8b",
                fg="white",
                font=("Arial", 11, "bold"),
                command=self.previous_question
            ).pack(side="left")

        if self.current < len(self.questions) - 1:

            tk.Button(
                navigation,
                text="NEXT",
                bg="#2463a6",
                fg="white",
                font=("Arial", 11, "bold"),
                command=self.next_question
            ).pack(side="right")

        tk.Button(
            navigation,
            text="SUBMIT EXAM",
            bg="#26936b",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.submit_exam
        ).pack(side="right", padx=15)

        self.update_timer_label()

    # =================================
    # SAVE ANSWER
    # =================================

    def save_answer(self):

        question_id = self.questions[self.current][0]

        self.answers[question_id] = self.selected.get()

    # =================================
    # NEXT QUESTION
    # =================================

    def next_question(self):

        self.save_answer()

        if self.current < len(self.questions) - 1:

            self.current += 1
            self.show_question()

    # =================================
    # PREVIOUS QUESTION
    # =================================

    def previous_question(self):

        self.save_answer()

        if self.current > 0:

            self.current -= 1
            self.show_question()

    # =================================
    # TIMER
    # =================================

    def update_timer(self):

        if not self.timer_running:
            return

        self.update_timer_label()

        if self.remaining <= 0:

            self.timer_running = False

            messagebox.showinfo(
                "Time Over",
                "Your examination time is over!"
            )

            self.save_answer()
            self.submit_exam()
            return

        self.remaining -= 1

        self.root.after(1000, self.update_timer)

    def update_timer_label(self):

        minutes = self.remaining // 60
        seconds = self.remaining % 60

        if hasattr(self, "timer_label"):

            self.timer_label.config(
                text=f"{minutes:02d}:{seconds:02d}"
            )

    # =================================
    # SUBMIT EXAM
    # =================================

    def submit_exam(self):

        self.save_answer()

        if self.timer_running:

            confirm = messagebox.askyesno(
                "Submit Examination",
                "Are you sure you want to submit?"
            )

            if not confirm:
                return

        self.timer_running = False

        correct = 0

        for question in self.questions:

            question_id = question[0]
            correct_answer = question[6]

            if self.answers.get(question_id) == correct_answer:
                correct += 1

        total = len(self.questions)

        percentage = (correct / total) * 100

        status = "PASS" if percentage >= 40 else "FAIL"

        con = connect_db()
        cur = con.cursor()

        cur.execute("""
        INSERT INTO results
        (student, total, correct, percentage, status)
        VALUES (?, ?, ?, ?, ?)
        """, (
            self.student_name,
            total,
            correct,
            percentage,
            status
        ))

        con.commit()
        con.close()

        self.show_result(total, correct, percentage, status)

    # =================================
    # RESULT PAGE
    # =================================

    def show_result(self, total, correct, percentage, status):

        self.clear()

        self.header("EXAMINATION RESULT")

        frame = tk.Frame(
            self.root,
            bg="white",
            padx=60,
            pady=35
        )
        frame.place(relx=0.5, rely=0.55, anchor="center")

        tk.Label(
            frame,
            text="Examination Completed!",
            font=("Arial", 22, "bold"),
            fg="#183153",
            bg="white"
        ).pack(pady=15)

        details = [
            ("Student Name", self.student_name),
            ("Total Questions", str(total)),
            ("Correct Answers", str(correct)),
            ("Wrong Answers", str(total - correct)),
            ("Percentage", f"{percentage:.2f}%"),
            ("Result", status)
        ]

        for label, value in details:

            tk.Label(
                frame,
                text=f"{label}: {value}",
                font=("Arial", 14, "bold"),
                bg="white",
                fg="#26936b" if label == "Result" and status == "PASS" else "#183153"
            ).pack(pady=7)

        tk.Button(
            frame,
            text="BACK TO HOME",
            bg="#2463a6",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.show_home
        ).pack(pady=20)

    # =================================
    # ADMIN LOGIN
    # =================================

    def admin_login(self):

        self.clear()
        self.header("ADMIN LOGIN")

        frame = tk.Frame(self.root, bg="white", padx=50, pady=35)
        frame.place(relx=0.5, rely=0.55, anchor="center")

        tk.Label(
            frame,
            text="Username",
            font=("Arial", 12),
            bg="white"
        ).pack()

        username = tk.Entry(frame, font=("Arial", 13))
        username.pack(pady=10)

        tk.Label(
            frame,
            text="Password",
            font=("Arial", 12),
            bg="white"
        ).pack()

        password = tk.Entry(
            frame,
            show="*",
            font=("Arial", 13)
        )
        password.pack(pady=10)

        def check_login():

            if (username.get() == "admin"
                    and password.get() == "admin123"):

                self.admin_dashboard()

            else:

                messagebox.showerror(
                    "Login Failed",
                    "Invalid Username or Password"
                )

        tk.Button(
            frame,
            text="LOGIN",
            bg="#26936b",
            fg="white",
            font=("Arial", 12, "bold"),
            command=check_login
        ).pack(pady=15)

        tk.Button(
            frame,
            text="BACK",
            command=self.show_home
        ).pack()

    # =================================
    # ADMIN DASHBOARD
    # =================================

    def admin_dashboard(self):

        self.clear()
        self.header("ADMIN DASHBOARD")

        frame = tk.Frame(self.root, bg="white")
        frame.pack(fill="both", expand=True, padx=30, pady=25)

        tk.Label(
            frame,
            text="Welcome Administrator",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#183153"
        ).pack(pady=15)

        tk.Button(
            frame,
            text="ADD NEW QUESTION",
            bg="#2463a6",
            fg="white",
            width=25,
            command=self.add_question
        ).pack(pady=12)

        tk.Button(
            frame,
            text="VIEW STUDENT RESULTS",
            bg="#26936b",
            fg="white",
            width=25,
            command=self.view_results
        ).pack(pady=12)

        tk.Button(
            frame,
            text="BACK TO HOME",
            bg="#607d8b",
            fg="white",
            width=25,
            command=self.show_home
        ).pack(pady=12)

    # =================================
    # ADD QUESTION
    # =================================

    def add_question(self):

        self.clear()
        self.header("ADD NEW QUESTION")

        frame = tk.Frame(self.root, bg="white", padx=35, pady=20)
        frame.place(relx=0.5, rely=0.55, anchor="center")

        entries = []

        fields = [
            "Question",
            "Option 1",
            "Option 2",
            "Option 3",
            "Option 4"
        ]

        for field in fields:

            tk.Label(
                frame,
                text=field,
                font=("Arial", 11, "bold"),
                bg="white"
            ).pack(anchor="w")

            entry = tk.Entry(frame, width=55, font=("Arial", 11))
            entry.pack(pady=5)

            entries.append(entry)

        tk.Label(
            frame,
            text="Correct Option",
            font=("Arial", 11, "bold"),
            bg="white"
        ).pack(anchor="w", pady=5)

        answer = ttk.Combobox(
            frame,
            values=["1", "2", "3", "4"],
            state="readonly",
            width=10
        )
        answer.pack(anchor="w")

        def save_question():

            values = [entry.get().strip() for entry in entries]

            if not all(values) or answer.get() not in ["1", "2", "3", "4"]:

                messagebox.showwarning(
                    "Warning",
                    "Please fill all fields"
                )
                return

            con = connect_db()
            cur = con.cursor()

            cur.execute("""
            INSERT INTO questions
            (question, option1, option2, option3, option4, answer)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (*values, int(answer.get())))

            con.commit()
            con.close()

            messagebox.showinfo(
                "Success",
                "Question Added Successfully!"
            )

            self.admin_dashboard()

        tk.Button(
            frame,
            text="SAVE QUESTION",
            bg="#26936b",
            fg="white",
            command=save_question
        ).pack(pady=15)

        tk.Button(
            frame,
            text="BACK",
            command=self.admin_dashboard
        ).pack()

    # =================================
    # VIEW RESULTS
    # =================================

    def view_results(self):

        self.clear()
        self.header("STUDENT RESULTS")

        frame = tk.Frame(self.root, bg="white")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        columns = (
            "Student", "Total", "Correct", "Percentage", "Status"
        )

        table = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
            height=17
        )

        for col in columns:

            table.heading(col, text=col)
            table.column(col, width=150, anchor="center")

        table.pack(fill="both", expand=True)

        con = connect_db()
        cur = con.cursor()

        cur.execute("SELECT * FROM results ORDER BY id DESC")

        for row in cur.fetchall():

            table.insert(
                "",
                "end",
                values=(
                    row[1],
                    row[2],
                    row[3],
                    f"{row[4]:.2f}%",
                    row[5]
                )
            )

        con.close()

        tk.Button(
            self.root,
            text="BACK TO DASHBOARD",
            bg="#2463a6",
            fg="white",
            command=self.admin_dashboard
        ).pack(pady=15)


# =====================================
# RUN PROGRAM
# =====================================

if __name__ == "__main__":

    create_database()

    root = tk.Tk()

    application = OnlineExam(root)

    root.mainloop()