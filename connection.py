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
        values = (name, idGestor, dtInicio, dtFinal)
        query = "INSERT INTO Eventos(evento, idresponsavel, dtinicio, dtfinal) VALUES(%s, %s, %s, %s);"
        try:            
            cursor.execute(query, values)
            db.commit()
            return 1
        except pymysql.IntegrityError as err:
            return 0
        
# Cadastro de Alunos:
def insertAluno(name, matricula, idTurma, idCurso, idEvento):
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

# Consulta de Eventos:
def getEventos(evento):
    with db.cursor() as cursor:
        if evento == '':
            query = f"SELECT e.evento, g.nome, DATE_FORMAT(e.dtinicio, '%d/%m/%Y'), DATE_FORMAT(e.dtfinal, '%d/%m/%Y')  FROM Eventos AS e INNER JOIN Gestores AS g ON g.id = e.idresponsavel"
            cursor.execute(query)
            eventos = cursor.fetchall()
            return eventos
        else:
            query = f"SELECT e.evento, g.nome, DATE_FORMAT(e.dtinicio, '%d/%m/%Y'), DATE_FORMAT(e.dtfinal, '%d/%m/%Y')  FROM Eventos AS e INNER JOIN Gestores AS g ON g.id = e.idresponsavel WHERE e.evento = '%{evento}%'"
            cursor.execute(query)
            eventos = cursor.fetchall()
            return eventos

# Consulta de Alunos:
def getAlunos(matricula):
    with db.cursor() as cursor:
        if matricula == '':
            query = f"SELECT a.matricula, a.aluno, t.turma, c.curso, e.evento FROM Alunos AS a INNER JOIN Turmas AS t ON t.id = a.idturma INNER JOIN Cursos AS c ON c.id = a.idcurso INNER JOIN Eventos AS e ON e.id = a.idevento"
            cursor.execute(query)
            alunos = cursor.fetchall()
            return alunos
        else:
            query = f"SELECT a.matricula, a.aluno, t.turma, c.curso, e.evento FROM Alunos AS a INNER JOIN Turmas AS t ON t.id = a.idturma INNER JOIN Cursos AS c ON c.id = a.idcurso INNER JOIN Eventos AS e ON e.id = a.idevento WHERE a.matricula = '%{matricula}%'"
            cursor.execute(query)
            alunos = cursor.fetchall()
            return alunos
