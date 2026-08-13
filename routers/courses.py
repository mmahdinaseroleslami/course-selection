from fastapi import APIRouter
from schemas.course_schema import CourseCreate, CourseUpdate
from schemas.response_models import CourseResponse
from services.course_services import (
    create_course,
    get_all_courses,
    get_course_by_id,
    update_course,
    delete_course
)

router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("/", status_code=201, response_model=CourseResponse)
def api_create_course(data: CourseCreate):
    course = create_course(data)
    return course.to_dict()


@router.get("/", response_model=list[CourseResponse])
def api_get_all_courses():
    courses = get_all_courses()
    return [c.to_dict() for c in courses]


@router.get("/{course_code}", response_model=CourseResponse)
def api_get_course(course_code: str):
    course = get_course_by_id(course_code)
    return course.to_dict()


@router.put("/{course_code}", response_model=CourseResponse)
def api_update_course(course_code: str, data: CourseUpdate):
    updated_course = update_course(course_code, data)
    return updated_course.to_dict()


@router.delete("/{course_code}")
def api_delete_course(course_code: str):
    delete_course(course_code)
    return {"message": "درس با موفقیت حذف شد."}
