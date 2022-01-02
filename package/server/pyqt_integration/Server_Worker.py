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
    
