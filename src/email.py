import os
import requests


def send_email_to_myself(text):
    domain = os.getenv('MAILGUN_DOMAIN')
    api_key = os.getenv('MAILGUN_API_KEY')
    my_email = os.getenv('MY_EMAIL')

    return requests.post(
        f'https://api.mailgun.net/v3/{domain}/messages',
        auth=("api", api_key),
        data={"from": f'Visualizador de Perfil Curricular <mailgun@{domain}>',
              "to": [my_email],
              "subject": "Contato",
              "text": text})
