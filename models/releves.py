from sqlmodel import Field, SQLModel
from datetime import datetime, timezone


class Releves(SQLModel, table = True):
    __tablename__ = "releves"
    id : int | None = Field(default=None, primary_key=True)
    temperature: float = Field(ge=0)
    vitesse_vent: float = Field(ge=0)
    date_heure : datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    ville_id : int | None = Field(default=None, foreign_key="villes.id")
