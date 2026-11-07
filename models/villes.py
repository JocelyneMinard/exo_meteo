from sqlmodel import Field, SQLModel, UniqueConstraint

class Villes(SQLModel, table = True):
    __tablename__ = "villes"
    id : int | None = Field(default=None, primary_key=True)
    nom: str
    latitude: float 
    longitude: float

    __table_args__ = (
        UniqueConstraint("nom", "latitude", "longitude", name="unique_value"),
    )
