from sqlalchemy import select
from sqlmodel import Session
from models import Releves
from models import Villes

# View all statements for all cities
def view_data(session: Session):
    try:
        requete = select(Villes)
        requete = (
            select(Villes.nom, Releves.temperature, Releves.vitesse_vent, Releves.date_heure)
            .outerjoin(Releves, Releves.ville_id == Villes.id) 
        )
        results = session.exec(requete).all()
        list_result = []
        for row in results:
            list_result.append({
                "nom": row.nom,
                "temperature": row.temperature,
                "vitesse_vent": row.vitesse_vent,
                "date_heure": row.date_heure
            })
        
        return list_result
    except Exception as e :
            print(f"Requête Échouée : \n{e}")