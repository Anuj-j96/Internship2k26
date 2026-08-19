from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from datetime import datetime, date
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change for production

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # your MySQL password
app.config['MYSQL_DB'] = 'student_attendance'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# -------------------- Login / Logout --------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s', (email, password))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['user_id'] = user['id']
            session['full_name'] = user['full_name']
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# -------------------- Dashboard --------------------
@app.route('/dashboard')
def dashboard():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Total students
    cursor.execute('SELECT COUNT(*) AS total FROM students')
    total_students = cursor.fetchone()['total']
    
    # Total classes
    cursor.execute('SELECT COUNT(*) AS total FROM classes')
    total_classes = cursor.fetchone()['total']
    
    # Today's date
    today = date.today().isoformat()
    cursor.execute('''
        SELECT 
            COUNT(CASE WHEN status = 'Present' THEN 1 END) AS present,
            COUNT(CASE WHEN status = 'Absent' THEN 1 END) AS absent
        FROM attendance
        WHERE attendance_date = %s
    ''', (today,))
    today_data = cursor.fetchone()
    present_today = today_data['present'] if today_data['present'] else 0
    absent_today = today_data['absent'] if today_data['absent'] else 0
    
    # Overall attendance percentage (all time)
    cursor.execute('SELECT COUNT(*) AS total FROM attendance')
    total_attendance = cursor.fetchone()['total']
    cursor.execute('SELECT COUNT(*) AS present FROM attendance WHERE status = "Present"')
    total_present = cursor.fetchone()['present']
    if total_attendance > 0:
        attendance_percentage = round((total_present / total_attendance) * 100, 2)
    else:
        attendance_percentage = 0
    
    return render_template('dashboard.html',
                           total_students=total_students,
                           total_classes=total_classes,
                           present_today=present_today,
                           absent_today=absent_today,
                           attendance_percentage=attendance_percentage)

