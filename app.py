import sqlite3

def conexao_banco():
    conexao = sqlite3.connect('contatos.db')
    cursor = conexao.cursor()

    sql = '''CREATE TABLE IF NOT EXISTS contatos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                telefone TEXT NOT NULL,
                email TEXT NOT NULL
            )'''
    cursor.execute(sql)
    conexao.commit()
    return conexao

def adicionar_contato(nome,telefone,email):
    conexao = conexao_banco()
    cursor = conexao.cursor()
    sql = '''
        INSERT INTO contatos (nome, telefone, email)
        VALUES (?, ?, ?)'''
    cursor.execute(sql, (nome, telefone, email))
    conexao.commit()
    conexao.close()

def listar_contatos():
    conexao = conexao_banco()
    cursor = conexao.cursor()
    sql = "SELECT * FROM contatos"
    cursor.execute(sql)
    contatos = cursor.fetchall()
    if len(contatos) == 0:
        print("Nenhum contato encontrado.")
    else:
        print()
        print("Lista de contatos:")
        print("-" * 90)
        print(f"{'|ID':<9} | {'Nome':<21} | {'Telefone':<15} | {'Email':<10}")
        print("-" * 90)
        for contato in contatos:
            print(f"|ID: {contato[0]:<5} | Nome: {contato[1]:<15} | Telefone: {contato[2]:<15} | Email: {contato[3]:<10}")
            print("-" * 90)
    conexao.close() 

def buscar_contato():
    nome = input("Digite o nome do contato que deseja buscar: ")
    conexao = conexao_banco()
    cursor = conexao.cursor()
    sql = "SELECT * FROM contatos WHERE nome LIKE ?"
    cursor.execute(sql, ('%' + nome + '%',))
    contatos = cursor.fetchall()
    if len(contatos) == 0:
        print("Nenhum contato encontrado com esse nome.")
    else:
        print()
        print("Contatos encontrados:")
        print("-" * 90)
        print(f"{'|ID':<9} | {'Nome':<21} | {'Telefone':<15} | {'Email':<10}")
        print("-" * 90)
        for contato in contatos:
            print(f"|ID: {contato[0]:<5} | Nome: {contato[1]:<15} | Telefone: {contato[2]:<15} | Email: {contato[3]:<10}")
            print("-" * 90)
    conexao.close()

def atualizar_contato():
    id_contato = input("Digite o ID do contato que deseja atualizar: ")
    conexao = conexao_banco()
    cursor = conexao.cursor()
    sql = "SELECT * FROM contatos WHERE id = ?"
    cursor.execute(sql, (id_contato,))
    contato = cursor.fetchone()
    if contato is None:
        print("Nenhum contato encontrado com esse ID.")
        conexao.close()
        return
    print(f"Contato encontrado: {contato[1]} - {contato[2]} - {contato[3]}")
    novo_nome = input("Digite o novo nome (ou pressione Enter para manter o atual): ")
    novo_telefone = input("Digite o novo telefone (ou pressione Enter para manter o atual): ")
    novo_email = input("Digite o novo email (ou pressione Enter para manter o atual): ")
    if novo_nome == "":
        novo_nome = contato[1]
    if novo_telefone == "":
        novo_telefone = contato[2]
    if novo_email == "":
        novo_email = contato[3]
    sql = "UPDATE contatos SET nome = ?, telefone = ?, email = ? WHERE id = ?"
    cursor.execute(sql, (novo_nome, novo_telefone, novo_email, id_contato))
    conexao.commit()
    print("Contato atualizado com sucesso!")
    conexao.close()

def excluir_contato():
    id_contato = input("Digite o ID do contato que deseja excluir: ")
    conexao = conexao_banco()
    cursor = conexao.cursor()
    sql = "DELETE FROM contatos WHERE id = ?"
    cursor.execute(sql, (id_contato,))
    conexao.commit()
    if cursor.rowcount == 0:
        print("Nenhum contato encontrado com esse ID.")
    else:
        print("Contato excluído com sucesso!")
    conexao.close()

def menu():
    while True:
        print("###Contatos###")
        print("1 - Adicionar contato")
        print("2 - Listar contatos")
        print("3 - Buscar contato pelo nome")
        print("4 - Atualizar contato")
        print("5 - Excluir contato")
        print("6 - Sair")

        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            nome = input("Digite o nome do contato: ")
            telefone = input("Digite o telefone do contato: ")
            email = input("Digite o email do contato: ")
            adicionar_contato(nome, telefone, email)
            print("Contato adicionado com sucesso!")


        elif opcao == "2":
            listar_contatos()
            

        elif opcao == "3":     
             buscar_contato()

        elif opcao == "4":
             atualizar_contato()

        elif opcao == "5":
             excluir_contato()

        elif opcao == "6":
             print("Saindo do programa...")
             break  
        else:
            print("Opção inválida. Tente novamente.")

menu()