from .perfil2 import do_everything

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def visualizador():
    return render_template('visualizador.html')

@app.route('/upload', methods = ['POST'])
def graph():
    f = request.files['file']
    if f.content_type != 'application/pdf':
        request.close()
        return render_template('grafo.html',
                               error='Não foi possível aceitar que você enviou '
                               'um pdf.')
    
    g = do_everything(f)
    request.close()
    if g:
        grafo = g.pipe().decode('utf-8')
        return render_template('grafo.html', grafo=grafo)
    else:
        return render_template('grafo.html', error='Não foi possível extrair as relações de cadeiras deste pdf. Se você realmente enviou um perfil curricular da UFPE, por favor nos informe criando um bug report no github, ou nos contatando.')

@app.route('/contato', methods = ['GET', 'POST'])
def contato():
    if request.method == 'GET':
        return render_template('contato.html')
    else:
        for k in request.form:
            print(k, request.form[k])
        request.close()
        return render_template('contato.html', obrigado='Obrigado por entrar em contato.')
    

@app.route('/ajuda', methods = ['GET'])
def ajuda():
    return render_template('ajuda.html')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
