from typing import Optional
from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50, pattern=r"^[^\W\d_]+(?: [^\W\d_]+)*$", description="نام دانشجو")
    last_name: str = Field(..., min_length=2, max_length=50, pattern=r"^[^\W\d_]+(?: [^\W\d_]+)*$", description="نام خانوادگی دانشجو")
    student_number: str = Field(..., min_length=3, max_length=20, pattern=r"^[A-Za-z0-9\u0600-\u06FF_()-]+$", description="شماره دانشجویی")
    major: str = Field(..., min_length=2, max_length=80, description="رشته تحصیلی")


class StudentUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=50, pattern=r"^[^\W\d_]+(?: [^\W\d_]+)*$")
    last_name: Optional[str] = Field(None, min_length=2, max_length=50, pattern=r"^[^\W\d_]+(?: [^\W\d_]+)*$")
    student_number: Optional[str] = Field(None, min_length=3, max_length=20, pattern=r"^[A-Za-z0-9\u0600-\u06FF_()-]+$")
    major: Optional[str] = Field(None, min_length=2, max_length=80)
