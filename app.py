from distutils.log import debug
from flask import Flask, render_template, request, session, redirect
import connection as conn
import sendEmail as send
app = Flask(__name__)

app.secret_key = "8ryt387bhdrj8e9xcf73fgby0f0vv"

redirectHome = redirect('http://127.0.0.1:5000/')
redirectMaster = redirect('http://127.0.0.1:5000/masterLogin')

# Função para enviar os dados do Gestor das notícias para a sessão.
def setGestorUser(user, pwdUser):
    if 'gestorLogin' and 'gestorPwd' in session:
        gestorLogin = session['gestorLogin']
        userPwd = session['gestorPwd']
    else:
        session['gestorLogin'] = user
        session['gestorPwd'] = pwdUser
    return redirectHome

@app.route('/', methods=['GET', 'POST'])
def showHomePage():
    if request.method == 'GET':
        nomeEvento = ''
        lista = conn.getEventos(nomeEvento)
        pageHome = render_template('index.html', eventos=lista)
        return pageHome
    else:
        nomeEvento = request.form['evento'].strip()        
        lista = conn.getEventos(nomeEvento)
        pageHome = render_template('index.html', eventos=lista)
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
        if 'masterLogin' and 'masterPwd' in session:
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
        else:
            return redirectMaster
                
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
                setGestorUser(email, senha)
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
        return redirect('http://127.0.0.1:5000/login')

@app.route('/alunos', methods=['GET', 'POST'])
def showPageAlunos():
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

@app.route('/cadastroAlunos', methods=['GET', 'POST'])
def showPageCadastroAlunos():
    lista = conn.getEvento()
    pageCadastroAlunos = render_template('pageCadastroAlunos.html', eventosLista=lista)
    if 'gestorLogin' and 'gestorPwd' in session:
        if  request.method == 'GET':
            return pageCadastroAlunos
        else:
            numMatricula = request.form['matricula'].strip()
            nome = request.form['nome'].title().strip()
            turma = request.form['turma'].strip().replace('\'', '\"')
            curso = request.form['curso'].strip()
            evento = request.form['evento'].strip()
            # Pegar os IDs da turma e do curso no banco.
            evento = conn.getEventoAluno(evento)
            turmaECurso = conn.getTurmaECurso(turma, curso)
            turma = turmaECurso[0]
            curso = turmaECurso[1]
            # Conferir se foi possível inserir o aluno no banco.
            resultado = conn.setAluno(nome, numMatricula, turma, curso, evento)
            if resultado == 1:
                return pageCadastroAlunos + '<script>window.alert("Aluno(a) cadastrado(a) com sucesso!")</script>'
            else:
                return pageCadastroAlunos + '<script>window.alert("Esse número de matrícula já está registrado!")</script>'
    else:
        return redirect('http://127.0.0.1:5000/login')

@app.route('/contato', methods=['GET', 'POST'])
def showPageContato():
    pageContato = render_template('pageContato.html')
    if request.method == 'GET':
        return pageContato
    else:
        nome = request.form['nome'].title().strip()
        email = request.form['email'].strip()
        cel = request.form['celular'].strip()
        msg = request.form['mensagem'].capitalize().strip()
        if msg == '':
            return pageContato + '<script>window.alert("Preencha a mensagem!")</script>'
        else:
            try:
                send.sendEmail(nome, email, cel, msg)
            except:
                return pageContato + '<script>window.alert("Ocorreu um erro ao enviar a mensagem!")</script>'
        return pageContato + '<script>window.alert("Mensagem enviada com sucesso!")</script>'
    
@app.route('/masterLogin', methods=['GET', 'POST'])
def showPageMasterLogin():
    pageMasterLogin = render_template('pageMasterLogin.html')
    if 'masterLogin' and 'masterPwd' in session:
        return redirectHome
    else:
        if request.method == 'GET':
            return pageMasterLogin
        else:
            login = request.form['master'].strip()
            senha = request.form['senha'].strip()
            redirectCadastroGestor = redirect('http://127.0.0.1:5000/cadastro')
            if login == 'GestorMaster' and senha == 'Adh712(d-s7ç':
                session['masterLogin'] = login
                session['masterPwd'] = senha
                return redirectCadastroGestor
            else:
                return pageMasterLogin + '<script>window.alert("Usuário e/ou senha incorretos.")</script>'

if __name__ == "__app__":
    app.run(debug=True)
