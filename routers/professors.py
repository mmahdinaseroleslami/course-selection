from fastapi import APIRouter
from schemas.professor_schema import ProfessorCreate, ProfessorUpdate
from schemas.response_models import ProfessorResponse
from services.professor_services import (
    create_professor,
    get_all_professors,
    get_professor_by_id,
    update_professor,
    delete_professor
)
from services.selection_services import assign_professor_to_course, replace_professor_in_course

router = APIRouter(prefix="/professors", tags=["professors"])


@router.post("/", status_code=201, response_model=ProfessorResponse)
def api_create_professor(data: ProfessorCreate):
    professor = create_professor(data)
    return professor.to_dict()


@router.get("/", response_model=list[ProfessorResponse])
def api_get_all_professors():
    professors = get_all_professors()
    return [p.to_dict() for p in professors]


@router.get("/{professor_id}", response_model=ProfessorResponse)
def api_get_professor(professor_id: int):
    professor = get_professor_by_id(professor_id)
    return professor.to_dict()


@router.put("/{professor_id}", response_model=ProfessorResponse)
def api_update_professor(professor_id: int, data: ProfessorUpdate):
    updated_prof = update_professor(professor_id, data)
    return updated_prof.to_dict()


@router.delete("/{professor_id}")
def api_delete_professor(professor_id: int):
    delete_professor(professor_id)
    return {"message": "استاد با موفقیت حذف شد."}


@router.post("/{professor_id}/assign-course/{course_code}")
def api_assign_course(professor_id: int, course_code: str):
    result = assign_professor_to_course(professor_id, course_code)
    return result


@router.post("/{professor_id}/replace-course/{course_code}")
def api_replace_course(professor_id: int, course_code: str):
    result = replace_professor_in_course(professor_id, course_code)
    return result
