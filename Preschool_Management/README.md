# 🏫 Pre_School Management System

A simple web-based **Pre School Management System** developed using **Python Flask, MySQL, HTML5, Bootstrap, CSS, and JavaScript**.

The system provides separate portals for **Admin, Teacher, and Parent** users with role-based login and basic school management features.

---

# 📌 Features

## 🌐 Landing Page

- School introduction
- About the school
- School facilities
- Contact information
- Login option
- Registration option

## 🔐 Login System

Users log in using their email and password.

After successful login, users are redirected according to their role:

```text
Admin   → Admin Portal
Teacher → Teacher Portal
Parent  → Parent Portal
```

## 📝 Parent Registration

- Parents can create an account.
- New parent accounts are initially marked as **Pending**.
- Admin can approve or reject parent accounts.
- Approved parents can log in to the Parent Portal.

> **Note:** The user role is **Parent**, not Student. Student information is displayed inside the Parent Portal.

---

# 👨‍💼 Admin Portal

The Admin Portal allows the administrator to manage basic school information.

## Admin Features

- View total teachers
- View total parents
- View total students
- View pending parent accounts
- Register teachers
- Approve parent accounts
- Reject parent accounts
- Register students
- Create class timetable

---

# 👩‍🏫 Teacher Portal

The Teacher Portal allows teachers to view information related to their assigned class.

## Teacher Features

- View teacher information
- View assigned class
- View students in the assigned class
- View class timetable

---

# 👨‍👩‍👧 Parent Portal

The Parent Portal allows parents to view information about their child/student.

## Parent Features

- View parent information
- View student name
- View date of birth
- View gender
- View class
- View class timetable

---

# 🛠️ Technologies Used

|    Technology      |          Purpose           |
|--------------------|----------------------------|
|       HTML5        |      Web page structure    |
|     Bootstrap      |  Responsive user interface |
|       CSS3         |       Custom styling       |
|     JavaScript     |  Client-side functionality |
|       Python       |    Backend programming     |
|       Flask        |       Web framework        |
|       MySQL        |     Database management    |
|    Flask-MySQLdb   | Flask and MySQL connection |

---

# 📂 Project Structure

```text
School-Management-System/
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
├── database.txt
│
└── README.md
```

---

# 🗄️ Database

The application uses **MySQL** as its database.

## Main Tables

### `users`

Stores user login and account information.

Information includes:

- User ID
- Full name
- Email
- Password
- Role
- Account status

### `teachers`

Stores teacher-specific information.

### `students`

Stores student information and the relationship with the parent account.

### `timetable`

Stores class timetable information.

---

# ⚙️ Installation & Setup

## 1. Check Python

Make sure Python is installed on your computer.

```bash
python --version
```

## 2. Install Required Packages

Open CMD or Terminal inside the project folder.

```bash
pip install flask
```

```bash
pip install flask-mysqldb
```

Or install both together:

```bash
pip install Flask Flask-MySQLdb
```

## 3. Start XAMPP

If you are using XAMPP:

1. Open XAMPP Control Panel.
2. Start **Apache**.
3. Start **MySQL**.

## 4. Create the Database

Open phpMyAdmin:

```text
http://localhost/phpmyadmin
```

Create the database used by the application.

Then run the SQL queries provided in:

```text
database.txt
```

This will create the required tables and database records.

---

# 🔧 MySQL Configuration

The MySQL configuration is located inside `app.py`.

Example:

```python
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "preschool_db"
```

Change these values according to your local MySQL configuration.

---

# ▶️ Running the Project

Open CMD or Terminal inside the project directory.

Run:

```bash
python app.py
```

If the application starts successfully, Flask will display:

```text
Running on http://127.0.0.1:5000
```

Open the application in your browser:

```text
http://127.0.0.1:5000
```

---

# 🔄 Application Flow

```text
                    ┌─────────────────┐
                    │   Landing Page  │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │      Login      │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
          ┌───────┐      ┌─────────┐    ┌────────┐
          │ Admin │      │ Teacher │    │ Parent │
          └───┬───┘      └────┬────┘    └───┬────┘
              │               │              │
              ▼               ▼              ▼
        Admin Portal    Teacher Portal  Parent Portal
```

---

# 📝 Parent Registration Flow

```text
Parent Registration
        │
        ▼
  Pending Account
        │
        ▼
   Admin Reviews
      /     \
     /       \
 Approve    Reject
    │
    ▼
Active Account
    │
    ▼
Parent Portal
```

---

# 👥 User Roles

|  Role       |                 Main Access                      |
|-------------|--------------------------------------------------|
| **Admin**   | Manage teachers, parents, students and timetable |
| **Teacher** | View assigned class, students and timetable      |
| **Parent**  | View child/student information and timetable     |

---

# 🔗 Main Flask Routes

|       Route         |       Purpose        |
|---------------------|----------------------|
| `/`                 | Landing Page         |
| `/login`            | Login Page           |
| `/register`         | Parent Registration  |
| `/admin`            | Admin Portal         |
| `/teacher`          | Teacher Portal       |
| `/parent`           | Parent Portal        |
| `/register_teacher` | Register Teacher     |
| `/register_student` | Register Student     |
| `/approve_parent`   | View Pending Parents |
| `/approve/<id>`     | Approve Parent       |
| `/reject/<id>`      | Reject Parent        |
| `/timetable`        | Timetable Management |
| `/logout`           | Logout               |

