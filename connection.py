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
def setGestor(name, email, pwd):
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
def setEvento(name, emailGestor, dtInicio, dtFinal):
    with db.cursor() as cursor:
        query = "SELECT id FROM Gestores WHERE email = %s"
        cursor.execute(query, emailGestor)
        gestor = cursor.fetchone()
        idGestor = gestor[0]
        values = (name, idGestor, dtInicio, dtFinal)
        query = "INSERT INTO Eventos(evento, idresponsavel, dtinicio, dtfinal) VALUES(%s, %s, %s, %s);"
        try:            
            cursor.execute(query, values)
            db.commit()
            return 1
        except pymysql.IntegrityError as err:
            return 0
        
# Cadastro de Alunos:
def setAluno(name, matricula, idTurma, idCurso, idEvento):
    with db.cursor() as cursor:
        values = (name, matricula, idTurma, idCurso, idEvento)
        query = "INSERT INTO Alunos(aluno, matricula, idTurma, idCurso, idEvento) VALUES(%s, %s, %s, %s, %s);"
        try:
            cursor.execute(query, values)
            db.commit()
            return 1
        except pymysql.IntegrityError as err:
            return 0

# Consultas:
# Consulta de Gestor
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

def getEvento():
    with db.cursor() as cursor:
        query = "SELECT evento FROM Eventos;"
        cursor.execute(query)
        eventos = cursor.fetchall()
        # Converter a tupla de tuplas em uma única lista.
        eventosLista = []
        for evento in eventos:
            eventosLista += list(evento)
        return eventosLista
    
def getEventoAluno(e):
    with db.cursor() as cursor:
        query = "SELECT id FROM Eventos WHERE evento = %s;"
        cursor.execute(query, e)
        evento = cursor.fetchone()
        idevento = evento[0]
        return idevento
    
# Consulta de Eventos:
def getEventos(e):
    with db.cursor() as cursor:
        if e == '':
            query = f"SELECT e.evento, g.nome, DATE_FORMAT(e.dtinicio, '%d/%m/%Y') AS dtinicio, DATE_FORMAT(e.dtfinal, '%d/%m/%Y') AS dtfinal, COUNT(a.id) AS qtdalunos FROM Eventos AS e INNER JOIN Gestores AS g ON g.id = e.idresponsavel LEFT JOIN Alunos AS a ON a.idevento = e.id GROUP BY e.evento;"
            cursor.execute(query)
            eventos = cursor.fetchall()
            return eventos
        else:
            query = f"SELECT e.evento, g.nome, DATE_FORMAT(e.dtinicio, '%d/%m/%Y') AS dtinicio, DATE_FORMAT(e.dtfinal, '%d/%m/%Y') AS dtfinal, COUNT(a.id) AS qtdalunos FROM Eventos AS e INNER JOIN Gestores AS g ON g.id = e.idresponsavel LEFT JOIN Alunos AS a ON a.idevento = e.id WHERE e.evento LIKE '%{e}%' GROUP BY e.evento;"
            cursor.execute(query)
            eventos = cursor.fetchall()
            return eventos

def getTurmaECurso(t, c):
    with db.cursor() as cursor:
        # Pegar o ID da turma pela Turma(t).
        query = "SELECT id FROM Turmas WHERE turma = %s;"
        cursor.execute(query, t)
        turma = cursor.fetchone()
        idTurma = turma[0]
        # Pegar o ID do curso pelo Curso(c).
        query = "SELECT id FROM Cursos WHERE curso = %s;"
        cursor.execute(query, c)
        curso = cursor.fetchone()
        idCurso = curso[0]
        # Criar uma lista para retornar os dois valores.
        turmaECurso = [idTurma, idCurso]
        return turmaECurso

# Consulta de Alunos:
def getAlunos(matricula):
    with db.cursor() as cursor:
        if matricula == '':
            query = f"SELECT a.matricula, a.aluno, t.turma, c.curso, e.evento FROM Alunos AS a INNER JOIN Turmas AS t ON t.id = a.idturma INNER JOIN Cursos AS c ON c.id = a.idcurso INNER JOIN Eventos AS e ON e.id = a.idevento;"
            cursor.execute(query)
            alunos = cursor.fetchall()
            return alunos
        else:
            query = f"SELECT a.matricula, a.aluno, t.turma, c.curso, e.evento FROM Alunos AS a INNER JOIN Turmas AS t ON t.id = a.idturma INNER JOIN Cursos AS c ON c.id = a.idcurso INNER JOIN Eventos AS e ON e.id = a.idevento WHERE a.matricula LIKE '%{matricula}%';"
            cursor.execute(query)
            alunos = cursor.fetchall()
            return alunos
print(getEventos(''))