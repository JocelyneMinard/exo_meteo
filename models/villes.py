import sqlmodel
from sqlmodel import Field, SQLModel

class Villes(SQLModel, table = True):
    __tablename__ = "villes"
    id : int | None = Field(default=None, primary_key=True)
    nom: str
    latitude: float 
    longitude: float
