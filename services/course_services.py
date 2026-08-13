from models.course import Course
from schemas.course_schema import CourseCreate, CourseUpdate
from data.storage import courses_db, students_db, professors_db, save_all, increment_course_counter
from exceptions.custom_exceptions import CourseNotFoundException, DuplicateCourseException, InvalidCapacityException


def create_course(data: CourseCreate) -> Course:
    data.code = data.code.strip()

    if any(c.code.lower() == data.code.lower() for c in courses_db.values()):
        raise DuplicateCourseException(f"درسی با کد {data.code} قبلاً ثبت شده است.")

    course = Course(
        code=data.code,
        title=data.title,
        unit=data.unit,
        capacity=data.capacity,
        major=data.major
    )
    courses_db[course.code] = course
    increment_course_counter()
    save_all()
    return course


def get_all_courses() -> list[Course]:
    return list(courses_db.values())


def get_course_by_id(course_code: str) -> Course:
    course_code = course_code.strip()
    if course_code not in courses_db:
        raise CourseNotFoundException(f"درسی با کد {course_code} یافت نشد.")
    return courses_db[course_code]


def update_course(course_code: str, data: CourseUpdate) -> Course:
    course_code = course_code.strip()
    course = get_course_by_id(course_code)

    if data.capacity is not None and data.capacity < len(course.students):
        raise InvalidCapacityException(
            f"ظرفیت جدید ({data.capacity}) نمی‌تواند کمتر از تعداد دانشجویان ثبت‌نام‌شده ({len(course.students)}) باشد."
        )

    if data.code is not None:
        data.code = data.code.strip()
        if data.code != course_code:
            if any(c.code.lower() == data.code.lower() and c.code != course_code for c in courses_db.values()):
                raise DuplicateCourseException(f"درسی با کد {data.code} قبلاً ثبت شده است.")
            del courses_db[course_code]
            old_code = course.code
            course.code = data.code
            courses_db[course.code] = course
            for student in students_db.values():
                student.selected_courses = [data.code if c == old_code else c for c in student.selected_courses]
            if course.professor is not None:
                prof = course.professor
                prof.courses = [data.code if c == old_code else c for c in prof.courses]

    if data.title is not None:
        course.title = data.title
    if data.unit is not None:
        course.unit = data.unit
    if data.capacity is not None:
        course.capacity = data.capacity
    if data.major is not None:
        course.major = data.major

    save_all()
    return course


def delete_course(course_code: str) -> bool:
    course_code = course_code.strip()
    course = get_course_by_id(course_code)

    for student in students_db.values():
        if course_code in student.selected_courses:
            student.selected_courses.remove(course_code)

    course.remove_professor()

    del courses_db[course.code]
    save_all()
    return True
