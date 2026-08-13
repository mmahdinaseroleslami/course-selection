from models.student import Student
from schemas.student_schema import StudentCreate, StudentUpdate
from data.storage import students_db, courses_db, save_all
import data.storage as data_storage
from exceptions.custom_exceptions import StudentNotFoundException, DuplicateStudentException


def create_student(data: StudentCreate) -> Student:
    data.student_number = data.student_number.strip()

    for s in students_db.values():
        if s.student_number.lower() == data.student_number.lower():
            raise DuplicateStudentException(f"دانشجویی با شماره دانشجویی {data.student_number} قبلاً ثبت شده است.")

    student = Student(
        ID=data_storage.STUDENT_COUNTER,
        first_name=data.first_name,
        last_name=data.last_name,
        student_number=data.student_number,
        major=data.major
    )
    students_db[student.ID] = student
    data_storage.increment_student_counter()
    save_all()
    return student


def get_all_students() -> list[Student]:
    return list(students_db.values())


def get_student_by_id(student_id: int) -> Student:
    student_id = int(student_id)
    if student_id not in students_db:
        raise StudentNotFoundException(f"دانشجویی با شناسه {student_id} یافت نشد.")
    return students_db[student_id]


def update_student(student_id: int, data: StudentUpdate) -> Student:
    student = get_student_by_id(student_id)

    if data.student_number is not None:
        data.student_number = data.student_number.strip()
        if data.student_number != student.student_number:
            for s in students_db.values():
                if s.ID != student.ID and s.student_number.lower() == data.student_number.lower():
                    raise DuplicateStudentException(f"دانشجویی با شماره {data.student_number} قبلاً ثبت شده است.")
            old_number = student.student_number
            student.student_number = data.student_number
            for course in courses_db.values():
                course.students = [data.student_number if s == old_number else s for s in course.students]

    if data.first_name is not None:
        student.first_name = data.first_name
    if data.last_name is not None:
        student.last_name = data.last_name
    if data.major is not None:
        student.major = data.major

    save_all()
    return student


def delete_student(student_id: int) -> bool:
    student = get_student_by_id(student_id)

    for course in courses_db.values():
        if student.student_number in course.students:
            course.students.remove(student.student_number)

    del students_db[student.ID]
    save_all()
    return True
