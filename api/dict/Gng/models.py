from sqlalchemy import Column, Integer, String
from config.db import Base


# Класс - ГНГ
class Gng(Base):
    __tablename__ = "gng"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(300), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    code_etsng = Column(String(20), nullable=True)

    def __repr__(self):
        return f"'{self.name}'"
