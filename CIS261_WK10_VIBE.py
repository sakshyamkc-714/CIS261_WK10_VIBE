"""CIS261 Week 10 - Student Grade Calculator."""


class Student:
	"""Store student information and calculate grade results."""

	def __init__(self, student_id, first_name, last_name, grades=None):
		self.student_id = student_id
		self.first_name = first_name
		self.last_name = last_name
		self.grades = grades if grades is not None else []

	@property
	def full_name(self):
		return f"{self.first_name} {self.last_name}"

	def average_grade(self):
		return sum(self.grades) / len(self.grades) if self.grades else 0.0

	def letter_grade(self):
		average = self.average_grade()
		if average >= 90:
			return "A"
		if average >= 80:
			return "B"
		if average >= 70:
			return "C"
		if average >= 60:
			return "D"
		return "F"

	def display(self):
		grades = ", ".join(f"{grade:.2f}" for grade in self.grades)
		return (
			f"ID: {self.student_id} | Name: {self.full_name} | "
			f"Grades: {grades or 'None'} | Average: {self.average_grade():.2f} | "
			f"Letter Grade: {self.letter_grade()}"
		)

	def to_file_line(self):
		grades = ",".join(str(grade) for grade in self.grades)
		return f"{self.student_id}|{self.first_name}|{self.last_name}|{grades}"


def get_number(prompt, minimum=None, maximum=None, whole_number=False):
	"""Read numeric input and retry when it is invalid or out of range."""
	while True:
		try:
			value = int(input(prompt)) if whole_number else float(input(prompt))
			if minimum is not None and value < minimum:
				print(f"Please enter a number of at least {minimum}.")
			elif maximum is not None and value > maximum:
				print(f"Please enter a number no greater than {maximum}.")
			else:
				return value
		except ValueError:
			print("Invalid numeric input. Please try again.")


def add_student(students):
	"""Prompt for a student and add it to the collection."""
	student_id = input("Enter student ID: ").strip()
	if not student_id:
		print("Student ID cannot be blank.")
		return
	if any(student.student_id == student_id for student in students):
		print("That student ID already exists.")
		return

	first_name = input("Enter first name: ").strip()
	last_name = input("Enter last name: ").strip()
	grade_count = get_number("How many grades? ", minimum=0, whole_number=True)
	grades = []
	for number in range(1, grade_count + 1):
		grades.append(get_number(f"Enter grade {number} (0-100): ", 0, 100))
	students.append(Student(student_id, first_name, last_name, grades))
	print("Student added successfully.")


def display_all_students(students):
	"""Display every student in the collection."""
	if not students:
		print("No student records found.")
		return
	print("\nAll Students\n------------")
	for student in students:
		print(student.display())


def search_student(students):
	"""Find and display one student by ID."""
	student_id = input("Enter student ID to search for: ").strip()
	for student in students:
		if student.student_id == student_id:
			print(student.display())
			return
	print("Student not found.")


def display_statistics(students):
	"""Display class size, averages, and letter-grade counts."""
	if not students:
		print("No student records found.")
		return
	averages = [student.average_grade() for student in students]
	letter_counts = {letter: 0 for letter in "ABCDF"}
	for student in students:
		letter_counts[student.letter_grade()] += 1
	print("\nClass Statistics\n----------------")
	print(f"Number of students: {len(students)}")
	print(f"Class average: {sum(averages) / len(averages):.2f}")
	print(f"Highest average: {max(averages):.2f}")
	print(f"Lowest average: {min(averages):.2f}")
	print("Letter grade counts: " + ", ".join(
		f"{letter}: {letter_counts[letter]}" for letter in "ABCDF"
	))


def save_records(students, filename="student_grades.txt"):
	"""Save student records as pipe-delimited text."""
	try:
		with open(filename, "w", encoding="utf-8") as file:
			for student in students:
				file.write(student.to_file_line() + "\n")
		print(f"Student records saved to {filename}.")
	except OSError as error:
		print(f"Unable to save records: {error}")


def load_records(filename="student_grades.txt"):
	"""Load student records from pipe-delimited text."""
	students = []
	try:
		with open(filename, "r", encoding="utf-8") as file:
			for line_number, line in enumerate(file, start=1):
				parts = line.strip().split("|")
				if len(parts) != 4:
					print(f"Skipping invalid record on line {line_number}.")
					continue
				student_id, first_name, last_name, grade_text = parts
				try:
					grades = [float(grade) for grade in grade_text.split(",") if grade]
				except ValueError:
					print(f"Skipping invalid grades on line {line_number}.")
					continue
				students.append(Student(student_id, first_name, last_name, grades))
		print(f"Loaded {len(students)} student record(s) from {filename}.")
	except FileNotFoundError:
		print(f"No file named {filename} was found.")
	except OSError as error:
		print(f"Unable to load records: {error}")
	return students


def display_menu():
	"""Display the available menu choices."""
	print("\nStudent Grade Calculator")
	print("1. Add a student")
	print("2. Display all students")
	print("3. Search for a student by student ID")
	print("4. Display class statistics")
	print("5. Save student records")
	print("6. Load student records")
	print("7. Exit")


def main():
	"""Run the student grade calculator menu."""
	students = []
	while True:
		display_menu()
		choice = input("Enter your choice (1-7): ").strip()
		if choice == "1":
			add_student(students)
		elif choice == "2":
			display_all_students(students)
		elif choice == "3":
			search_student(students)
		elif choice == "4":
			display_statistics(students)
		elif choice == "5":
			save_records(students)
		elif choice == "6":
			students = load_records()
		elif choice == "7":
			print("Goodbye!")
			break
		else:
			print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
	main()
