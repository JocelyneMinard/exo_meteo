from sqlalchemy import select
from sqlmodel import  Session
from models import Villes

def delete_city_by_id(session: Session, city_id: int):
    try:
        # Search city in database
        city = session.get(Villes, city_id)
        
        #  if not exist
        if city is None:
            print(f"Aucune ville trouvée avec l'ID : {city_id}")
            return False
            
        # If exist delete and validate in Db
        session.delete(city)
        session.commit()
        print("Suppression réussie avec succès !")
        return True
        
    except Exception as e:
        session.rollback()
        print(f"Erreur lors de la suppression : \n{e}")
        return False