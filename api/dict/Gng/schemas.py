from pydantic import BaseModel, conint, Field
from typing import Optional


# region Схема НДС
class GngBase(BaseModel):
    name: str
    code: str
    code_etsng: Optional[str] = ""

class GngCreate(GngBase):
    pass


class GngUpdate(BaseModel):
    name: str
    code: str
    code_etsng: str = None


class GngInDBBase(GngBase):
    id: int

    class Config:
        from_attributes = True


class Gng(GngInDBBase):
    pass


class GngInDB(GngInDBBase):
    pass
# endregion
