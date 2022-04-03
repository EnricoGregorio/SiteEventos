-- Criação do banco de dados:
CREATE DATABASE dbeventos;

-- Definição do banco que usaremos:
USE dbeventos;

-- Criação da tabela para o Master, que terá todo o controle dos gestores.
CREATE TABLE MasterGestor(
    id INT AUTO_INCREMENT,
    user VARCHAR(10) NOT NULL UNIQUE,
    pwd VARCHAR(20) NOT NULL,
    PRIMARY KEY(id)
);

-- Tabelas para o cadastro do gestor:
CREATE TABLE Gestores(
    id INT AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(32) NOT NULL UNIQUE,
    pwd VARCHAR(20) NOT NULL,
    PRIMARY KEY(id)
);

CREATE TABLE Eventos(
    id INT AUTO_INCREMENT,
    evento VARCHAR(64) NOT NULL UNIQUE,
    idresponsavel INT NOT NULL,
    dtinicio DATE NOT NULL,
    dtfinal DATE NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(idresponsavel) REFERENCES Gestores(id)
);

-- Tabelas para o cadastro do aluno:
CREATE TABLE Turmas(
    id INT AUTO_INCREMENT,
    turma VARCHAR(10) NOT NULL UNIQUE,
    PRIMARY KEY(id)
);

CREATE TABLE Cursos(
    id INT AUTO_INCREMENT,
    curso VARCHAR(32) NOT NULL UNIQUE,
    PRIMARY KEY(id)
);

CREATE TABLE Alunos(
    id INT AUTO_INCREMENT,
    aluno VARCHAR(50) NOT NULL,
    matricula VARCHAR(11) NOT NULL UNIQUE,
    idturma INT NOT NULL,
    idcurso INT NOT NULL,
    idevento INT NOT NULL,
    PRIMARY KEY(id),
    FOREIGN KEY(idturma) REFERENCES Turmas(id),
    FOREIGN KEY(idcurso) REFERENCES Cursos(id),
    FOREIGN KEY(idevento) REFERENCES Eventos(id)
);