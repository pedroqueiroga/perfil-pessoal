import os
from .perfil2 import do_everything
from . import msgs
from .settings import settings
import requests
import io
import traceback
from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def visualizador():
    return render_template('visualizador.html')

@app.route('/upload', methods = ['POST'])
def graph():
    if request.form:
        # devo pegar o arquivo do url
        url = request.form['url']
        res = requests.get(url)
        if res.status_code == requests.codes.ok:
            content_type = res.headers['Content-Type']
            f = io.BytesIO(res.content)
            res.close()
        else:
            return render_template('grafo.html',
                                   error=msgs.ERROR_COULDNT_DOWNLOAD)
    elif request.files:
        f = request.files['file']
        content_type = f.content_type
    if not 'application/pdf' in content_type:
        request.close()
        return render_template('grafo.html',
                               error=msgs.ERROR_NOT_PDF)
    try:
        g, curso, universidade, perfil = do_everything(f)
    except Exception as e:
        print('Erro:', e)
        traceback.print_tb(e.__traceback__)
        g = None
    finally:
        request.close()

    if g:
        grafo = g.pipe().decode('utf-8')
        return render_template('grafo.html', grafo=grafo, curso=curso, universidade=universidade, perfil=perfil)
    else:
        return render_template('grafo.html', error=msgs.ERROR_COULDNT_EXTRACT)

@app.route('/contato', methods = ['GET', 'POST'])
def contato():
    if request.method == 'GET':
        return render_template('contato.html')
    else:
        for k in request.form:
            print(k, request.form[k])
        request.close()
        return render_template('contato.html', obrigado=msgs.THANKS_FOR_CONTACT)
    

@app.route('/ajuda', methods = ['GET'])
def ajuda():
    return render_template('ajuda.html')


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = bool(os.getenv("DEBUG", False))
    app.run(host='0.0.0.0', port=port, debug=debug)
