import sqlalchemy
import requests
from sqlalchemy import inspect
import sqlmodel
from sqlmodel import Field, SQLModel, create_engine, Session
from datetime import date


sqlite_file_name = "meteo.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


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
    temperature: float = Field(ge=0)
    vitesse_vent: float = Field(ge=0)
    date_heure : date
    ville_id : int | None = Field(default=None, foreign_key="villes.id")

engine.echo = True  
SQLModel.metadata.create_all(engine)
engine.echo = False  

# inspect() permet de vérifier ce que contient réellement la base
print("Tables présentes dans la base :", inspect(engine).get_table_names())

# class check_city(RootModel[List[liste_ville]]):
#     @model_validator(mode="after")
#     def ckeck_unicity(self) -> Self:
#         list_to_validate = self.root
#         local_list = set()
#         all_city = []
#         for city in list_to_validate:
#             couple = (city.latitude, city.longitude)
#             if couple in local_list:
#                 raise ValueError(
#                     f"Doublon détecté dans la liste fournie : {ville.nom} ({paire})"
#                 )
#             local_list.add(couple)
#             all_city.append(couple)

#         return all_city

        

with Session(engine) as session:
    liste_ville = [
        Villes(nom = "La Rochelle", latitude = 46.166672, longitude = -1.150000 ),
        Villes(nom = "Paris", latitude = 48.8534, longitude = 2.3522),
        Villes(nom = "Tergnier", latitude = 49.656, longitude = 3.292),
    ]
    try:
        #valid_city = check_city.model_validate(liste_ville)
        session.add_all(liste_ville)
        session.commit()
        print("Insertion réussie avec succès !")
    except ValueError as e :
        print(f"Validation Échouée : \n{e}")

meteo_url = f("https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&current_weather=true")
url3 = "https://httpbin.org/get"

params={"ville": "Paris", "mois": "Juillet"}
reponse = requests.get(url3, params)
print(reponse.url)