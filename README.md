# Login Page – Python & SQLite
This project is a simple yet secure user registration and login (authentication) system developed using Python.
The application is console-based and uses an SQLite database.

🚀 Features

- User registration (sign up)
- User login (authentication)
- Secure password hashing with bcrypt
- Email format validation
- User active/inactive status control
- Activity logging system for user actions
- Persistent data storage with SQLite
- Modular and extensible class-based architecture

🗄️ Database Structure

- loginpage table
- id (INTEGER, PK)
- name
- surname
- nickname
- email (UNIQUE)
- password_hash
- is_active
- role (user / admin)
- logs table
- created_at
- updated_at
- userid
- update_subject

🔐 Security

- Passwords are never stored in plain text
- Passwords are hashed using bcrypt (one-way hashing)
- Authentication is performed using bcrypt.checkpw()
