from pydantic import BaseModel, ValidationError


class Produit(BaseModel):
    """Un produit du catalogue Pixel & Co."""

    nom: str
    prix: float
    stock: int

produit = Produit(nom="Clavier mécanique K70", prix=89.90, stock=34)

print(produit)

# Les champs sont des attributs ordinaires
print(f"Nom : {produit.nom} | Prix : {produit.prix} € | Stock : {produit.stock} unités")
print(f"Valeur du stock : {produit.prix * produit.stock:.2f} €")

try:
    Produit(nom="Souris gamer RX-500", prix="gratuit", stock=41)
except ValidationError as e:
    print(e)

donnees_recues = {"prix": "cinquante-neuf", "stock": "beaucoup"}

try:
    Produit.model_validate(donnees_recues)
except ValidationError as e:
    for erreur in e.errors():
        print(f"loc   : {erreur['loc']}")
        print(f"msg   : {erreur['msg']}")
        print(f"type  : {erreur['type']}")
        print(f"input : {erreur['input']!r}")

def afficher_erreurs(erreur):
    """Résume une ValidationError : une ligne par problème."""
    print(f"{erreur.error_count()} erreur(s) pour le modèle {erreur.title}")
    for err in erreur.errors():
        # loc est un tuple : on le transforme en chemin lisible
        champ = " → ".join(str(element) for element in err["loc"]) or "(modèle entier)"
        print(f"  ❌ {champ} : {err['msg']} [reçu : {err['input']!r}]")


try:
    Produit.model_validate(donnees_recues)
except ValidationError as e:
    afficher_erreurs(e)

class Client(BaseModel):
    prenom: str
    nom: str
    telephone: str | None = None   # facultatif : None si non fourni
    parrain_id: int | None = None  # facultatif aussi


# Chloé n'a pas donné son téléphone, mais elle a été parrainée par le client n°1
client = Client(prenom="Chloé", nom="Bernard", parrain_id=1)
print(client)