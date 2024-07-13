from pydantic import BaseModel


# region Ж\Д код
class RWCodeBase(BaseModel):
    name: str
    code: str
    owner_id: int
    territory_id: int

    class Config:
        from_attributes = True


class RWCodeCreate(RWCodeBase):
    pass


class RWCodeUpdate(BaseModel):
    name: str
    code: str
    owner_id: int
    territory_id: int

    class Config:
        from_attributes = True


class RWCodeInDBBase(RWCodeBase):
    id: int

    class Config:
        from_attributes = True


class RWCode(RWCodeInDBBase):
    pass


class RWCodeInDB(RWCodeInDBBase):
    pass
# endregion
