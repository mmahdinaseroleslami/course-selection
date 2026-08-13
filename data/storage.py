import json
import os
import sys
from models.student import Student
from models.professor import Professor
from models.course import Course
from exceptions.custom_exceptions import RequiredFieldException

for stream in (sys.stdout, sys.stderr):
    if stream is not None and hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")

DATA_DIR = os.path.dirname(os.path.abspath(__file__))
STUDENTS_FILE = os.path.join(DATA_DIR, "students.json")
PROFESSORS_FILE = os.path.join(DATA_DIR, "professors.json")
COURSES_FILE = os.path.join(DATA_DIR, "courses.json")

STUDENT_COUNTER = 1
PROFESSOR_COUNTER = 1
COURSE_COUNTER = 1

students_db: dict[int, Student] = {}
professors_db: dict[int, Professor] = {}
courses_db: dict[str, Course] = {}


def _read_json(filepath: str):
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except Exception as e:
        print(f"خطا در خواندن فایل {filepath}: {e}")
        return []


def _write_json(data, filepath: str):
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"خطا در نوشتن در فایل {filepath}: {e}")


def save_all():
    global students_db, professors_db, courses_db

    students_data = [student.to_dict() for student in students_db.values()]
    professors_data = [prof.to_dict() for prof in professors_db.values()]
    courses_data = [course.to_dict() for course in courses_db.values()]

    _write_json(students_data, STUDENTS_FILE)
    _write_json(professors_data, PROFESSORS_FILE)
    _write_json(courses_data, COURSES_FILE)


def load_all():
    global students_db, professors_db, courses_db, STUDENT_COUNTER, PROFESSOR_COUNTER, COURSE_COUNTER

    students_db.clear()
    professors_db.clear()
    courses_db.clear()

    raw_students = _read_json(STUDENTS_FILE)
    for s_dict in raw_students:
        if not isinstance(s_dict, dict):
            continue
        try:
            student = Student(
                ID=s_dict.get("ID", 0),
                first_name=s_dict.get("first_name", ""),
                last_name=s_dict.get("last_name", ""),
                student_number=s_dict.get("student_number", ""),
                major=s_dict.get("major", ""),
                selected_courses=s_dict.get("selected_courses", [])
            )
            students_db[student.ID] = student
        except (ValueError, RequiredFieldException) as e:
            print(f"رد کردن رکورد دانشجوی ناقص: {e}")
    if students_db:
        STUDENT_COUNTER = max(students_db.keys()) + 1
    else:
        STUDENT_COUNTER = 1

    raw_professors = _read_json(PROFESSORS_FILE)
    for p_dict in raw_professors:
        if not isinstance(p_dict, dict):
            continue
        try:
            professor = Professor(
                ID=p_dict.get("ID", 0),
                first_name=p_dict.get("first_name", ""),
                last_name=p_dict.get("last_name", ""),
                personnel_code=p_dict.get("personnel_code", ""),
                department=p_dict.get("department", ""),
                courses=p_dict.get("courses", [])
            )
            professors_db[professor.ID] = professor
        except (ValueError, RequiredFieldException) as e:
            print(f"رد کردن رکورد استاد ناقص: {e}")
    if professors_db:
        PROFESSOR_COUNTER = max(professors_db.keys()) + 1
    else:
        PROFESSOR_COUNTER = 1

    raw_courses = _read_json(COURSES_FILE)
    for c_dict in raw_courses:
        if not isinstance(c_dict, dict):
            continue
        try:
            professor_obj = None
            professor_code = c_dict.get("professor", None)
            if professor_code:
                for p in professors_db.values():
                    if p.personnel_code == professor_code:
                        professor_obj = p
                        break

            course = Course(
                code=c_dict.get("code", ""),
                title=c_dict.get("title", ""),
                unit=c_dict.get("unit", 3),
                capacity=c_dict.get("capacity", 30),
                major=c_dict.get("major", ""),
                professor=professor_obj,
                students=c_dict.get("students", [])
            )
            courses_db[course.code] = course
        except (ValueError, RequiredFieldException) as e:
            print(f"رد کردن رکورد درس ناقص: {e}")
    if courses_db:
        COURSE_COUNTER = len(courses_db) + 1
    else:
        COURSE_COUNTER = 1


def increment_student_counter():
    global STUDENT_COUNTER
    STUDENT_COUNTER += 1
    return STUDENT_COUNTER


def increment_professor_counter():
    global PROFESSOR_COUNTER
    PROFESSOR_COUNTER += 1
    return PROFESSOR_COUNTER


def increment_course_counter():
    global COURSE_COUNTER
    COURSE_COUNTER += 1
    return COURSE_COUNTER


def reset_storage():
    global students_db, professors_db, courses_db, STUDENT_COUNTER, PROFESSOR_COUNTER, COURSE_COUNTER
    students_db.clear()
    professors_db.clear()
    courses_db.clear()
    STUDENT_COUNTER = 1
    PROFESSOR_COUNTER = 1
    COURSE_COUNTER = 1

    _write_json([], STUDENTS_FILE)
    _write_json([], PROFESSORS_FILE)
    _write_json([], COURSES_FILE)
