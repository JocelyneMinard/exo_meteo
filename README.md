# Excercice meteo

## Techniques
Utilisation de SQLModel pour monter en compétences
Souhait de réaliser un validateur sur le couple latitude / longitude, mais par manque de temps il a été abandonné. L'utilisation de rootModel est nécessaire.  

J'ai également pensé à réaliser un validateur simple pour les float latitude / longitude pour remplacer les virgules par des points, mais ayant perdu beaucoup de temps sur la gestion de la date du relevé j'ai préféré avancer sur le reste de l'exercice
Le soucis de date viendrais de SQLite.  

Utilisation pour la première fois de Uv pour lancer FastAPI, celui-ci crée des fichiers dans le répertoire, un basculement avec Uvicorn est envisagé

### FastApi
J'ai utilisé le module OS afin de mieux gérer le chemin absolu pour la base de données.

L'utilisation d'un fichier .env est à prévoir


### Alembic
j'ai dû utiliser Alembic pour créer une clé sur la table ville afin de mieux contrôler les données et m'assurer que la base n'accepte pas de doublon, même si FastAPI contrôle avant l'insertion

Après modification du SQLModel, et configuration d'alambic,
on  peut lancer une commande qui crée le script automatiquement :
```
alembic revision --autogenerate -m "add_triple_unique_constraint"
alembic upgrade head
```

### Conclusion
Suite à l'utilisation d'alambic et le contrôle d'insertion de FastApi, j'ai renoncé à créer un validateur Pydantic avec RootModel

## Installation

```pip install -r requierements.txt```

