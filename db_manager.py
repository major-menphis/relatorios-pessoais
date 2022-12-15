import sqlite3
import os
import hashlib

#Nome do banco de dados
banco = "banco.db"

#Criação do banco de dados se não existir no diretório atual
def criar_banco():
    if os.path.exists(banco):
        print(f"O banco de dados {banco} já existe.")
    else:
        conexao = sqlite3.connect(banco)
        cursor = conexao.cursor()

        #Criação da tabela de usuários
        cursor.execute("""
        CREATE TABLE usuarios(
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            senha TEXT NOT NULL
        );
        """)
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
        print(f"Usuário {usuario_logado} logado.")
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