import json
import requests

from notifiers import EmailNotifier


def get_servers():
    with open('servers.json') as f:
        servers = json.load(f)
        return servers


def monitor_server(server):
    try:
        r = requests.get(server['address'], timeout=5)
        status = r.status_code
        return status
    except Exception:
        return False


def notify_downtime(server):
    notifiers = server.get('notify_via')

    if 'email' in notifiers:
        
        subject = "The {} server is down".format(server['name'])
        content = "Hello, The server for {} is down. Please take necessary action.".format(
            server['name'])        
        recipients = notifiers.get('email').get('address')

        # TODO : make it asynchronous (celery?)
        email_notify = EmailNotifier()
        email_notify.notify(subject=subject, recipients=recipients, content=content)

    if 'slack' in notifiers:
        # send msg to slack
        print(
            f"I will SEND A MESSAGE IN SLACK that the server {server['name']} is down")

    if 'sms' in notifiers:
        # send sms
        print(
            f"I will SEND A SMS that the server {server['name']} is down")


try:
    servers = get_servers()
except Exception as e:
    print(e)
else:
    for server in servers:
        status = monitor_server(server)
        if status != 200:
            notify_downtime(server)
