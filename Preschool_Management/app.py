from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from MySQLdb.cursors import DictCursor

app = Flask(__name__)

app.secret_key = "preschool123"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "preschool"

mysql = MySQL(app)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        cur = mysql.connection.cursor(DictCursor)
        cur.execute("""
            SELECT *
            FROM users
            WHERE email=%s
            AND password=%s
        """, (email, password))
        user = cur.fetchone()
        cur.close()
        if user:
            session["user_id"] = user["id"]
            session["user_name"] = user["full_name"]
            session["role"] = user["role"]

            if user["role"] == "admin":
                return redirect(url_for("admin"))
            elif user["role"] == "teacher":
                return redirect(url_for("teacher"))
            else:
                if user["status"] == "active":
                    return redirect(url_for("parent"))
                else:
                    return "Your account is waiting for admin approval."
        else:
            return "Invalid Email or Password"
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form["full_name"]
        email = request.form["email"]
        password = request.form["password"]
        cur = mysql.connection.cursor(DictCursor)
        cur.execute("""
            INSERT INTO users
            (full_name,email,password,role,status)
            VALUES
            (%s,%s,%s,'parent','pending')
        """, (full_name, email, password))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/admin")
def admin():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session["role"] != "admin":
        return redirect(url_for("login"))
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE role='teacher'
    """)
    teacher_count = cur.fetchone()[0]
    cur.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE role='parent'
    """)
    parent_count = cur.fetchone()[0]
    cur.execute("""
        SELECT COUNT(*)
        FROM students
    """)
    student_count = cur.fetchone()[0]
    cur.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE role='parent'
        AND status='pending'
    """)
    pending_count = cur.fetchone()[0]
    cur.close()
    return render_template(
        "admin.html",
        teacher_count=teacher_count,
        parent_count=parent_count,
        student_count=student_count,
        pending_count=pending_count
    )

@app.route("/teacher")
def teacher():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session["role"] != "teacher":
        return redirect(url_for("login"))
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT class_assigned
        FROM teachers
        WHERE user_id=%s
    """, (session["user_id"],))
    teacher_data = cur.fetchone()
    class_name = teacher_data["class_assigned"]
    cur.execute("""
        SELECT *
        FROM students
        WHERE class_name=%s
    """, (class_name,))
    students = cur.fetchall()
    cur.execute("""
        SELECT *
        FROM timetable
        WHERE class_name=%s
    """, (class_name,))
    timetable = cur.fetchall()
    cur.close()
    return render_template(
        "teacher.html",
        teacher_name=session["user_name"],
        class_name=class_name,
        students=students,
        timetable=timetable
    )

@app.route("/parent")
def parent():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session["role"] != "parent":
        return redirect(url_for("login"))
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT *
        FROM students
        WHERE parent_user_id=%s
    """, (session["user_id"],))
    student = cur.fetchone()
    if student:
            class_name = student["class_name"]
            cur.execute("""SELECT * FROM timetable
            WHERE class_name=%s
            """, (class_name,))
            timetable = cur.fetchall()
    else:
        timetable = []
    cur.close()

    return render_template(
        "parent.html",
        parent_name=session["user_name"],
        student=student,
        timetable=timetable
    )


@app.route("/register_teacher", methods=["GET", "POST"])
def register_teacher():

    if "user_id" not in session:
        return redirect(url_for("login"))
    if session["role"] != "admin":
        return redirect(url_for("login"))
    if request.method == "POST":
        full_name = request.form["full_name"]
        email = request.form["email"]
        password = request.form["password"]
        class_assigned = request.form["class_assigned"]
        cur = mysql.connection.cursor(DictCursor)
        cur.execute("""
            INSERT INTO users
            (full_name,email,password,role,status)
            VALUES
            (%s,%s,%s,'teacher','active')
        """, (full_name,email,password))
        mysql.connection.commit()
        user_id = cur.lastrowid
        cur.execute("""
            INSERT INTO teachers
            (user_id,class_assigned)
            VALUES
            (%s,%s)
        """, (user_id,class_assigned))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("admin"))
    return render_template("register_teacher.html")



@app.route("/approve_parent")
def approve_parent():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session["role"] != "admin":
        return redirect(url_for("login"))
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        SELECT *
        FROM users
        WHERE role='parent'
        AND status='pending'
    """)
    parents = cur.fetchall()
    cur.close()
    return render_template(
        "approve_parent.html",
        parents=parents
    )



@app.route("/approve/<int:id>")
def approve(id):
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        UPDATE users
        SET status='active'
        WHERE id=%s
    """, (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("approve_parent"))

@app.route("/reject/<int:id>")
def reject(id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session["role"] != "admin":
        return redirect(url_for("login"))
    cur = mysql.connection.cursor(DictCursor)
    cur.execute("""
        DELETE FROM users
        WHERE id=%s
    """, (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for("approve_parent"))


@app.route("/register_student", methods=["GET", "POST"])
def register_student():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session["role"] != "admin":
        return redirect(url_for("login"))
    cur = mysql.connection.cursor(DictCursor)
    if request.method == "POST":
        student_name = request.form["student_name"]
        dob = request.form["dob"]
        gender = request.form["gender"]
        class_name = request.form["class_name"]
        parent_user_id = request.form["parent_user_id"]
        cur.execute("""
            INSERT INTO students
            (student_name,dob,gender,class_name,parent_user_id)
            VALUES
            (%s,%s,%s,%s,%s)
        """,
        (
            student_name,
            dob,
            gender,
            class_name,
            parent_user_id
        ))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("admin"))
    cur.execute("""
        SELECT id,full_name
        FROM users
        WHERE role='parent'
        AND status='active'
    """)
    parents = cur.fetchall()
    cur.close()
    return render_template(
        "register_student.html",
        parents=parents
    )


@app.route("/timetable", methods=["GET", "POST"])
def timetable():
    if "user_id" not in session:
        return redirect(url_for("login"))
    if session["role"] != "admin":
        return redirect(url_for("login"))
    cur = mysql.connection.cursor(DictCursor)
    if request.method == "POST":
        class_name = request.form["class_name"]
        day = request.form["day_of_week"]
        period_1 = request.form["period_1"]
        period_2 = request.form["period_2"]
        period_3 = request.form["period_3"]
        period_4 = request.form["period_4"]
        period_5 = request.form["period_5"]
        period_6 = request.form["period_6"]
        cur.execute("""
            INSERT INTO timetable
            (
                class_name,
                day_of_week,
                period_1,
                period_2,
                period_3,
                period_4,
                period_5,
                period_6
            )
            VALUES
            (%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            class_name,
            day,
            period_1,
            period_2,
            period_3,
            period_4,
            period_5,
            period_6
        ))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("timetable"))
    cur.execute("""
        SELECT *
        FROM timetable
        ORDER BY class_name, day_of_week
    """)
    timetable = cur.fetchall()
    cur.close()
    return render_template(
        "timetable.html",
        timetable=timetable
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.errorhandler(404)
def page_not_found(error):
    return "<h2>404 - Page Not Found</h2>", 404


@app.errorhandler(500)
def internal_error(error):
    return "<h2>500 - Internal Server Error</h2>", 500


if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )