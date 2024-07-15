from pydantic import BaseModel


# region Ж\Д код
class RailWayCodeBase(BaseModel):
    name: str
    code: str
    owner_id: int
    territory_id: int

    class Config:
        from_attributes = True


class RailWayCodeCreate(RailWayCodeBase):
    pass


class RailWayCodeUpdate(BaseModel):
    name: str
    code: str
    owner_id: int
    territory_id: int

    class Config:
        from_attributes = True


class RailWayCodeInDBBase(RailWayCodeBase):
    id: int

    class Config:
        from_attributes = True


class RailWayCode(RailWayCodeInDBBase):
    pass


class RailWayCodeInDB(RailWayCodeInDBBase):
    pass
# endregion
