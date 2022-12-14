import db_manager

db_manager.criar_banco()
opcao = 0
usuario_atual = "Faça o login"
while opcao != 6:
    print(f"USUÁRIO LOGADO: {usuario_atual}        OPÇÕES:")
    print('--' * 30)
    print('1 - cadastrar usuário.')
    print('2 - logar no sistema.')
    print('3 - consultar de usuários por ID.')
    print('4 - excluir usuário por ID.')
    print('5 - Deslogar do sistema')
    print('6 - sair do sistema')
    print('--' * 30)
    opcao = int(input("digite a opção: "))
    if opcao == 1:
        usuario = str(input("Digite usuário para cadastro:")).strip()
        senha = str(input("Digite a senha:" )).strip()  
        db_manager.inserir_usuario(usuario, senha)
    elif opcao == 2:
        usuario = str(input("Digite o seu usuário para logar:")).strip()
        senha = str(input("Digite a senha de login:" )).strip()
        usuario_logado = db_manager.validar_usuario(usuario, senha)
        if usuario_logado != None:
            usuario_atual = usuario_logado[1]
    elif opcao == 3:
        usuario = str(input("Digite o ID do usuário para pesquisa:")).strip()
        consulta = db_manager.consultar_usuario(usuario)
        print(consulta)
    elif opcao == 4:
        usuario = str(input("Digite o ID do usuário para exclusão:")).strip()
        db_manager.excluir_usuario(usuario)
    elif opcao == 5:
        print(f'Usuário {usuario_atual} fez logout.')
        usuario_atual = 'Faça o login'
    else:
        opcao = 6