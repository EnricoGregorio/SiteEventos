import pymysql

# Configuração da conexão ao banco de dados.
setDB = {
    'host':'localhost',
    'user':'root',
    'password':'',
    'database':'dbeventos'
}

db = pymysql.connect(**setDB)

# Códigos para query no banco:

# Cadastros:

# Cadastro de Gestores:
def insertGestor(name, email, pwd):
    with db.cursor() as cursor:
        query = "SELECT id FROM Gestores WHERE email = %s"
        cursor.execute(query, email)
        gestor = cursor.fetchone()
        if gestor == None:
            values = (name, email, pwd)
            query = "INSERT INTO Gestores(nome, email, pwd) VALUES(%s, %s, %s);"
            cursor.execute(query, values)
            db.commit()
            return 0
        else:
            return 1
        
# Teste com try exception
def insertGestor2(name, email, pwd):
    with db.cursor() as cursor:
        values = (name, email, pwd)
        query = "INSERT INTO Gestores(nome, email, pwd) VALUES(%s, %s, %s);"
        try:
            cursor.execute(query, values)
            db.commit()
            return 1
        except pymysql.IntegrityError as err:
            return 0

# Cadastro de Eventos:
def insertEvento(name, idGestor, dtInicio, dtFinal):
    with db.cursor() as cursor:
        query = "SELECT id FROM Eventos WHERE evento = %s"
        cursor.execute(query, name)
        evento = cursor.fetchone()
        if evento == None:
            values = (name, idGestor, dtInicio, dtFinal)
            query = "INSERT INTO Eventos(evento, idresponsavel, dtinicio, dtfinal) VALUES(%s, %s, %s, %s);"
            cursor.execute(query, values)
            db.commit()
            return 0
        else:
            return 1
        
# Cadastro de Alunos:
def insertAluno(name, matricula, idTurma, idCurso, idEvento):
    with db.cursor() as cursor:
        query = "SELECT id FROM Alunos WHERE matricula = %s"
        cursor.execute(query, name)
        aluno = cursor.fetchone()
        if aluno == None:
            values = (name, matricula, idTurma, idCurso, idEvento)
            query = "INSERT INTO Alunos(aluno, matricula, idTurma, idCurso, idEvento) VALUES(%s, %s, %s, %s, %s);"
            cursor.execute(query, values)
            db.commit()
            return 0
        else:
            return 1

# Consultas:

def getGestor(email, pwd):
    with db.cursor() as cursor:
        query = "SELECT id FROM Gestores WHERE email = %s"
        cursor.execute(query, email)
        existeEmail = cursor.fetchone()
        if existeEmail == None:
            return 0
        else:
            values = (email, pwd)
            query = "SELECT id FROM Gestores WHERE email = %s AND pwd = %s"
            cursor.execute(query, values)
            existeGestor = cursor.fetchone()
            if existeGestor == None:
                return 1
            else:
                return 2

# Consulta de Eventos:
def getEventos(evento):
    with db.cursor() as cursor:
        if evento == '':
            query = f"SELECT e.evento, g.nome, DATE_FORMAT(e.dtinicio, '%d/%m/%Y'), DATE_FORMAT(e.dtfinal, '%d/%m/%Y')  FROM Eventos AS e INNER JOIN Gestores AS g ON g.id = e.idresponsavel"
            cursor.execute(query)
            eventos = cursor.fetchall()
            return eventos
        else:
            query = f"SELECT e.evento, g.nome, DATE_FORMAT(e.dtinicio, '%d/%m/%Y'), DATE_FORMAT(e.dtfinal, '%d/%m/%Y')  FROM Eventos AS e INNER JOIN Gestores AS g ON g.id = e.idresponsavel WHERE e.evento = '{evento}'"
            cursor.execute(query)
            eventos = cursor.fetchall()
            return eventos

# Consulta de Eventos:
def getAlunos(aluno):
    with db.cursor() as cursor:
        if aluno == '':
            query = f"SELECT e.evento, g.nome, DATE_FORMAT(e.dtinicio, '%d/%m/%Y'), DATE_FORMAT(e.dtfinal, '%d/%m/%Y')  FROM Eventos AS e INNER JOIN Gestores AS g ON g.id = e.idresponsavel"
            cursor.execute(query)
            alunos = cursor.fetchall()
            return alunos
        else:
            query = f"SELECT e.evento, g.nome, DATE_FORMAT(e.dtinicio, '%d/%m/%Y'), DATE_FORMAT(e.dtfinal, '%d/%m/%Y')  FROM Eventos AS e INNER JOIN Gestores AS g ON g.id = e.idresponsavel WHERE e.evento = '{aluno}'"
            cursor.execute(query)
            alunos = cursor.fetchall()
            return alunos

