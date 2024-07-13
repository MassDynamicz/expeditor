from pydantic import BaseModel


# region Схема НДС
class ServiceTypeBase(BaseModel):
    name: str


class ServiceTypeCreate(ServiceTypeBase):
    pass


class ServiceTypeUpdate(BaseModel):
    name: str


class ServiceTypeInDBBase(ServiceTypeBase):
    id: int

    class Config:
        from_attributes = True


class ServiceType(ServiceTypeInDBBase):
    pass


class ServiceTypeInDB(ServiceTypeInDBBase):
    pass
# endregion
