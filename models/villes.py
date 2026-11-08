from pydantic import field_validator
from sqlmodel import Field, SQLModel, UniqueConstraint

class Villes(SQLModel, table = True):
    __tablename__ = "villes"
    id : int | None = Field(default=None, primary_key=True)
    nom: str =  Field(min_length=1)
    latitude: float
    longitude: float 

    # This validator is ultimately useless because JSON in FastAPI does not allow a trailing comma
    # A format error occurs even before reaching the validator
    @field_validator('latitude', 'longitude', mode='before')
    @classmethod
    def replace_symbol(cls, v):
        if isinstance(v, str):
            v = v.replace(',', '.')
        return v

    __table_args__ = (
        UniqueConstraint("nom", "latitude", "longitude", name="unique_value"),
    )
