from sqlalchemy import select
from sqlmodel import  Session
from pydantic import ValidationError
import requests
from datetime import datetime, timezone
from models import Villes
from models import Releves

# Add city into Database
def add_city(session: Session, name, latitude, longitude):
    try:   
        city = Villes(nom = name, latitude = latitude, longitude = longitude )
        session.add(city)
        session.commit()
        print("Insertion réussie avec succès !")
        return city
    except ValidationError as e:
        session.rollback() 
        print(f"Validation Pydantic Échouée : \n{e}")
        return e

# Add statement for all cities
def add_statement(session: Session):
    try:
        query = select(Villes)
        cities = session.exec(query).all()
        for city in cities:
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={city[0].latitude}&longitude={city[0].longitude}&current_weather=true"
            answer = requests.get(weather_url)
            api_data = answer.json()
            current_weather_units = api_data['current_weather']
            date_statement = datetime.fromisoformat(current_weather_units["time"])
            date_statement = date_statement.replace(tzinfo=timezone.utc)
            new_data = Releves(temperature = f"{current_weather_units["temperature"]}", vitesse_vent = f"{current_weather_units["windspeed"]}", date_heure = date_statement, ville_id = city[0].id) 
            session.add(new_data)
            session.commit() 
            print("--" * 40)
            
    except ValueError as e :
        print(f"Requête Échouée : \n{e}")
