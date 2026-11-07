from sqlmodel import  Session
from pydantic import ValidationError
from models import Villes

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

    