from fastapi import APIRouter
from schemas.student_schema import StudentCreate, StudentUpdate
from schemas.response_models import StudentResponse, CourseResponse
from services.student_services import (
    create_student,
    get_all_students,
    get_student_by_id,
    update_student,
    delete_student
)
from services.selection_services import (
    select_course_for_student,
    drop_course_for_student,
    get_student_courses
)

router = APIRouter(prefix="/students", tags=["students"])


@router.post("/", status_code=201, response_model=StudentResponse)
def api_create_student(data: StudentCreate):
    student = create_student(data)
    return student.to_dict()


@router.get("/", response_model=list[StudentResponse])
def api_get_all_students():
    students = get_all_students()
    return [s.to_dict() for s in students]


@router.get("/{student_id}", response_model=StudentResponse)
def api_get_student(student_id: int):
    student = get_student_by_id(student_id)
    return student.to_dict()


@router.put("/{student_id}", response_model=StudentResponse)
def api_update_student(student_id: int, data: StudentUpdate):
    updated_student = update_student(student_id, data)
    return updated_student.to_dict()


@router.delete("/{student_id}")
def api_delete_student(student_id: int):
    delete_student(student_id)
    return {"message": "دانشجو با موفقیت حذف شد."}


@router.post("/{student_id}/select-course/{course_code}")
def api_select_course(student_id: int, course_code: str):
    result = select_course_for_student(student_id, course_code)
    return result


@router.delete("/{student_id}/drop-course/{course_code}")
def api_drop_course(student_id: int, course_code: str):
    result = drop_course_for_student(student_id, course_code)
    return result


@router.get("/{student_id}/courses", response_model=list[CourseResponse])
def api_get_student_courses(student_id: int):
    courses = get_student_courses(student_id)
    return [c.to_dict() for c in courses]
