import requests

from .settings import settings


def send_email_to_myself(text):
    """Function to send an e-mail to MY_EMAIL config var

    :param str text: Email content
    :returns: a response object. 200 ok means email sent successfully.
    :rtype: requests.response

    """
    domain = settings.MAILGUN_DOMAIN
    api_key = settings.API_KEY
    my_email = settings.MY_EMAIL

    return requests.post(
        f'https://api.mailgun.net/v3/{domain}/messages',
        auth=("api", api_key),
        data={"from": f'Visualizador de Perfil Curricular <mailgun@{domain}>',
              "to": [my_email],
              "subject": "Contato",
              "text": text})
