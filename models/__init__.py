import os 
import requests
from sqlalchemy import inspect, select
from sqlmodel import SQLModel, Session
from datetime import datetime, timezone
from pydantic import ValidationError


from .villes import Villes
from .releves import Releves

def create_db(engine, sqlite_file_name):
    if not os.path.exists(sqlite_file_name):
        engine.echo = True  
        SQLModel.metadata.create_all(engine)
        engine.echo = False  
        # inspect() permet de vérifier ce que contient réellement la base
        print("Tables présentes dans la base :", inspect(engine).get_table_names())

        with Session(engine) as session:
            list_city = [
                Villes(nom = "La Rochelle", latitude = 46.166672, longitude = -1.150000 ),
                Villes(nom = "Paris", latitude = 48.8534, longitude = 2.3522),
                Villes(nom = "Tergnier", latitude = 49.656, longitude = 3.292),
            ]
            try:
                session.add_all(list_city)
                session.commit()
                print("Insertion réussie avec succès !")
            except ValidationError as e:
                print(f"Validation Pydantic Échouée : \n{e}")
            except Exception as e :
                print(f"Erreur de base : \n{e}")


def add_statement(session: Session):
    try:
        query = select(Villes)
        cities = session.exec(query).all()
        for city in cities:
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={city[0].latitude}&longitude={city[0].longitude}&current_weather=true"
            reponse = requests.get(weather_url)
            api_data = reponse.json()
            current_weather_units = api_data['current_weather']
            date_statement = datetime.fromisoformat(current_weather_units["time"])
            date_statement = date_statement.replace(tzinfo=timezone.utc)
            new_data = Releves(temperature = f"{current_weather_units["temperature"]}", vitesse_vent = f"{current_weather_units["windspeed"]}", date_heure = date_statement, ville_id = city[0].id) 
            session.add(new_data)
            session.commit() 
            print("--" * 40)
            
    except ValueError as e :
        print(f"Requête Échouée : \n{e}")
