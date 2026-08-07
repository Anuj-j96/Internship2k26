<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>School Management System - README</title>

    <style>

        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 40px;
            color: #333;
        }

        h1 {
            color: #0d6efd;
        }

        h2 {
            color: #198754;
            border-bottom: 1px solid #ddd;
            padding-bottom: 5px;
        }

        h3 {
            color: #444;
        }

        code {
            background: #f4f4f4;
            padding: 3px 6px;
            border-radius: 4px;
        }

        pre {
            background: #f4f4f4;
            padding: 15px;
            border-radius: 6px;
            overflow-x: auto;
        }

        table {
            border-collapse: collapse;
            width: 100%;
            margin-top: 15px;
        }

        th,
        td {
            border: 1px solid #ccc;
            padding: 10px;
            text-align: left;
        }

        th {
            background: #0d6efd;
            color: white;
        }

        .note {
            background: #fff3cd;
            padding: 15px;
            border-left: 5px solid #ffc107;
            margin: 15px 0;
        }

    </style>

</head>

<body>

    <h1>School Management System</h1>

    <p>
        A simple web-based <strong>School Management System</strong>
        built using HTML, Bootstrap, Custom CSS, JavaScript,
        Python Flask, and MySQL.
    </p>

    <p>
        The project provides separate portals for
        <strong>Admin, Teacher, and Parent</strong> users.
    </p>


    <h2>Features</h2>

    <h3>Landing Page</h3>

    <ul>
        <li>School introduction</li>
        <li>School facilities and features</li>
        <li>Contact section</li>
        <li>Login button</li>
        <li>Register button</li>
    </ul>


    <h3>Login System</h3>

    <p>
        Users can log in using their email and password.
    </p>

    <ul>
        <li><strong>Admin</strong> → Admin Portal</li>
        <li><strong>Teacher</strong> → Teacher Portal</li>
        <li><strong>Parent</strong> → Parent Portal</li>
    </ul>

    <p>
        Parent accounts can remain pending until they are
        approved by the administrator.
    </p>


    <h3>Parent Registration</h3>

    <ul>
        <li>Parent can create an account.</li>
        <li>New parent accounts are initially pending.</li>
        <li>Admin can approve or reject the account.</li>
    </ul>


    <h3>Admin Portal</h3>

    <ul>
        <li>View total teachers</li>
        <li>View total parents</li>
        <li>View total students</li>
        <li>View pending parents</li>
        <li>Register teachers</li>
        <li>Approve parent accounts</li>
        <li>Reject parent accounts</li>
        <li>Register students</li>
        <li>Create timetable</li>
    </ul>


    <h3>Teacher Portal</h3>

    <ul>
        <li>View teacher information</li>
        <li>View assigned class</li>
        <li>View students in the assigned class</li>
        <li>View class timetable</li>
    </ul>


    <h3>Parent Portal</h3>

    <ul>
        <li>View parent's information</li>
        <li>View child/student information</li>
        <li>View date of birth</li>
        <li>View gender</li>
        <li>View class</li>
        <li>View timetable</li>
    </ul>

    <div class="note">
        <strong>Note:</strong>
        The user role is <strong>Parent</strong>, not Student.
        Student information is displayed inside the Parent Portal.
    </div>


    <h2>Technologies Used</h2>

    <ul>
        <li><strong>HTML5</strong> – Page structure</li>
        <li><strong>Bootstrap</strong> – Responsive UI</li>
        <li><strong>CSS3</strong> – Custom styling</li>
        <li><strong>JavaScript</strong> – Client-side functionality</li>
        <li><strong>Python</strong> – Backend programming</li>
        <li><strong>Flask</strong> – Web framework</li>
        <li><strong>MySQL</strong> – Database</li>
        <li><strong>Flask-MySQLdb</strong> – MySQL connection</li>
    </ul>


    <h2>Project Structure</h2>

    <pre>
