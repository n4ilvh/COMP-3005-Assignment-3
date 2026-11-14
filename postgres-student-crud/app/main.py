
# Import the CRUD functions from database.py
from database import (
    getAllStudents,
    addStudent,
    updateStudentEmail,
    deleteStudent
)


# Display the application's main menu
def display_menu():
    print("\n========== STUDENT DATABASE ==========")
    print("1. View all students")
    print("2. Add a student")
    print("3. Update student email")
    print("4. Delete a student")
    print("5. Exit")
    print("======================================")


# Run the application
def main():

    while True:
        display_menu()

        choice = input("Enter your choice (1-5): ")

        # READ: Display all students
        if choice == "1":
            getAllStudents()

        # CREATE: Add a new student
        elif choice == "2":
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            email = input("Enter email: ")
            enrollment_date = input("Enter enrollment date (YYYY-MM-DD): ")

            addStudent(first_name, last_name, email, enrollment_date)

        # UPDATE: Change a student's email
        elif choice == "3":
            try:
                student_id = int(input("Enter student ID: "))
                new_email = input("Enter new email: ")

                updateStudentEmail(student_id, new_email)

            except ValueError:
                print("Please enter a valid student ID.")

        # DELETE: Remove a student
        elif choice == "4":
            try:
                student_id = int(input("Enter student ID: "))

                deleteStudent(student_id)

            except ValueError:
                print("Please enter a valid student ID.")

        # EXIT: Close the application
        elif choice == "5":
            print("Exiting Student Database. Goodbye!")
            break

        else:
            print("Invalid choice. Please select 1-5.")


# Start the application
if __name__ == "__main__":
    main()
