import requests

url = " https://httpbin.org/status/404"
reponse = requests.get(url)

#if "2" in str(reponse.status_code):
if reponse.status_code >= 200 and reponse.status_code <300:
    print("Tout va bien !")
    print(reponse.text)  # Affiche le code HTML de la page
elif str(reponse.status_code)[0] == 4 or str(reponse.status_code)[0] == 5 :
    reponse.raise_for_status()
else:
    print(f"Erreur de connexion : {reponse.status_code}")

url2 = "https://httpbin.org/headers"
header = {"User-Agent": "MonSuperScriptPython/1.0",
          "X-Mon-Jeton-Secret": "abc123xyz"}
reponse = requests.get(url2, headers= header)
print(reponse.headers["Content-type"])

url3 = "https://httpbin.org/get"

params={"ville": "Paris", "mois": "Juillet"}
reponse = requests.get(url3, params)
print(reponse.url)

url4 = "https://httpbin.org/post"
params={"ville": "Paris", "mois": "Juillet"}
reponse = requests.post(url4, json = params)
print(reponse.url)
print(reponse.json().get("json"))

url5 = "https://httpbin.org/cookies"
params={"ville": "Paris", "mois": "Juillet"}
reponse = requests.post(url4, params)
print(reponse.url)