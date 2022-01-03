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
  # ajoutez "--port {numéro du port}" pour changer le port par défaut (3000)
  ```
  - testez le serveur en entrant ce lien sur votre navigateur http://localhost:3000 vous trouverez un "hello world"

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

##  Pour les utilisateurs de pyqt5


Tous les fichiers nécessaires se trouvent dans  tp_m2_bsd\package\server\pyqt_integration

Pour démarrer importer ou copier la classe Server_Worker dans le même fichier où votre classe QMainWindow est définie.
ce serveur est le même adel a écrite mais il est fait de manière à fonctionner avec pyqt5

```python
# add this at the beging of your main file code 
from flask import Flask, request,current_app
from handler import validate_encrypt_request 
from PyQt5 import QtCore

class Server_Worker(QtCore.QObject):
    res = QtCore.pyqtSignal(dict)
    app = Flask(__name__)

    def __init__(self):
        super().__init__()
    

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
        self.app.config['obj'] = self
        self.app.run(port=3000)
```

Ensuite, dans votre fonction \_\_init\_\_ dans la classe QMainWindow, ajoutez ceci

```python
self.server_worker = Server_Worker()
self.thread = QtCore.QThread()
self.server_worker.moveToThread(self.thread)
self.thread.started.connect(self.server_worker.run)
self.server_worker.res.connect(self.p)
self.thread.start()
```
ajoutez cette fonction à votre classe QMainWindow redéfinissez la selon vos besoins, elle devrait mettre à jour l'interface,(**n'oubliez pas de déchiffrer le texte**).

```python
def p(self,val):
# add this in your QMainWindow class and write UI changes here the val varible is what result of the post request
    print(val)
```

la variable val est un dictionnaire python avec une structure similaire à celle-ci
```python
{'sender': 'yacine', 'algorithm': 'ceasar', 'message': 'Hello World', 'key': 6, 'type': 'encrypt'}
```

# peer_discovery


Toutes les fonctions peuvent être trouvées dans le fichier tp_m2_bsd/package/server/peer_discovery.py 

dans ce fichier, vous trouverez les fonctions nécessaires à votre identification ainsi qu'à l'identification d'autres personnes en plus de la fonction d'envoi des données à votre destination.

### get_gatway_ip()

cette fonction permet d'obtenir l'adresse IP de la passerelle par défaut (gatway)
```python
def get_gatway_ip():
    try:
        gateways = netifaces.gateways()
        defaults = gateways.get("default")
        return defaults[2][0]
    except:
        raise Exception('make sure you are online...')
```

### request()

cette fonction est utilisée à la fois pour vous identifier ainsi que pour obtenir des informations sur d'autres peer
```python
def request(name,state=False):
  data = {'name':name,'active':state}
  x = requests.post(f"http://{get_gatway_ip()}:3000/get-peers",json=data)
  if x.status_code == 200:
    return extract_list_of_users(x.json())
  else:
    return []
```

pour l'utiliser il suffit de spécifier votre nom dans le réseau et votre état dans le réseau

- state = False: signifie que je veux m'identifier mais je ne veux pas recevoir de données de qui que ce soit.

- state = True: signifie que je veux m'identifier et que je suis prêt à recevoir des données d'autres peer

lorsque vous envoyez la demande, une réponse sera renvoyée par le serveur si le code de réponse est 200 cela signifie que la demande a réussi et la fonction renverra une chaîne json similaire à cette structure

```json
[{"ip":"10.42.0.12","name":"Yacine","active":false}]
```
sinon la fonction retournera une list vide

### extract_list_of_users()

transformer de la list des peers
```python
[{"ip":"10.42.0.12","name":"Yacine","active":false}] 
=>>> {"10.42.0.12" :"Yacine"}
```

```python
def extract_list_of_users(peer_data):
        temp_list = {}
        if peer_data == []:
                return temp_list
        else:
                for user in peer_data:
                        if user['active'] == True:
                                temp_list[user['ip']] = user['name']
        return temp_list
```



### send_data()

cette fonction est utilisée pour envoyer des données à d'autres peer (vous n'êtes pas obligé de l'utiliser, vous pouvez écrire la votre).

<br />

assurez-vous simplement d'appeler cette fonction avec tous les bons arguments et vérifiez si le code de retour est 200, si c'est le cas, cela signifie que vous êtes bon, les informations que vous avez envoyées ont été reçues et le serveur de destination a répondu. tout autre code signifie que la demande n'a pas été faite correctement.
```python
def send_data(ip,sender,algo,msg,key):
    data = {"sender": sender ,"algorithm": algo ,"message": msg ,"key": key ,"type": "encrypt"}
    url = f'http://{ip}:3000/encrypt'
    x = requests.post(url, json=data)
    return x.status_code
```


