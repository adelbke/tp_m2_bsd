import netifaces
import requests

def get_gatway_ip():
    try:
            gateways = netifaces.gateways()
            defaults = gateways.get("default")
            return defaults[2][0]
    except:
            raise Exception('make sure you are online...')

def request(name):
        data = {'name':name,'active':True}
        try:
                x = requests.post(f"http://{get_gatway_ip()}:3000/get-peers",json=data)
                if x.status_code == 200:
                        return x.json()
                else:
                        return []
        except Exception as e:
                print(e)
                return []



def send_data(ip,sender,algo,msg,key):
        data = {"sender": sender ,"algorithm": algo ,"message": msg ,"key": key ,"type": "encrypt"}
        url = f'http://{ip}:3000/encrypt'
        try:
                x = requests.post(url, json=data)
                return x.status_code
        except Exception as e:
                print(e)
                return -1
    


