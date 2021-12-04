# Documentation Projet Sécurité

## Sommaire

- [Standard de requête](#standard-de-requête)
- [Serveur](#serveur)


## standard de requête

Nous allons suivre le standard REST (c'est le plus simple des standards matechkiwch)

Le format utilisé est json,
exemple de requête:
```json
{
    "sender": "adel",
    "algorithm": "ceasar",
    "message": "Hello World",
    "key": 6,
    "type": "encrypt"
}
```

- sender: représente le nom de l'expéditeur (utilisez vôtre prénom)
- algorithm: le nom de l'algorithme utilisé (où à utiliser) la liste standard des noms d'algorithms se trouve ici
- message: tout simplement le message à envoyer
- key: la clé, elle est dynamique et dépend de l'algo
- type (encrypt|decrypt): peut prendre deux valeurs 'encrypt' ou 'decrypt'
  - encrypt: signifie que le message envoyé doit être crypté par le recipient (message doit être en clair)
  - decrypt: signifie que le message envoyé doit être décrypté par le recipient (message doit être crypté)

### listes des Algorithmes

- ceasar: 'ceasar'
- vigenere: 'vigenere'
- substitution: 'substitution'
- transposition: 'transposition'
<!-- - des: 'des' -->
<!-- - rsa: 'rsa' -->

### types de la clé

- ceasar: nombre (type: number)
  - `key: 6`
- vigenere: string
  - `key: 'grou'`
- substitution: String
  - alphabet de chiffrement:
    - taille 26
    - sans duplication
  - `key: 'zyxwvutsrqponmlkjihgfedcba' `
- transposition: nombre (type: number)
  - `key: 6`
<!-- - des: 'des' -->





# Serveur

## Installation

- clonez ce projet 
  ```bash 
  git clone git@github.com:Quickinline/tp_m2_bsd.git 
  ```
- Copiez le dossier "serveur" qui se trouve dans le dossier package dans votre projet 
### Pour les utilisateurs docker
  

- lancez docker
  ```bash 
  docker-compose up -d && docker-compose logs -f 
  ```
- et le serveur fonctionne au port 80 !!!
- - testez le serveur en entrant ce lien sur votre navigateur http://localhost vous verrez un "hello world"

### Pour les autres utilisateurs docker
  - Installez les dépendances
  ```sh
  export PYTHONDONTWRITEBYTECODE=1 # (optional but its cleaner)
  export FLASK_ENV=development # to enable development
  export FLASK_APP=app # this is the file's name, if you happen to change it, change this env as well
  # replace 'export' by 'set' for windows cmd)
  pip install flask # installs flask (duh ...)
  ```
  - lancez le serveur
  ```bash
  flask run 
  # ajoutez "--port {numéro du port}" pour changer le port par défaut (5000)
  ```
  - testez le serveur en entrant ce lien sur votre navigateur http://localhost:5000 vous trouverez un "hello world"

## utilisation

une fois le fichier app.py ouvert vous trouverez ceci

Vous **devez** ajouter votre code avant le return pour traiter la requête et actionner des modification dans vôtre application desktop (affichage, etc...) 

```python
from flask import Flask, request
from handler import validate_encrypt_request


app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"




@app.route('/encrypt', methods=['POST'])
def encrypt():
    requestJson = request.get_json()
    validate_encrypt_request(requestJson)
    sender = requestJson['sender']
    algorithm = requestJson['algorithm']
    message = requestJson['message']
    key = requestJson['key']
    typed = requestJson['type']
    # build response
    #  //insèrez votre code qui traite le message là
    # 
    # 
    # 
    return 'response'


```