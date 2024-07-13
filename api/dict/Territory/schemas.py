from pydantic import BaseModel


# region
class TerritoryBase(BaseModel):
    name: str
    code: str


class TerritoryCreate(TerritoryBase):
    pass


class TerritoryUpdate(BaseModel):
    name: str = None
    code: str = None


class TerritoryInDBBase(TerritoryBase):
    id: int

    class Config:
        from_attributes = True


class Territory(TerritoryInDBBase):
    pass


class TerritoryInDB(TerritoryInDBBase):
    pass
# endregion
