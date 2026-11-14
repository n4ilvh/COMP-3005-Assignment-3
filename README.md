# COMP 3005 Assignment 3: PostgreSQL CRUD Application

A command-line Python application that connects to a PostgreSQL database and performs CRUD (Create, Read, Update, Delete) operations on a `students` table.

**Demonstration video:** [ADD YOUR VIDEO LINK HERE]

## Technologies

- Python 3.10+
- PostgreSQL (with pgAdmin)
- `psycopg` (PostgreSQL driver) and `python-dotenv` (loads credentials from `.env`)

## Project Structure

```
.
├── postgres-student-crud/
│   ├── app/
│   │   ├── main.py          # Menu and user input
│   │   └── database.py      # Database connection and the four CRUD functions
│   └── database/
│       └── schema.sql       # Creates the students table and inserts the initial data
├── requirements.txt         # Python dependencies
├── .env.example             # Template for database credentials
└── README.md
```

## Database Schema

| Field | Type and Constraints |
|---|---|
| `student_id` | Integer, Primary Key, Auto-increment (`SERIAL`) |
| `first_name` | Text, Not Null |
| `last_name` | Text, Not Null |
| `email` | Text, Not Null, Unique |
| `enrollment_date` | Date |

`schema.sql` creates this table and inserts the three initial students (John Doe, Jane Smith, Jim Beam).

## Steps to Run the Application

Python is interpreted, so there is no compile step.

### 1. Clone the repository and install dependencies

```bash
git clone <REPOSITORY_URL>
cd <REPOSITORY_FOLDER>

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure credentials

Copy `.env.example` to `.env` in the project root and fill in your values:

```bash
cp .env.example .env
```

```
DB_HOST=127.0.0.1
DB_PORT=5433
DB_NAME=student_db
DB_USER=postgres
DB_PASSWORD=basketball727
```

`.env` is listed in `.gitignore`, so credentials are never committed.

### 3.: using the SCS OpenStack VM

The course VM only exposes ports 22 (SSH) and 80 (pgAdmin web), so Postgres is not directly reachable. Connect to the Carleton VPN, open an SSH tunnel, and leave that terminal running:

```bash
ssh -N -L 5433:127.0.0.1:5432 student@134.117.135.22
```

Then set `DB_HOST=127.0.0.1` and `DB_PORT=5433` in `.env`.

### 4. Run

```bash
python postgres-student-crud/app/main.py
```

Menu:

```
========== STUDENT DATABASE ==========
1. View all students
2. Add a student
3. Update student email
4. Delete a student
5. Exit
======================================
```

Enter the number of the operation you want. Dates are entered as `YYYY-MM-DD`.



## Functions (`postgres-student-crud/app/database.py`)

| Function | Operation | Description |
|---|---|---|
| `get_connection()` | Helper | Opens a connection using the credentials in `.env`. Returns `None` and prints an error if the connection fails. |
| `getAllStudents()` | Read | Runs `SELECT * FROM students ORDER BY student_id` and prints every record. |
| `addStudent(first_name, last_name, email, enrollment_date)` | Create | Inserts a new student and prints the auto-generated `student_id`. |
| `updateStudentEmail(student_id, new_email)` | Update | Changes the email of the student with the given ID. Reports if the ID does not exist. |
| `deleteStudent(student_id)` | Delete | Removes the student with the given ID. Reports if the ID does not exist. |

Design notes:
- All queries are parameterized (`%s`) to prevent SQL injection.
- Each function uses `with connection:`, so changes are committed on success and rolled back on error.
- Database errors (for example a duplicate email) are caught and printed instead of crashing the program.
- `main.py` validates that student IDs are numbers before calling the database functions.

## Troubleshooting

| Error | Likely cause |
|---|---|
| `Connection refused` | The SSH tunnel is not running, or the port in `.env` does not match. |
| `password authentication failed` | `DB_PASSWORD` does not match the Postgres password for `DB_USER`. |
| `database "student_db" does not exist` | Create the database first (Step 2). |
| `relation "students" does not exist` | Run `schema.sql` in `student_db`. |
| Connection times out | VPN is disconnected, or the floating IP has changed. |
