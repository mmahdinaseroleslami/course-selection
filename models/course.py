from exceptions.custom_exceptions import AlreadyAssignedToSameProfessorException, CourseAlreadyHasProfessorException, CourseHasNoProfessorException, RequiredFieldException


class Course:
    def __init__(self, code: str, title: str, unit: int, capacity: int, major: str = "", professor=None, students: list = None):
        if not code or not title or unit is None or capacity is None:
            raise RequiredFieldException("کد، عنوان، تعداد واحد و ظرفیت درس الزامی می‌باشند.")
        self.code = str(code)
        self.title = str(title)
        self.unit = int(unit)
        self.capacity = int(capacity)
        self.major = str(major) if major else ""
        self.professor = professor
        self.students = students if students is not None else []

    def is_full(self) -> bool:
        return len(self.students) >= self.capacity

    def add_student(self, student_number) -> bool:
        sn = str(student_number)
        if self.is_full():
            return False
        if sn in self.students:
            return False
        self.students.append(sn)
        return True

    def remove_student(self, student_number) -> bool:
        sn = str(student_number)
        if sn in self.students:
            self.students.remove(sn)
            return True
        return False

    def assign_professor(self, professor):
        if self.professor is not None and self.professor.ID == professor.ID:
            raise AlreadyAssignedToSameProfessorException(
                f"درس {self.title} قبلاً به استاد {professor.get_full_name()} اختصاص داده شده است."
            )
        if self.professor is not None and self.professor.ID != professor.ID:
            raise CourseAlreadyHasProfessorException(
                f"درس {self.title} قبلاً استاد {self.professor.get_full_name()} را دارد."
            )
        self.professor = professor
        professor.assign_course(self.code)

    def replace_professor(self, new_professor):
        if self.professor is None:
            raise CourseHasNoProfessorException(
                f"درس {self.title} استادی ندارد. لطفاً از گزینه تخصیص استاد استفاده کنید."
            )
        if self.professor.ID == new_professor.ID:
            raise AlreadyAssignedToSameProfessorException(
                f"درس {self.title} قبلاً به استاد {new_professor.get_full_name()} اختصاص داده شده است."
            )
        old_professor = self.professor
        self.professor = new_professor
        if self.code in old_professor.courses:
            old_professor.courses.remove(self.code)
        new_professor.assign_course(self.code)

    def remove_professor(self):
        if self.professor is not None:
            prof = self.professor
            self.professor = None
            if self.code in prof.courses:
                prof.courses.remove(self.code)

    def to_dict(self) -> dict:
        return {
            "code": self.code,
            "title": self.title,
            "unit": self.unit,
            "capacity": self.capacity,
            "major": self.major,
            "professor": self.professor.personnel_code if self.professor else None,
            "professor_name": self.professor.get_full_name() if self.professor else None,
            "students": self.students,
            "enrolled_count": len(self.students),
            "is_full": self.is_full()
        }
