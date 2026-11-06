from sqlmodel import create_engine, Session

from models import create_db, add_data
from services import view_data


sqlite_file_name = "meteo.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)


create_db(engine, sqlite_file_name)

with Session(engine) as session:
    add_data(session)
    results = view_data(session)
    for row in results:
        print(f"A {row["nom"]} il faissait {row["temperature"]} le {row["date_heure"].strftime("%d-%m-%Y")} a {row["date_heure"].strftime("%H:%M:%S")} UTC")
                        
