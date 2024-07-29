import enum
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Numeric, Enum
from sqlalchemy.orm import relationship
from config.db import Base


# Перечисление - виды собственности
class OwnerType(enum.Enum):
    # Физ лицо
    Individual = "Individual"
    # Юр. лицо
    Entity = "Entity"
