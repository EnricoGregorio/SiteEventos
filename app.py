from distutils.log import debug
from flask import Flask, render_template, request, session, redirect
import connection as conn
app = Flask(__name__)

app.secret_key = "8ryt387bhdrj8e9xcf73fgby0f0vv"

redirectHome = redirect('http://127.0.0.1:5000/')

# Função para enviar os dados do Gestor das notícias para a sessão.
def setGestorUser(user, pwdUser, pageLink):
    if 'gestorLogin' and 'gestorPwd' in session:
        gestorLogin = session['gestorLogin']
        userPwd = session['gestorPwd']
    else:
        session['gestorLogin'] = user
        session['gestorPwd'] = pwdUser
    return redirectHome

@app.route('/')
def showHomePage():
    pageHome = render_template('index.html')
    return pageHome

# Função para carregar uma página que não existe no site.
@app.route('/<inexistente>', methods=['GET'])
def showErrorPage(inexistente):
    pageError = render_template('pageError404.html')
    return pageError

@app.route('/cadastro', methods=['GET', 'POST'])
def showPageCadastro():
    pageCadastro = render_template('pageCadastro.html')
    if 'gestorLogin' and 'gestorPwd' in session:
        return redirectHome
    else:
        if request.method == 'GET':
            return pageCadastro
        else:
            nome = request.form['nome'].strip()
            email = request.form['email'].strip()
            senha = request.form['senha'].strip()
            resultado = conn.setGestor(nome, email, senha)
            if resultado == 1:
                return redirectHome
            else:
                return pageCadastro + '<script>window.alert("Esse e-mail já está cadastrado!")</script>'
            
@app.route('/login', methods=['GET', 'POST'])
def showPageLogin():
    pageLogin = render_template('pageLogin.html')
    if 'gestorLogin' and 'gestorPwd' in session:
        return redirectHome
    else:
        if request.method == 'GET':
            return pageLogin
        else:
            email = request.form['email'].strip()
            senha = request.form['senha'].strip()
            resultado = conn.getGestor(email, senha)
            if resultado == 0:
                return pageLogin + '<script>window.alert("Esse e-mail não existe.")</script>'
            elif resultado == 1:
                return pageLogin + '<script>window.alert("E-mail e/ou senha incorreto(s).")</script>'
            else:
                return redirectHome

@app.route('/eventos', methods=['GET', 'POST'])
def showPageEventos():
    pageEventos = render_template('pageEventos.html')
    if 'gestorLogin' and 'gestorPwd' in session:
        if request.method == 'GET':
            return pageEventos
        else:
            nomeE = request.form['nome'].strip()
            emailGestor = session['gestorLogin']
            dtInicio = request.form['dtinicio'].strip()
            dtFinal = request.form['dtfinal'].strip()
            resultado = conn.setEvento(nomeE, emailGestor, dtInicio, dtFinal)
            if resultado == 1:
                return redirectHome
            else:
                return pageEventos + '<script>window.alert("Esse título já foi usado em outro evento!")</script>'
    else:
        return redirectHome

@app.route('/alunos', methods=['GET', 'POST'])
def showPageAlunos():
    # pageAlunos = render_template('pageAlunos.html')
    if request.method == 'GET':
        numMatricula = ''
        lista = conn.getAlunos(numMatricula)
        pageAlunos = render_template('pageAlunos.html', alunos=lista)
        return pageAlunos
    else:
        numMatricula = request.form['matricula'].strip()
        lista = conn.getAlunos(numMatricula)
        pageAlunos = render_template('pageAlunos.html', alunos=lista)
        return pageAlunos

@app.route('/contato', methods=['GET', 'POST'])
def showPageContato():
    pageContato = render_template('pageContato.html')
    if request.method == 'GET':
        return pageContato
    else:
        # Escrever código.
        return pageContato

if __name__ == "__app__":
    app.run(debug=True)
