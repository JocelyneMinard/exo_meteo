from pydantic import field_validator
from sqlmodel import Field, SQLModel, UniqueConstraint

class Villes(SQLModel, table = True):
    __tablename__ = "villes"
    id : int | None = Field(default=None, primary_key=True)
    nom: str
    latitude: float 
    longitude: float

    # Ce validateur est au final inutile car le JSON dans FastApi n'accepte pas la virgule
    # Erreur de format avant meme d'arriver au validateur
    @field_validator('latitude', 'longitude', mode='before')
    @classmethod
    def replace_symbol(cls, v):
        if isinstance(v, str):
            v = v.replace(',', '.')
        return v

    __table_args__ = (
        UniqueConstraint("nom", "latitude", "longitude", name="unique_value"),
    )
