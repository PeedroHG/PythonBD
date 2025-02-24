import pandas as pd
nome_arquivo = "" 

def limpar_tela():
    print("\033c", end="")

def exibir_tabela(df):
    limpar_tela()
    print(df.to_string())
    input("\nPressione qualquer tecla para voltar ao menu...")

def ler_arquivo():
    global nome_arquivo

    nome_arquivo = input("Informe o nome do arquivo que deseja ler: ")
    colunas_esperadas = {"ID_Cliente", "Nome_Cliente", "Produto", "Quantidade", "Preco_Unitario", "Data_Venda"}

    try:
        df = pd.read_csv(nome_arquivo + ".csv", encoding="utf-8", dtype={"ID_Cliente": "Int64"}) 
        
        colunas_csv = set(df.columns)

        if colunas_csv != colunas_esperadas:
            limpar_tela()
            print("Erro: O arquivo CSV não contém exatamente as colunas esperadas.")
            print(f"Esperado: {colunas_esperadas}")
            print(f"Encontrado: {colunas_csv}")
            exit()

        df["Data_Venda"] = pd.to_datetime(df["Data_Venda"], errors="coerce")
        df.index.name = "ID_Venda"

        return df

    except FileNotFoundError:
        print("Erro: Arquivo não encontrado")
        exit()
    
def filtrar_tabela(df):
    limpar_tela()
    # Exibir colunas disponíveis para escolha
    print("Colunas disponíveis para filtro:", list(df.columns))
    coluna = input("Digite o nome da coluna para filtrar: ")
    
    if coluna not in df.columns:
        print("Erro: Coluna não encontrada.")
        input("\nPressione qualquer tecla para voltar ao menu...")
        return

    tipo_coluna = df[coluna].dtype

    if tipo_coluna == 'datetime64[ns]': 
        valor = input(f"Digite o valor da data que deseja filtrar na coluna '{coluna}' no formato [AAAA-MM-DD]: ")
        tipo_filtro = input("Digite o tipo de filtro (igual, maior, menor): ").lower()
    elif tipo_coluna in ['int64', 'float64']: 
        valor = input(f"Digite o valor numérico que deseja filtrar na coluna '{coluna}': ")
        tipo_filtro = input("Digite o tipo de filtro (igual, maior, menor): ").lower()
    else:
        valor = input(f"Digite o valor que deseja filtrar na coluna '{coluna}': ")

    # Tipo string
    if tipo_coluna == 'object':  
        df_filtrado = df[df[coluna].str.contains(valor, case=False, na=False)]

    # Tipo data [AAAA-MM-DD]
    elif tipo_coluna == 'datetime64[ns]': 
        try:
            valor_data = pd.to_datetime(valor, errors='raise')
            
            if tipo_filtro == 'igual':
                df_filtrado = df[df[coluna] == valor_data]
            elif tipo_filtro == 'maior':
                df_filtrado = df[df[coluna] > valor_data]
            elif tipo_filtro == 'menor':
                df_filtrado = df[df[coluna] < valor_data]
            else:
                print("Erro: Tipo de filtro inválido.")
                input("\nPressione qualquer tecla para voltar ao menu...")
                return
        
        except ValueError:
            print("Erro: O valor fornecido não é uma data válida.")
            input("\nPressione qualquer tecla para voltar ao menu...")
            return

     # Tipo numérico (int ou float)
    elif tipo_coluna in ['int64', 'float64']: 
        try:
            valor_numero = float(valor)

            if tipo_filtro == 'igual':
                df_filtrado = df[df[coluna] == valor_numero]
            elif tipo_filtro == 'maior':
                df_filtrado = df[df[coluna] > valor_numero]
            elif tipo_filtro == 'menor':
                df_filtrado = df[df[coluna] < valor_numero]
            else:
                print("Erro: Tipo de filtro inválido.")
                input("\nPressione qualquer tecla para voltar ao menu...")
                return
        
        except ValueError:
            print("Erro: O valor fornecido não é numérico válido.")
            input("\nPressione qualquer tecla para voltar ao menu...")
            return

    # Tipo de dato de coluna desconhecido
    else:
        print("Erro: Tipo de dado da coluna não reconhecido.")
        input("\nPressione qualquer tecla para voltar ao menu...")
        return

    # Resultado
    limpar_tela()
    if df_filtrado.empty:
        print("Nenhum resultado encontrado para esse filtro.")
    else:
        print(df_filtrado)

    input("\nPressione qualquer tecla para voltar ao menu...")

