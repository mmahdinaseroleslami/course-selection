from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError, HTTPException
import os
import sys

for stream in (sys.stdout, sys.stderr):
    if stream is not None and hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")

from routers.students import router as students_router
from routers.professors import router as professors_router
from routers.courses import router as courses_router
from exceptions.custom_exceptions import (
    CourseSelectionException,
    StudentNotFoundException,
    ProfessorNotFoundException,
    CourseNotFoundException,
)
from data.storage import (
    load_all,
    save_all,
    reset_storage,
    students_db,
    professors_db,
    courses_db,
)

FIELD_NAMES_FA = {
    "first_name": "نام",
    "last_name": "نام خانوادگی",
    "student_number": "شماره دانشجویی",
    "personnel_code": "شماره استادی (کد پرسنلی)",
    "department": "دانشکده",
    "major": "رشته تحصیلی",
    "code": "کد درس",
    "title": "عنوان درس",
    "unit": "تعداد واحد",
    "capacity": "ظرفیت",
}


def _translate_pydantic_error(err: dict) -> str:
    loc = err.get("loc", [])
    field = loc[-1] if loc else ""
    field_fa = FIELD_NAMES_FA.get(str(field), str(field))

    err_type = err.get("type", "")
    ctx = err.get("ctx", {})
    msg = err.get("msg", "")

    if "string_too_short" in err_type or "min_length" in err_type:
        min_l = ctx.get("min_length", 2)
        return f"فیلد «{field_fa}» باید حداقل {min_l} کاراکتر باشد."
    elif "string_too_long" in err_type or "max_length" in err_type:
        max_l = ctx.get("max_length")
        return f"فیلد «{field_fa}» نباید بیشتر از {max_l} کاراکتر باشد."
    elif "missing" in err_type:
        return f"وارد کردن فیلد «{field_fa}» الزامی است."
    elif "greater_than_equal" in err_type:
        ge = ctx.get("ge")
        return f"مقدار فیلد «{field_fa}» باید حداقل {ge} باشد."
    elif "less_than_equal" in err_type:
        le = ctx.get("le")
        return f"مقدار فیلد «{field_fa}» باید حداکثر {le} باشد."
    elif "int" in err_type or "number" in err_type:
        return f"مقدار فیلد «{field_fa}» باید عدد معتبر باشد."
    elif "string_pattern_mismatch" in err_type:
        if str(field) in ("first_name", "last_name"):
            return f"فیلد «{field_fa}» باید فقط شامل حروف باشد (بدون عدد یا علامت)."
        return f"فیلد «{field_fa}» نباید شامل فاصله باشد. لطفاً بدون فاصله وارد کنید."
    else:
        if "at least" in msg and "character" in msg:
            min_l = ctx.get("min_length", 2)
            return f"فیلد «{field_fa}» باید حداقل {min_l} کاراکتر باشد."
        return f"اطلاعات وارد شده برای «{field_fa}» معتبر نیست."


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("در حال بارگذاری داده‌های سیستم...")
    load_all()

    yield

    print("در حال ذخیره‌سازی داده‌های سیستم...")
    save_all()


app = FastAPI(
    title="سیستم انتخاب واحد دانشگاهی لرستان",
    description="پروژه پایانی درس برنامه‌نویسی پیشرفته - دکتر آرمین رشنو",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(students_router)
app.include_router(professors_router)
app.include_router(courses_router)


@app.exception_handler(CourseSelectionException)
async def custom_exception_handler(request: Request, exc: CourseSelectionException):
    if isinstance(exc, (StudentNotFoundException, ProfessorNotFoundException, CourseNotFoundException)):
        status_code = 404
    else:
        status_code = 400
    return JSONResponse(
        status_code=status_code,
        content={"detail": exc.message, "status": "error"}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    messages = [_translate_pydantic_error(e) for e in errors]
    detail_str = " | ".join(messages) if messages else "خطای اعتبارسنجی ورودی‌ها"
    return JSONResponse(
        status_code=422,
        content={"detail": detail_str, "errors": messages, "status": "error"}
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    msg = exc.detail
    if exc.status_code == 404:
        msg = "منبع مورد نظر یافت نشد."
    elif exc.status_code == 405:
        msg = "روش درخواست غیرمجاز است."
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": msg, "status": "error"}
    )



@app.get("/summary")
def api_get_summary():
    total_students = len(students_db)
    total_professors = len(professors_db)
    total_courses = len(courses_db)
    total_enrollments = sum(len(c.students) for c in courses_db.values())

    return {
        "university": "دانشگاه لرستان",
        "title": "سیستم جامع انتخاب واحد دانشگاهی",
        "total_students": total_students,
        "total_professors": total_professors,
        "total_courses": total_courses,
        "total_enrollments": total_enrollments,
        "status": "فعال"
    }


@app.get("/all-data")
def api_get_all_data():
    return {
        "students": [s.to_dict() for s in students_db.values()],
        "professors": [p.to_dict() for p in professors_db.values()],
        "courses": [c.to_dict() for c in courses_db.values()]
    }


@app.post("/reset-storage")
def api_reset_storage():
    reset_storage()
    return {"message": "تمام داده‌های ذخیره‌شده با موفقیت بازنشانی شدند."}


static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def read_root():
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "message": "خوش آمدید به سیستم انتخاب واحد دانشگاهی لرستان",
        "docs": "/docs",
        "summary": "/summary"
    }
