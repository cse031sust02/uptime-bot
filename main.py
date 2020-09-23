import json
import requests


def get_servers():
    with open('servers.json') as f:
        servers = json.load(f)
        return servers


def monitor_server(server):
    try:
        r = requests.get(server['address'], timeout=5)
        status = r.status_code
        if status != 200:
            notify_downtime(server)
    except Exception as e:
        print("Error in requesting the server :", e)
        notify_downtime(server)


def notify_downtime(server):
    mediums = server['notify_via'].split(",")
    for medium in mediums:
        print(
            f"I am going to notify on {medium} that the server {server['name']} is down")


try:
    servers = get_servers()
except Exception as e:
    print(e)
else:
    for server in servers:
        monitor_server(server)
