import netifaces
import requests

def get_gatway_ip():
    gateways = netifaces.gateways()
    defaults = gateways.get("default")
    return defaults[2][0]

def request(name,state=False):
    data = {'name':name,'active':state}
    x = requests.post(f"http://{get_gatway_ip()}:3000",json=data)
    if x.status_code == 200:
        return x.text
    else:
        return -1
    
def send_data(ip,sender,algo,msg,key):
    data = {"sender": sender ,"algorithm": algo ,"message": msg ,"key": key ,"type": "encrypt"}
    url = f'http://{ip}:3000/encrypt'
    x = requests.post(url, json=data)
    return x.status_code