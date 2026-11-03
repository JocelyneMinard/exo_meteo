from requests import Session
from sqlmodel import Field, SQLModel, create_engine
from pydantic_sqlite import DataBase
from datetime import date
import sqlite3

sqlite_file_name = "meteo.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

class Villes(SQLModel, table = True):
    __tablename__ = "villes"
    id : int | None = Field(default=None, primary_key=True)
    nom: str
    latitude: float
    longitude: float


class Releves(SQLModel, table = True):
    __tablename__ = "releves"
    id : int | None = Field(default=None, primary_key=True)
    nom: str
    temperature: float
    vitesse_vent: float
    date_heure : date
    ville_id : int | None = Field(default=None, foreign_key="team.id")


with Session(engine) as session:
    ville = Villes(id = 1, nom = "La Rochelle", latitude = 46.166672, longitude = -1.150000 )
    session.add(ville)
    session.commit()