---

# 🖥️ Main Pages

## Public Pages

- Landing Page
- Login Page
- Registration Page

## Admin Pages

- Admin Dashboard
- Teacher Registration
- Student Registration
- Parent Approval
- Timetable Management

## Teacher Pages

- Teacher Dashboard

## Parent Pages

- Parent Dashboard

---

# 🔐 Authentication

The application uses a simple role-based authentication system.

When a user logs in, the application checks the user's role.

```text
Email + Password
       │
       ▼
   Check User
       │
       ├── Admin
       │     ↓
       │  Admin Portal
       │
       ├── Teacher
       │     ↓
       │  Teacher Portal
       │
       └── Parent
             ↓
        Parent Portal
```

Parent accounts with a pending status cannot access the Parent Portal until the administrator approves the account.

---

# 🔗 Flask URL Handling

The project uses Flask routes instead of directly opening HTML files.

## Recommended

```html
<a href="{{ url_for('login') }}">Login</a>
```

## Not Recommended

```html
<a href="login.html">Login</a>
```

Using `url_for()` allows Flask to handle page routing properly.

---

# 📊 Basic CRUD Operations

The system demonstrates basic database operations.

## Create

- Register users
- Register teachers
- Register students
- Create timetable entries

## Read

- View users
- View teachers
- View students
- View timetable

## Update

- Approve parent accounts
- Update account information

## Delete

- Reject/remove pending parent accounts

---

# 📅 Timetable Management

The administrator can create timetable entries for classes.

The timetable can then be viewed by:

- Teachers
- Parents

Timetable information is stored in the MySQL database.

---

# ⚠️ Project Limitations

This project is designed primarily for **academic and demonstration purposes**.

The current implementation intentionally keeps the security system simple.

## Current Limitations

- Passwords are not hashed.
- Basic session authentication is used.
- Advanced permission management is not implemented.
- CSRF protection is not implemented.
- Input validation is basic.

For a real production school management system, stronger security features should be implemented.

---

# 🚀 Future Improvements

Possible future improvements include:

- Student attendance management
- Homework management
- Exam and marks management
- Parent-teacher communication
- School announcements
- Notifications
- Student performance tracking
- Teacher profile management
- Parent profile management
- Password reset
- Email verification
- Advanced search and filtering
- Improved mobile responsiveness
- Secure password hashing
- Advanced role-based permissions

---

# 📚 Academic Purpose

This project demonstrates practical implementation of:

- HTML5
- Bootstrap
- CSS3
- JavaScript
- Python
- Flask
- MySQL
- Database connectivity
- CRUD operations
- Flask routing
- Session handling
- User roles
- Database relationships

---

# 🧪 Testing

## Landing Page

Check that:

- Landing page opens correctly.
- Login button works.
- Register button works.

## Registration

Check that:

- Parent can register.
- Account is stored in the database.
- Account status is set to pending.

## Admin Login

Check that:

- Correct admin credentials open the Admin Portal.
- Incorrect credentials are rejected.

## Parent Approval

Check that:

- Pending parents appear in the Admin Portal.
- Admin can approve a parent.
- Admin can reject a parent.
- Approved parent can log in.

## Teacher

Check that:

- Teacher can log in.
- Teacher Portal opens.
- Assigned class is displayed.
- Students are displayed.
- Timetable is displayed.

## Parent

Check that:

- Parent can log in after approval.
- Student information is displayed.
- Timetable is displayed.

---

# 🐛 Troubleshooting

## Flask Does Not Start

Make sure the required packages are installed:

```bash
pip install flask flask-mysqldb
```

## MySQL Connection Error

Check:

- MySQL is running.
- Database name is correct.
- MySQL username is correct.
- MySQL password is correct.
- MySQL configuration in `app.py` is correct.

## Template Not Found

Make sure HTML files are inside the `templates` folder:

```text
templates/
│
├── index.html
├── login.html
├── register.html
└── ...
```

## Static Files Not Loading

Make sure CSS and JavaScript files are inside the `static` folder:

```text
static/
│
├── css/
│   └── style.css
│
└── js/
    └── script.js
```

Use Flask's `url_for()` for static files:

```html
<link rel="stylesheet"
      href="{{ url_for('static', filename='css/style.css') }}">
```

---

# 📁 Important Files

|      File       |         Purpose          |
|-----------------|--------------------------|
| `app.py`        | Main Flask backend       |
| `index.html`    | School landing page      |
| `login.html`    | Login page               |
| `register.html` | Parent registration      |
| `admin.html`    | Admin dashboard          |
| `teacher.html`  | Teacher dashboard        |
| `parent.html`   | Parent dashboard         |
| `style.css`     | Custom styling           |
| `script.js`     | JavaScript functionality |
| `database.txt`  | MySQL database queries   |
| `README.md`     | Project documentation    |

---

# 👨‍💻 Author

**Anuj Jamdar**

**School Management System**

Developed as an academic project using:

**Python • Flask • MySQL • HTML5 • Bootstrap • CSS3 • JavaScript**

---

# ⭐ Acknowledgement

This project was developed as an academic web development project to demonstrate the integration of **frontend, backend, and database technologies** into a simple School Management System.
