from typing import Optional
from pydantic import BaseModel, Field


class ProfessorCreate(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=50, pattern=r"^[^\W\d_]+(?: [^\W\d_]+)*$", description="نام استاد")
    last_name: str = Field(..., min_length=2, max_length=50, pattern=r"^[^\W\d_]+(?: [^\W\d_]+)*$", description="نام خانوادگی استاد")
    personnel_code: str = Field(..., min_length=3, max_length=20, pattern=r"^[A-Za-z0-9\u0600-\u06FF_()-]+$", description="شماره استادی")
    department: str = Field(..., min_length=2, max_length=80, description="دانشکده")


class ProfessorUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=2, max_length=50, pattern=r"^[^\W\d_]+(?: [^\W\d_]+)*$")
    last_name: Optional[str] = Field(None, min_length=2, max_length=50, pattern=r"^[^\W\d_]+(?: [^\W\d_]+)*$")
    personnel_code: Optional[str] = Field(None, min_length=3, max_length=20, pattern=r"^[A-Za-z0-9\u0600-\u06FF_()-]+$")
    department: Optional[str] = Field(None, min_length=2, max_length=80)
