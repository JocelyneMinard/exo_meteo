from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import select
from sqlmodel import create_engine, Session
import os
import sys

# Récupère le chemin absolu du dossier parent
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Ajoute le dossier parent au chemin de recherche de Python si ce n'est pas déjà fait
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from models import Villes, add_statement
from services import view_data, add_city

# Configuration de la base de données
sqlite_file_name = os.path.join(parent_dir, "meteo.db")
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)

# Initialisation de FastAPI
app = FastAPI(title="API Météo")

# Fonction de dépendance pour FastAPI
def get_session():
    with Session(engine) as session:
        yield session 

# --- ROUTES ---
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Météo"}

@app.get("/weather")
def get_all_weather(session: Session = Depends(get_session)):
    try:
        liste_meteo = view_data(session)
        return liste_meteo
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la requête : {e}")

@app.post("/weather/add")
def add_weather_data(session: Session = Depends(get_session)):
    """Déclenche manuellement la récupération des données Open-Meteo pour chaque ville."""
    try:
        add_statement(session)
        return {"status": "success", "message": "nouveaux relevés ajoutés."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Échec de la mise à jour : {e}")

@app.post("/city/add", status_code = status.HTTP_201_CREATED, response_model = Villes, response_model_exclude_unset = True)
def create_city(city_data: Villes, session: Session = Depends(get_session)):
    try:
        statement = select(Villes).where(
            Villes.nom ==  city_data.nom,
            Villes.latitude ==  city_data.latitude,
            Villes.longitude ==  city_data.longitude
        )
        exist_value = session.exec(statement).first()
        
        if exist_value:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "La combinaison de ces trois valeurs existe déjà."
            )
        city_data.id = None 
        new_city = add_city(
            session = session, 
            name = city_data.nom, 
            latitude = city_data.latitude, 
            longitude = city_data.longitude
        )
        return new_city     
    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Erreur lors de l'enregistrement de la ville : {str(e)}"
        )
