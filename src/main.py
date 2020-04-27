import io
import traceback

import requests
from flask import Flask, render_template, request

from . import msgs
from .email import send_email_to_myself
from .perfil2 import do_everything
from .settings import settings

app = Flask(__name__)


@app.route('/')
def visualizador():
    """Route for '/'.

    Renders the template for the root URL.
    """
    return render_template('visualizador.html')


@app.route('/upload', methods=['POST'])
def graph():
    """Route for '/upload'.

    Gets a file object from an URL or from a file found in request and renders
    the graph if possible.
    """
    if request.form:
        # devo pegar o arquivo do url
        url = request.form['url']
        res = requests.get(url)
        if res.status_code == requests.codes['ok']:
            content_type = res.headers['Content-Type']
            pdf_file = io.BytesIO(res.content)
            res.close()
        else:
            return render_template('grafo.html',
                                   error=msgs.ERROR_COULDNT_DOWNLOAD)
    elif request.files:
        pdf_file = request.files['file']
        content_type = pdf_file.content_type
    if 'application/pdf' not in content_type:
        request.close()
        return render_template('grafo.html',
                               error=msgs.ERROR_NOT_PDF)
    try:
        dot, curso, universidade, perfil = do_everything(pdf_file)
    except Exception as err:
        print('Erro:', err)
        traceback.print_tb(err.__traceback__)
        dot = None
    finally:
        request.close()

    if dot:
        grafo = dot.pipe().decode('utf-8')
        return render_template('grafo.html', grafo=grafo, curso=curso,
                               universidade=universidade, perfil=perfil)
    return render_template('grafo.html', error=msgs.ERROR_COULDNT_EXTRACT)


@app.route('/contato', methods=['GET', 'POST'])
def contato():
    """Route for '/contato'.

    Handles both POST and GET. If GET, renders a form. If POST, sends an e-mail
    with the form's content.
    """
    if request.method == 'GET':
        return render_template('contato.html')

    email = request.form['email']
    text = request.form['textbox']
    email_text = f'E-mail informado: {email}\n\nTexto:\n{text}'
    res = send_email_to_myself(email_text)
    request.close()

    if res.status_code == requests.codes['ok']:
        return render_template('contato.html',
                               obrigado=msgs.THANKS_FOR_CONTACT)

    return render_template('contato.html', error=msgs.FAILED_CONTACT)


@app.route('/ajuda', methods=['GET'])
def ajuda():
    """Route for '/ajuda'

    Renders a template with help wanted text.
    """
    return render_template('ajuda.html')


if __name__ == "__main__":
    PORT = settings.PORT
    DEBUG = settings.DEBUG
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
