import netifaces
import requests

def get_gatway_ip():
    try:
            gateways = netifaces.gateways()
            defaults = gateways.get("default")
            return defaults[2][0]
    except:
            raise Exception('make sure you are online...')

def request(name,state=False):
        data = {'name':name,'active':state}
        try:
                x = requests.post(f"http://{get_gatway_ip()}:3000/get-peers",json=data)
                if x.status_code == 200:
                        return extract_list_of_users(x.json())
                else:
                        return {}
        except:
                return {}

def extract_list_of_users(peer_data):
        temp_list = {}
        if len(peer_data) == []:
                return temp_list
        else:
                for user in peer_data:
                        if user['active'] == True:
                                temp_list[user['ip']] = user['name']
        return temp_list

def send_data(ip,sender,algo,msg,key):
        data = {"sender": sender ,"algorithm": algo ,"message": msg ,"key": key ,"type": "encrypt"}
        url = f'http://{ip}:3000/encrypt'
        try:
                x = requests.post(url, json=data)
                return x.status_code
        except:
                return -1
    


