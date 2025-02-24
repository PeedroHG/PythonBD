import funcs

funcs.limpar_tela()
print("Gerenciamento de Vendas")
df = funcs.ler_arquivo()

while True:
    funcs.limpar_tela()
    print("Arquivo carregado: " + funcs.nome_arquivo + ".csv")
    print("""
        Menu:
          
        [1] -> Listar Vendas
        [2] -> Editar Tabela
        [3] -> Filtrar
        [0] -> Sair
        """)

    while True:
        try:
            opc = int(input('Digite a opção desejada: '))
            break
        except ValueError:
            print('\nOpção inválida. Por favor, tente novamente.')

    match opc:
        case 1:
            funcs.exibir_tabela(df)
        case 2:
            df = funcs.editar_tabela(df)
        case 3:
            funcs.filtrar_tabela(df)
        case 0:
            exit()
        case _:
            print("\nOpção inválida. Por favor, tente novamente.")