import os 
from sqlalchemy import inspect
from sqlmodel import SQLModel, Session
from pydantic import ValidationError


from .villes import Villes
from .releves import Releves

# Create Db and insert 3 city
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

