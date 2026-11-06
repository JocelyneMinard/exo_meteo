from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import create_engine, Session
import os
import sys

# Récupère le chemin absolu du dossier parent
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Ajoute le dossier parent au chemin de recherche de Python si ce n'est pas déjà fait
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Importations de vos modules existants
from models import add_data
from services import view_data

# Configuration de la base de données
sqlite_file_name = "meteo.db"
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


@app.get("/meteo")
def get_all_meteo(session: Session = Depends(get_session)):
    try:
        liste_meteo = view_data(session)
        # 5. On renvoie la liste complète à FastAPI pour qu'il la transforme en JSON
        return liste_meteo

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la requête : {e}")


@app.post("/meteo/add")
def add_meteo_data(session: Session = Depends(get_session)):
    """Déclenche manuellement la récupération des données Open-Meteo pour chaque ville."""
    try:
        add_data(session)
        return {"status": "success", "message": "nouveaux relevés ajoutés."}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Échec de la mise à jour : {e}")
