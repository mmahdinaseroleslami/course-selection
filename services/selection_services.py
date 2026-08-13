from models.course import Course
from data.storage import save_all
from services.student_services import get_student_by_id
from services.professor_services import get_professor_by_id
from services.course_services import get_course_by_id
from exceptions.custom_exceptions import CapacityFullException, DuplicateCourseSelectionException, CourseNotFoundException, CourseNotSelectedException


def select_course_for_student(student_id: int, course_code: str) -> dict:
    course_code = course_code.strip()
    student = get_student_by_id(student_id)
    course = get_course_by_id(course_code)

    if course_code in student.selected_courses:
        raise DuplicateCourseSelectionException(f"درس {course.title} ({course_code}) قبلاً توسط دانشجو اخذ شده است.")

    if course.is_full():
        raise CapacityFullException(f"ظرفیت درس {course.title} ({course_code}) تکمیل است.")

    student.select_course(course_code)
    course.add_student(student.student_number)

    save_all()
    return {
        "message": f"درس {course.title} با موفقیت برای دانشجو {student.get_full_name()} اخذ شد.",
        "student_id": student.ID,
        "course_code": course.code
    }


def drop_course_for_student(student_id: int, course_code: str) -> dict:
    course_code = course_code.strip()
    student = get_student_by_id(student_id)
    course = get_course_by_id(course_code)

    if course_code not in student.selected_courses:
        raise CourseNotSelectedException(f"درس {course_code} در لیست دروس اخذ شده دانشجو وجود ندارد.")

    student.drop_course(course_code)
    course.remove_student(student.student_number)

    save_all()
    return {
        "message": f"درس {course.title} با موفقیت حذف شد.",
        "student_id": student.ID,
        "course_code": course.code
    }


def assign_professor_to_course(professor_id: int, course_code: str) -> dict:
    course_code = course_code.strip()
    professor = get_professor_by_id(professor_id)
    course = get_course_by_id(course_code)

    course.assign_professor(professor)

    save_all()
    return {
        "message": f"استاد {professor.get_full_name()} به عنوان مدرس درس {course.title} تعیین شد.",
        "professor_id": professor.ID,
        "course_code": course.code
    }


def replace_professor_in_course(professor_id: int, course_code: str) -> dict:
    course_code = course_code.strip()
    new_professor = get_professor_by_id(professor_id)
    course = get_course_by_id(course_code)
    old_professor_name = course.professor.get_full_name() if course.professor else None

    course.replace_professor(new_professor)

    save_all()
    return {
        "message": f"استاد درس {course.title} از {old_professor_name} به {new_professor.get_full_name()} تعویض شد.",
        "course_code": course.code,
        "old_professor": old_professor_name,
        "new_professor": new_professor.get_full_name()
    }


def get_student_courses(student_id: int) -> list[Course]:
    student = get_student_by_id(student_id)
    courses = []
    for code in student.selected_courses:
        try:
            courses.append(get_course_by_id(code))
        except CourseNotFoundException:
            continue
    return courses
