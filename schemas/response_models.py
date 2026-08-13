from pydantic import BaseModel


class StudentResponse(BaseModel):
    ID: int
    first_name: str
    last_name: str
    full_name: str
    student_number: str
    major: str
    selected_courses: list[str]


class ProfessorResponse(BaseModel):
    ID: int
    first_name: str
    last_name: str
    full_name: str
    personnel_code: str
    department: str
    courses: list[str]


class CourseResponse(BaseModel):
    code: str
    title: str
    unit: int
    capacity: int
    major: str
    professor: str | None
    professor_name: str | None
    students: list[str]
    enrolled_count: int
    is_full: bool
