from .person import Person
from exceptions.custom_exceptions import RequiredFieldException


class Student(Person):
    def __init__(self, ID: int, first_name: str, last_name: str, student_number: str, major: str, selected_courses: list = None):
        super().__init__(ID=ID, first_name=first_name, last_name=last_name)
        if student_number is None or not major:
            raise RequiredFieldException("فیلدهای شماره دانشجویی و رشته تحصیلی الزامی می‌باشند.")
        self.student_number = str(student_number)
        self.major = str(major)
        self.selected_courses = selected_courses if selected_courses is not None else []

    def select_course(self, course_code: str):
        course_code_str = str(course_code)
        if course_code_str not in self.selected_courses:
            self.selected_courses.append(course_code_str)

    def drop_course(self, course_code: str):
        course_code_str = str(course_code)
        if course_code_str in self.selected_courses:
            self.selected_courses.remove(course_code_str)

    def get_courses(self) -> list:
        return self.selected_courses

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "student_number": self.student_number,
            "major": self.major,
            "selected_courses": self.selected_courses
        })
        return base_dict
