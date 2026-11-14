
import os
import psycopg
from dotenv import load_dotenv

# Load database credentials from the .env file
load_dotenv()


# Establish a connection to the PostgreSQL database
def get_connection():
    try:
        connection = psycopg.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        return connection

    except psycopg.Error as error:
        print("Database connection failed:", error)
        return None


# READ: Retrieve and display all students
def getAllStudents():
    connection = get_connection()

    if connection is None:
        return

    try:
        with connection:
            with connection.cursor() as cursor:

                # Retrieve all student records
                cursor.execute("SELECT * FROM students ORDER BY student_id")

                # Fetch all results returned by the query
                students = cursor.fetchall()

                print("\n--- STUDENT RECORDS ---")

                if not students:
                    print("No students found.")
                else:
                    for student in students:
                        print(
                            f"ID: {student[0]} | "
                            f"Name: {student[1]} {student[2]} | "
                            f"Email: {student[3]} | "
                            f"Enrollment Date: {student[4]}"
                        )

                return students

    except psycopg.Error as error:
        print("Error retrieving students:", error)


# CREATE: Add a new student to the database
def addStudent(first_name, last_name, email, enrollment_date):
    connection = get_connection()

    if connection is None:
        return False

    try:
        with connection:
            with connection.cursor() as cursor:

                # Insert a new student using parameterized values
                cursor.execute(
                    """
                    INSERT INTO students
                    (first_name, last_name, email, enrollment_date)
                    VALUES (%s, %s, %s, %s)
                    RETURNING student_id
                    """,
                    (first_name, last_name, email, enrollment_date)
                )

                # Retrieve the automatically generated student ID
                student_id = cursor.fetchone()[0]

                print(f"Student successfully added! ID: {student_id}")
                return True

    except psycopg.Error as error:
        print("Error adding student:", error)
        return False


# UPDATE: Change the email address of an existing student
def updateStudentEmail(student_id, new_email):
    connection = get_connection()

    if connection is None:
        return False

    try:
        with connection:
            with connection.cursor() as cursor:

                # Update the email for the specified student
                cursor.execute(
                    """
                    UPDATE students
                    SET email = %s
                    WHERE student_id = %s
                    RETURNING student_id
                    """,
                    (new_email, student_id)
                )

                updated_student = cursor.fetchone()

                if updated_student:
                    print("Student email successfully updated!")
                    return True
                else:
                    print("Student ID not found.")
                    return False

    except psycopg.Error as error:
        print("Error updating student email:", error)
        return False


# DELETE: Remove a student from the database
def deleteStudent(student_id):
    connection = get_connection()

    if connection is None:
        return False

    try:
        with connection:
            with connection.cursor() as cursor:

                # Delete the student with the specified ID
                cursor.execute(
                    """
                    DELETE FROM students
                    WHERE student_id = %s
                    RETURNING student_id
                    """,
                    (student_id,)
                )

                deleted_student = cursor.fetchone()

                if deleted_student:
                    print("Student successfully deleted!")
                    return True
                else:
                    print("Student ID not found.")
                    return False

    except psycopg.Error as error:
        print("Error deleting student:", error)
        return False