School Management System/
│
├── app.py
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── admin.html
│   ├── teacher.html
│   ├── parent.html
│   ├── register_teacher.html
│   ├── register_student.html
│   ├── approve_parent.html
│   └── timetable.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── js/
│       └── script.js
│
└── README.html
    </pre>


    <h2>Database</h2>

    <p>
        The project uses MySQL as the database.
    </p>

    <h3>Main Tables</h3>

    <ul>
        <li><code>users</code> – Stores user login and role information</li>
        <li><code>teachers</code> – Stores teacher information</li>
        <li><code>students</code> – Stores student information</li>
        <li><code>timetable</code> – Stores class timetable information</li>
    </ul>


    <h2>Flask Configuration</h2>

    <p>
        MySQL connection settings are configured in
        <code>app.py</code>.
    </p>

    <pre>
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "preschool_db"
    </pre>


    <h2>Installation</h2>

    <h3>1. Check Python</h3>

    <pre>
python --version
    </pre>


    <h3>2. Install Required Packages</h3>

    <pre>
pip install flask
pip install flask-mysqldb
    </pre>


    <h3>3. Start MySQL</h3>

    <p>
        If you are using XAMPP:
    </p>

    <ol>
        <li>Open XAMPP</li>
        <li>Start Apache</li>
        <li>Start MySQL</li>
    </ol>


    <h3>4. Create Database</h3>

    <p>
        Open phpMyAdmin and create the database used by
        <code>app.py</code>.
    </p>

    <p>
        Run the SQL queries provided with the project to create
        the required tables and initial data.
    </p>


    <h3>5. Run the Application</h3>

    <pre>
python app.py
    </pre>

    <p>
        Open the following address in your browser:
    </p>

    <pre>
http://127.0.0.1:5000
    </pre>


    <h2>Login Flow</h2>

    <pre>
Landing Page
     │
     ├── Login
     │     │
     │     ├── Admin
     │     │      ↓
     │     │   Admin Portal
     │     │
     │     ├── Teacher
     │     │      ↓
     │     │   Teacher Portal
     │     │
     │     └── Parent
     │            ↓
     │        Parent Portal
     │
     └── Register
            ↓
       Parent Account
            ↓
         Pending
            ↓
      Admin Approval
            ↓
          Active
    </pre>


    <h2>User Roles</h2>

    <table>

        <tr>
            <th>Role</th>
            <th>Main Access</th>
        </tr>

        <tr>
            <td>Admin</td>
            <td>
                Manage teachers, parents, students and timetable
            </td>
        </tr>

        <tr>
            <td>Teacher</td>
            <td>
                View assigned class, students and timetable
            </td>
        </tr>

        <tr>
            <td>Parent</td>
            <td>
                View child/student information and timetable
            </td>
        </tr>

    </table>


    <h2>Important Notes</h2>

    <ul>
        <li>
            This project is intended as an academic project.
        </li>

        <li>
            Authentication is kept simple.
        </li>

        <li>
            Passwords are currently stored as plain database values.
        </li>

        <li>
            Production applications should use password hashing,
            validation, CSRF protection and stronger authorization.
        </li>
    </ul>


    <h2>Troubleshooting</h2>

    <h3>Flask does not start</h3>

    <pre>
pip install flask flask-mysqldb
    </pre>


    <h3>MySQL Connection Error</h3>

    <p>Check the following:</p>

    <ul>
        <li>MySQL is running</li>
        <li>Database name is correct</li>
        <li>MySQL username is correct</li>
        <li>MySQL password is correct</li>
        <li>MySQL configuration is correct</li>
    </ul>


    <h3>Template Not Found</h3>

    <p>
        Make sure all HTML files are inside the
        <code>templates</code> folder.
    </p>

    <pre>
templates/
    ├── index.html
    ├── login.html
    └── register.html
    </pre>


    <h3>Flask Routes</h3>

    <p>
        Use Flask routes instead of directly opening HTML files.
    </p>

    <p><strong>Recommended:</strong></p>

    <pre>
&lt;a href="{{ url_for('login') }}"&gt;Login&lt;/a&gt;
    </pre>

    <p><strong>Not recommended:</strong></p>

    <pre>
&lt;a href="login.html"&gt;Login&lt;/a&gt;
    </pre>


    <h2>Author</h2>

    <p>
        <strong>School Management System Project</strong>
    </p>

    <p>
        Built as an academic web development project using
        Flask and MySQL.
    </p>

</body>

</html>