def editar_tabela(df):
    limpar_tela()
    print("Editar Tabela")
    print("""
    [1] Adicionar nova linha
    [2] Remover uma linha
    [3] Editar uma linha
    [0] Voltar
    """)

    opcao = input("Escolha uma opção: ")

    # Adicionar
    if opcao == "1":
        # Gerar automaticamente o próximo ID_Cliente
        if not df.empty:
            novo_id = df["ID_Cliente"].max() + 1
        else:
            novo_id = 1  # Primeiro ID se DataFrame estiver vazio
        
        nome_cliente = input("Digite o nome do cliente: ")
        produto = input("Digite o nome do produto: ")

        try:
            quantidade = int(input("Digite a quantidade (número inteiro): "))
            preco_unitario = float(input("Digite o preço unitário (número decimal): "))
            data_venda = input("Digite a data da venda (AAAA-MM-DD): ")
            data_venda = pd.to_datetime(data_venda, format='%Y-%m-%d')  # Converter para datetime
        except ValueError:
            print("Erro: Entrada inválida. Certifique-se de digitar números e datas corretamente.")
            return df
        
        nova_linha = {
            "ID_Cliente": novo_id,
            "Nome_Cliente": nome_cliente,
            "Produto": produto,
            "Quantidade": quantidade,
            "Preco_Unitario": preco_unitario,
            "Data_Venda": data_venda
        }

        # Adicionar Ordena e Salva
        df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
        df = df.sort_values(by="ID_Cliente", ascending=True)
        df.to_csv(nome_arquivo + ".csv", index=False, encoding="utf-8")
        print("Nova venda adicionada com sucesso!")

    # Remover
    elif opcao == "2":
        try:
            id_venda = int(input("Digite o ID da venda que deseja remover: "))
            if id_venda in df.index:

                #Remove Ordena e Salva
                df = df.drop(index=id_venda)  
                df = df.sort_values(by="ID_Cliente", ascending=True)  
                df.to_csv(nome_arquivo + ".csv", index=False, encoding="utf-8") 

                print("Venda removida com sucesso!")
            else:
                print("Erro: ID da venda não encontrado.")
        except ValueError:
            print("Erro: Digite um número válido.")

    # Editar
    elif opcao == "3":
        try:
            id_venda = int(input("Digite o ID da venda que deseja editar: "))
            if id_venda not in df.index:
                print("Erro: ID da venda não encontrado.")
                return df
            
            print(f"Colunas disponíveis: {', '.join(df.columns)}")
            coluna = input("Digite o nome da coluna que deseja editar: ")

            if coluna not in df.columns or coluna == "ID_Cliente":
                print("Erro: Coluna inválida.")
                return df

            novo_valor = input(f"Digite o novo valor para {coluna}: ")

            # Ajustar tipo de dado
            if df[coluna].dtype == 'int64':
                novo_valor = int(novo_valor)
            elif df[coluna].dtype == 'float64':
                novo_valor = float(novo_valor)
            elif df[coluna].dtype == 'datetime64[ns]':
                novo_valor = pd.to_datetime(novo_valor, format='%Y-%m-%d')

            # Atualizar Ordena e Salva
            df.loc[id_venda, coluna] = novo_valor
            df = df.sort_values(by="ID_Cliente", ascending=True)
            df.to_csv(nome_arquivo + ".csv", index=False, encoding="utf-8")  # Mantém o ID_Venda como índice
            print("Venda editada com sucesso!")

        except ValueError:
            print("Erro: Entrada inválida.")

    elif opcao == "0":
        return df

    else:
        print("Opção inválida.")
    
    input("\nPressione qualquer tecla para voltar ao menu...")
    return df 