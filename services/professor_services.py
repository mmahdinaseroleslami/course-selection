from models.professor import Professor
from schemas.professor_schema import ProfessorCreate, ProfessorUpdate
from data.storage import professors_db, courses_db, save_all
import data.storage as data_storage
from exceptions.custom_exceptions import ProfessorNotFoundException, DuplicateProfessorException


def create_professor(data: ProfessorCreate) -> Professor:
    data.personnel_code = data.personnel_code.strip()

    for p in professors_db.values():
        if p.personnel_code.lower() == data.personnel_code.lower():
            raise DuplicateProfessorException(f"استادی با شماره پرسنلی {data.personnel_code} قبلاً ثبت شده است.")

    professor = Professor(
        ID=data_storage.PROFESSOR_COUNTER,
        first_name=data.first_name,
        last_name=data.last_name,
        personnel_code=data.personnel_code,
        department=data.department
    )
    professors_db[professor.ID] = professor
    data_storage.increment_professor_counter()
    save_all()
    return professor


def get_all_professors() -> list[Professor]:
    return list(professors_db.values())


def get_professor_by_id(professor_id: int) -> Professor:
    professor_id = int(professor_id)
    if professor_id not in professors_db:
        raise ProfessorNotFoundException(f"استادی با شناسه {professor_id} یافت نشد.")
    return professors_db[professor_id]


def update_professor(professor_id: int, data: ProfessorUpdate) -> Professor:
    professor = get_professor_by_id(professor_id)

    if data.personnel_code is not None:
        data.personnel_code = data.personnel_code.strip()
        if data.personnel_code != professor.personnel_code:
            for p in professors_db.values():
                if p.ID != professor.ID and p.personnel_code.lower() == data.personnel_code.lower():
                    raise DuplicateProfessorException(f"استادی با کد پرسنلی {data.personnel_code} قبلاً ثبت شده است.")
            professor.personnel_code = data.personnel_code

    if data.first_name is not None:
        professor.first_name = data.first_name
    if data.last_name is not None:
        professor.last_name = data.last_name
    if data.department is not None:
        professor.department = data.department

    save_all()
    return professor


def delete_professor(professor_id: int) -> bool:
    professor = get_professor_by_id(professor_id)

    for course in courses_db.values():
        if course.professor is not None and course.professor.ID == professor.ID:
            course.remove_professor()

    del professors_db[professor.ID]
    save_all()
    return True
