from .person import Person
from exceptions.custom_exceptions import RequiredFieldException


class Professor(Person):
    def __init__(self, ID: int, first_name: str, last_name: str, personnel_code: str, department: str, courses: list = None):
        super().__init__(ID=ID, first_name=first_name, last_name=last_name)
        if not personnel_code or not department:
            raise RequiredFieldException("فیلدهای شماره استادی و دانشکده الزامی می‌باشند.")
        self.personnel_code = str(personnel_code)
        self.department = str(department)
        self.courses = courses if courses is not None else []

    def assign_course(self, course_code: str):
        course_code_str = str(course_code)
        if course_code_str not in self.courses:
            self.courses.append(course_code_str)

    def get_courses(self) -> list:
        return self.courses

    def to_dict(self) -> dict:
        base_dict = super().to_dict()
        base_dict.update({
            "personnel_code": self.personnel_code,
            "department": self.department,
            "courses": self.courses
        })
        return base_dict
