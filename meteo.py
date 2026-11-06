import os 
import sqlalchemy
import requests
from sqlalchemy import inspect, select
import sqlmodel
from sqlmodel import Field, SQLModel, create_engine, Session
from datetime import datetime, timezone
from pydantic import ValidationError, field_validator


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
    temperature: float = Field(ge=0)
    vitesse_vent: float = Field(ge=0)
    date_heure : datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    ville_id : int | None = Field(default=None, foreign_key="villes.id")

if not os.path.exists(sqlite_file_name):
    engine.echo = True  
    SQLModel.metadata.create_all(engine)
    engine.echo = False  
    # inspect() permet de vérifier ce que contient réellement la base
    print("Tables présentes dans la base :", inspect(engine).get_table_names())

    with Session(engine) as session:
        liste_ville = [
            Villes(nom = "La Rochelle", latitude = 46.166672, longitude = -1.150000 ),
            Villes(nom = "Paris", latitude = 48.8534, longitude = 2.3522),
            Villes(nom = "Tergnier", latitude = 49.656, longitude = 3.292),
        ]
        try:
            session.add_all(liste_ville)
            session.commit()
            print("Insertion réussie avec succès !")
        except ValidationError as e:
            print(f"Validation Pydantic Échouée : \n{e}")
        except Exception as e :
            print(f"Erreur de base : \n{e}")


with Session(engine) as session:
    try:
        requete = select(Villes)
        villes = session.exec(requete).all()
        #base_query = "INSERT INTO relevees (temperature, vitesse_vent, date_heure, ville_id) VALUES "
        for ville in villes:
            meteo_url = f"https://api.open-meteo.com/v1/forecast?latitude={ville[0].latitude}&longitude={ville[0].longitude}&current_weather=true"
            reponse = requests.get(meteo_url)
            api_data = reponse.json()
            current_weather_units = api_data['current_weather']
            date_releve = datetime.fromisoformat(current_weather_units["time"])
            date_releve = date_releve.replace(tzinfo=timezone.utc)
            print(current_weather_units["temperature"])
            print(current_weather_units["windspeed"])
            new_data = Releves(temperature = f"{current_weather_units["temperature"]}", vitesse_vent = f"{current_weather_units["windspeed"]}", date_heure = date_releve, ville_id = ville[0].id) 
            session.add(new_data)
            session.commit() 
            print("--" * 40)
            
    except ValueError as e :
        print(f"Requête Échouée : \n{e}")



with Session(engine) as session:
    try:
        requete = select(Villes)
        requete = (
            select(Villes.nom, Releves.temperature, Releves.vitesse_vent, Releves.date_heure)
            .outerjoin(Releves, Releves.ville_id == Villes.id) 
        )
        for ligne in session.exec(requete):
            print(f"{ligne.nom:<15} {ligne.temperature}")
    except Exception as e :
            print(f"Requête Échouée : \n{e}")
    
