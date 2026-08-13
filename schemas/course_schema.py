from typing import Optional
from pydantic import BaseModel, Field


class CourseCreate(BaseModel):
    major: str = Field(..., min_length=2, max_length=80, description="رشته ارائه دهنده")
    title: str = Field(..., min_length=2, max_length=100, description="عنوان درس")
    code: str = Field(..., min_length=2, max_length=20, pattern=r"^[A-Za-z0-9\u0600-\u06FF_()-]+$", description="کد درس")
    unit: int = Field(..., ge=1, le=5, description="تعداد واحد (بین ۱ تا ۵)")
    capacity: int = Field(..., ge=1, le=200, description="ظرفیت درس (بین ۱ تا ۲۰۰)")


class CourseUpdate(BaseModel):
    major: Optional[str] = Field(None, min_length=2, max_length=80)
    title: Optional[str] = Field(None, min_length=2, max_length=100)
    code: Optional[str] = Field(None, min_length=2, max_length=20, pattern=r"^[A-Za-z0-9\u0600-\u06FF_()-]+$")
    unit: Optional[int] = Field(None, ge=1, le=5)
    capacity: Optional[int] = Field(None, ge=1, le=200)