# -------------------- Student Management --------------------
@app.route('/students')
def students():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''
        SELECT students.*, classes.class_name
        FROM students
        LEFT JOIN classes ON students.class_id = classes.id
        ORDER BY students.id
    ''')
    students_list = cursor.fetchall()
    return render_template('students.html', students=students_list)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id, class_name FROM classes ORDER BY class_name')
    classes = cursor.fetchall()
    
    if request.method == 'POST':
        name = request.form['student_name']
        roll = request.form['roll_no']
        email = request.form['email']
        contact = request.form['contact']
        class_id = request.form['class_id']
        
        cursor.execute('''
            INSERT INTO students (student_name, roll_no, email, contact, class_id)
            VALUES (%s, %s, %s, %s, %s)
        ''', (name, roll, email, contact, class_id))
        mysql.connection.commit()
        flash('Student added successfully.', 'success')
        return redirect(url_for('students'))
    
    return render_template('add_student.html', classes=classes)

@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if request.method == 'POST':
        name = request.form['student_name']
        roll = request.form['roll_no']
        email = request.form['email']
        contact = request.form['contact']
        class_id = request.form['class_id']
        
        cursor.execute('''
            UPDATE students
            SET student_name = %s, roll_no = %s, email = %s, contact = %s, class_id = %s
            WHERE id = %s
        ''', (name, roll, email, contact, class_id, id))
        mysql.connection.commit()
        flash('Student updated successfully.', 'success')
        return redirect(url_for('students'))
    
    cursor.execute('SELECT * FROM students WHERE id = %s', (id,))
    student = cursor.fetchone()
    cursor.execute('SELECT id, class_name FROM classes ORDER BY class_name')
    classes = cursor.fetchall()
    return render_template('edit_student.html', student=student, classes=classes)

@app.route('/delete_student/<int:id>')
def delete_student(id):
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM students WHERE id = %s', (id,))
    mysql.connection.commit()
    flash('Student deleted successfully.', 'success')
    return redirect(url_for('students'))

# -------------------- Class Management --------------------
@app.route('/classes')
def classes():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM classes ORDER BY class_name')
    classes_list = cursor.fetchall()
    return render_template('classes.html', classes=classes_list)

@app.route('/add_class', methods=['GET', 'POST'])
def add_class():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        class_name = request.form['class_name']
        description = request.form['description']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO classes (class_name, description) VALUES (%s, %s)', (class_name, description))
        mysql.connection.commit()
        flash('Class added successfully.', 'success')
        return redirect(url_for('classes'))
    return render_template('add_class.html')

@app.route('/edit_class/<int:id>', methods=['GET', 'POST'])
def edit_class(id):
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        class_name = request.form['class_name']
        description = request.form['description']
        cursor.execute('UPDATE classes SET class_name = %s, description = %s WHERE id = %s', (class_name, description, id))
        mysql.connection.commit()
        flash('Class updated successfully.', 'success')
        return redirect(url_for('classes'))
    
    cursor.execute('SELECT * FROM classes WHERE id = %s', (id,))
    class_data = cursor.fetchone()
    return render_template('edit_class.html', class_data=class_data)

@app.route('/delete_class/<int:id>')
def delete_class(id):
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM classes WHERE id = %s', (id,))
    mysql.connection.commit()
    flash('Class deleted successfully.', 'success')
    return redirect(url_for('classes'))

# -------------------- Attendance --------------------
@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id, class_name FROM classes ORDER BY class_name')
    classes = cursor.fetchall()
    
    students = []
    selected_class = None
    selected_date = date.today().isoformat()
    
    if request.method == 'POST':
        class_id = request.form.get('class_id')
        selected_date = request.form.get('attendance_date')
        
        if class_id and selected_date:
            cursor.execute('''
                SELECT s.*, 
                       COALESCE(a.status, '') AS status,
                       a.id AS attendance_id
                FROM students s
                LEFT JOIN attendance a ON s.id = a.student_id AND a.attendance_date = %s
                WHERE s.class_id = %s
                ORDER BY s.roll_no
            ''', (selected_date, class_id))
            students = cursor.fetchall()
            selected_class = class_id
    
    # Handle Save attendance
    if request.method == 'POST' and 'save_attendance' in request.form:
        class_id = request.form.get('class_id')
        selected_date = request.form.get('attendance_date')
        statuses = request.form.getlist('status')  # list of status for each student
        student_ids = request.form.getlist('student_id')
        
        for student_id, status in zip(student_ids, statuses):
            if status in ('Present', 'Absent'):
                # Check if record exists for this student and date
                cursor.execute('SELECT id FROM attendance WHERE student_id = %s AND attendance_date = %s', (student_id, selected_date))
                existing = cursor.fetchone()
                if existing:
                    cursor.execute('UPDATE attendance SET status = %s WHERE id = %s', (status, existing['id']))
                else:
                    cursor.execute('INSERT INTO attendance (student_id, attendance_date, status) VALUES (%s, %s, %s)',
                                   (student_id, selected_date, status))
        mysql.connection.commit()
        flash('Attendance saved successfully.', 'success')
        return redirect(url_for('attendance'))
    
    return render_template('attendance.html', classes=classes, students=students,
                           selected_class=selected_class, selected_date=selected_date)

# -------------------- Attendance Records --------------------
@app.route('/attendance_records', methods=['GET'])
def attendance_records():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    selected_date = request.args.get('date', date.today().isoformat())
    
    cursor.execute('''
        SELECT a.attendance_date, s.student_name, s.roll_no, c.class_name, a.status
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        LEFT JOIN classes c ON s.class_id = c.id
        WHERE a.attendance_date = %s
        ORDER BY s.roll_no
    ''', (selected_date,))
    records = cursor.fetchall()
    
    return render_template('attendance_records.html', records=records, selected_date=selected_date)

# -------------------- 404 Error Handler --------------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# -------------------- Run Application --------------------
if __name__ == '__main__':
    app.run(debug=True)