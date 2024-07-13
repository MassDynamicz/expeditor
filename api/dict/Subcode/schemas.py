from pydantic import BaseModel


# region Ж\Д код
class SubcodeBase(BaseModel):
    name: str
    owner_id: int

    class Config:
        from_attributes = True


class SubcodeCreate(SubcodeBase):
    pass


class SubcodeUpdate(BaseModel):
    name: str
    owner_id: int

    class Config:
        from_attributes = True


class SubcodeInDBBase(SubcodeBase):
    id: int

    class Config:
        from_attributes = True


class Subcode(SubcodeInDBBase):
    pass


class SubcodeInDB(SubcodeInDBBase):
    pass
# endregion
