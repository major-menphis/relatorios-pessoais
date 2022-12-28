import sqlite3
import os
import hashlib
from datetime import datetime

#Nome do banco de dados
banco = "banco.db"

#Criação do banco de dados se não existir no diretório atual
def criar_banco():
    if os.path.exists(banco):
        print(f"O banco de dados {banco} já existe.")
    else:
        conexao = sqlite3.connect(banco)
        cursor = conexao.cursor()

        #Criação da tabela de 'usuarios' no banco de dados
        cursor.execute("""
        CREATE TABLE usuarios(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            senha TEXT NOT NULL
        );
        """)

        # Criar a tabela 'atividades' no banco de dados
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS atividades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                usuario TEXT NOT NULL,
                status TEXT NOT NULL,
                data_agendada DATE NOT NULL,
                hora_agendada TIME NOT NULL,
                valor REAL,
                data_hora_iniciada TIMESTAMP,
                data_hora_terminada TIMESTAMP,
                tempo_total TIMESTAMP,
                descricao TEXT NOT NULL
            )
        ''')

        # Criar a tabela 'areas' no banco de dados
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS areas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                area TEXT NOT NULL,
                descricao TEXT NOT NULL,
                criada_em TIMESTAMP
            )
        ''')
        conexao.commit()
        conexao.close()

        print(f"Banco de dados {banco} criado com sucesso.")

#Função de criptografia
def hash_senha(senha):
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    return senha_hash

#Validação de usuários
def validar_usuario(usuario, senha):
    senha_hashed = hash_senha(senha)
    conexao = sqlite3.connect(banco)
    cursor = conexao.cursor()
    cursor.execute("""
    SELECT * FROM usuarios
    WHERE usuario = ? AND senha = ?
    """, (usuario, senha_hashed))
    usuario_logado = cursor.fetchone()
    if usuario_logado:
        print(f"Usuário válido {usuario_logado} logado.")
        return usuario_logado
    else:
        print(f'Usuário e senha inválidos.')
    conexao.close()

#Inserção de dados de usuários
def inserir_usuario(usuario, senha):
    senha_hashed = hash_senha(senha)
    conexao = sqlite3.connect(banco)
    cursor = conexao.cursor()
    #verificar se usuário existe
    cursor.execute("""
    SELECT * FROM usuarios
    WHERE usuario = ?
    """, (usuario,))
    resultado_consulta = cursor.fetchone()
    if resultado_consulta:
        print(f'Usuário {resultado_consulta[1]} já existe.')
    else:
        cursor.execute("""
        INSERT INTO usuarios (usuario, senha)
        VALUES (?, ?)
        """, (usuario, senha_hashed))
        conexao.commit()
        print(f'Usuário {usuario} inserido com sucesso.')
        conexao.close()

#Consulta de usuários
def consultar_usuario(id):
    conexao = sqlite3.connect(banco)
    cursor = conexao.cursor()
    cursor.execute("""
    SELECT * FROM usuarios
    WHERE id = ?
    """, (id,))
    usuario = cursor.fetchone()
    conexao.close()
    return usuario

#Exclusão de usuários
def excluir_usuario(id):
    conexao = sqlite3.connect(banco)
    cursor = conexao.cursor()
    cursor.execute("""
    DELETE FROM usuarios
    WHERE id = ?
    """, (id,))
    conexao.commit()
    print(f'Usuario ID {id} excluído.')
    conexao.close()

#adicionar nova atividade no banco
def adicionar_nova_atividade(atividade):
    conexao = sqlite3.connect(banco)
    cursor = conexao.cursor()
    # Converter a data e a hora para strings no formato DD-MM-YYYY e HH:MM:SS
    data_agendada = atividade.data_agendada.strftime("%d/%m/%Y")
    hora_agendada = atividade.hora_agendada.strftime("%H:%M:%S")
    data_hora_iniciada = atividade.data_hora_iniciada.strftime("%d/%m/%Y %H:%M:%S")
    data_hora_terminada = atividade.data_hora_terminada.strftime("%d/%m/%Y %H:%M:%S")
    tempo_total = atividade.tempo_total.strftime("%d/%m/%Y %H:%M:%S")
    # executa o adição
    cursor.execute("""INSERT INTO atividades 
    (titulo, usuario, status, data_agendada, hora_agendada, valor, data_hora_iniciada, data_hora_terminada, tempo_total, descricao) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
    (atividade.titulo, atividade.usuario, atividade.status, data_agendada, hora_agendada, atividade.valor, data_hora_iniciada, data_hora_terminada, 
    tempo_total, atividade.descricao))
    conexao.commit()
    conexao.close()

def consultar_atividades():
    conexao = sqlite3.connect(banco)
    cursor = conexao.cursor()
    cursor.execute("""
    SELECT * FROM atividades
    """)
    atividades = cursor.fetchall()
    conexao.commit()
    conexao.close()
    return atividades

def consultar_atividades_titulo_usuario(titulo, status):
    conexao = sqlite3.connect(banco)
    cursor = conexao.cursor()
    cursor.execute("""
    SELECT * FROM atividades
    WHERE titulo = ? AND
    status = ?
    """, (titulo, status))
    atividade = cursor.fetchone()
    conexao.close()
    return atividade

def editar_atividade(atividade):
    conexao = sqlite3.connect(banco)
    cursor = conexao.cursor()
    # Converter a data e a hora para strings no formato DD-MM-YYYY e HH:MM:SS
    data_agendada = atividade.data_agendada.strftime("%d/%m/%Y")
    hora_agendada = atividade.hora_agendada.strftime("%H:%M:%S")
    data_hora_iniciada = atividade.data_hora_iniciada.strftime("%d/%m/%Y %H:%M:%S")
    data_hora_terminada = atividade.data_hora_terminada.strftime("%d/%m/%Y %H:%M:%S")
    tempo_total = atividade.tempo_total.strftime("%d/%m/%Y %H:%M:%S")
    cursor.execute("""
    UPDATE atividades SET 
    usuario = ?, 
    status = ?, 
    data_agendada = ?, 
    hora_agendada = ?, 
    valor = ?, 
    data_hora_iniciada = ?, 
    data_hora_termianda = ?, 
    tempo_total = ?,  
    descricao = ? WHERE id = ?
    """, (atividade.usuario, atividade.status, data_agendada, hora_agendada, atividade.valor, data_hora_iniciada, data_hora_terminada, 
    tempo_total, atividade.descricao))
    conexao.commit()
    conexao.close()

def adicionar_area_atividade(area):
    #obter data e hora atual
    data_atual = datetime.now()
    #formatar a data atual para 'DD-MM-YYYY HH:MM:SS'
    data_criacao = data_atual.strftime('%d-%m-%Y %H:%M:%S')
    conexao = sqlite3.connect(banco)
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO areas (area, descricao, criada_em) VALUES (?, ?, ?)",
              (area.area, area.descricao, data_criacao))
    conexao.commit()
    conexao.close()

def consultar_areas():
    conexao = sqlite3.connect(banco)
    cursor = conexao.cursor()
    cursor.execute("""
    SELECT * FROM areas
    """)
    areas = cursor.fetchall()
    conexao.commit()
    conexao.close()
    return areas

