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

### Pour les autres utilisateurs
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

##  For pyqt5 users

Tous les fichiers nécessaires se trouvent dans  tp_m2_bsd\package\server\pyqt_integration

Pour démarrer importer ou copier la classe Server_Worker dans le même fichier où votre classe QMainWindow est définie.
ce serveur est le même adel a écrite mais il est fait de manière à fonctionner avec pyqt5

```python
# add this at the beging of your main file code in case of some import error change the import to what works for you
from flask import Flask, request,current_app
from handler import validate_encrypt_request 
from PyQt5 import QtCore

class Server_Worker(QtCore.QObject):
    res = QtCore.pyqtSignal(dict)
    app = Flask(__name__)

    def __init__(self):
        super().__init__()
        self.Stat = False
    

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
        current_app.config['obj'].res.emit(requestJson)

        return requestJson

    def run(self):
        self.Stat = True
        self.app.config['obj'] = self
        self.app.run(port=3000)
    def stop(self):
        self.Stat = False

```

après cela, vous devez exécuter l'objet Server_Worker dans un thread en liant la fonction p2p_even_recive à un événement de boutton. Cette fonction doit être définie dans votre classe QMainWindow

```python
def p2p_even_recive(self):
    # add this in your QMainWindow class and connect it the btn that is going to start the server for the peer2peer conection
    if self.server_worker.Stat == False:
        self.server_worker.moveToThread(self.thread)
        self.thread.started.connect(self.server_worker.run)
        self.server_worker.res.connect(self.p)
        self.thread.start()
```

Ensuite, dans votre fonction \_\_init\_\_ dans la classe QMainWindow, ajoutez ceci
```python
self.server_worker = Server_Worker()
self.thread = QtCore.QThread()
```

```python
def p(self,val):
# add this in your QMainWindow class and write UI changes here the val varible is what result of the post request
    print(val)
```

la variable val est un dictionnaire python avec une structure similaire à celle-ci
```python
{'sender': 'yacine', 'algorithm': 'ceasar', 'message': 'Hello World', 'key': 6, 'type': 'encrypt'}
```