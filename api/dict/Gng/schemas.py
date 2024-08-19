from pydantic import BaseModel
from typing import Optional


class GngBase(BaseModel):
    name: str
    code: str
    code_etsng: Optional[str]=None


class GngInDB(GngBase):
    id: int

    class Config:
        from_attributes = True
