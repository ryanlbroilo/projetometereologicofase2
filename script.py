import csv
from datetime import datetime
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import os

def selecionar_arquivo():
    """
    Abre uma janela para seleção de arquivo CSV.
    Retorna o caminho do arquivo selecionado ou None se cancelado.
    """
    Tk().withdraw()  # Esconde a janela principal do tkinter
    caminho = askopenfilename(
        title="Selecione o arquivo CSV",
        filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")]
    )
    return caminho

def carregar_dados(caminho_arquivo):
    """
    Lê o arquivo CSV e carrega os dados meteorológicos em uma lista de dicionários.
    Ignora linhas incompletas ou mal formatadas.
    """
    dados = []
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        leitor = csv.reader(arquivo)
        for linha in leitor:
            if len(linha) < 6:
                continue  # Ignora linhas incompletas
            try:
                data = datetime.strptime(linha[0], '%d/%m/%Y')
                precipitacao = float(linha[1])
                temp_max = float(linha[2])
                temp_min = float(linha[3])
                umidade = float(linha[4])
                vento = float(linha[5])
                dados.append({
                    'data': data,
                    'precipitacao': precipitacao,
                    'temp_max': temp_max,
                    'temp_min': temp_min,
                    'umidade': umidade,
                    'vento': vento
                })
            except Exception:
                continue  # Ignora linhas inválidas
    return dados

def visualizar_intervalo(dados, mes_ini, ano_ini, mes_fim, ano_fim, opcao):
    """
    Exibe os dados meteorológicos em texto no intervalo de datas especificado,
    com diferentes opções de visualização.
    """
    # Ajusta o último dia do mês para data final correta
    def ultimo_dia_mes(ano, mes):
        from calendar import monthrange
        return monthrange(ano, mes)[1]
    
    data_inicio = datetime(ano_ini, mes_ini, 1)
    data_fim = datetime(ano_fim, mes_fim, ultimo_dia_mes(ano_fim, mes_fim))

    dados_filtrados = [d for d in dados if data_inicio <= d['data'] <= data_fim]

    if not dados_filtrados:
        print("Nenhum dado encontrado para o intervalo informado.")
        return

    if opcao == 1:
        print(f"{'Data':<12} {'Precipitação':<12} {'Temp Max':<10} {'Temp Min':<10} {'Umidade':<8} {'Vento':<6}")
        for d in dados_filtrados:
            print(f"{d['data'].strftime('%d/%m/%Y'):<12} {d['precipitacao']:<12.2f} {d['temp_max']:<10.2f} {d['temp_min']:<10.2f} {d['umidade']:<8.2f} {d['vento']:<6.2f}")
    elif opcao == 2:
        print(f"{'Data':<12} {'Precipitação':<12}")
        for d in dados_filtrados:
            print(f"{d['data'].strftime('%d/%m/%Y'):<12} {d['precipitacao']:<12.2f}")
    elif opcao == 3:
        print(f"{'Data':<12} {'Temp Max':<10} {'Temp Min':<10}")
        for d in dados_filtrados:
            print(f"{d['data'].strftime('%d/%m/%Y'):<12} {d['temp_max']:<10.2f} {d['temp_min']:<10.2f}")
    elif opcao == 4:
        print(f"{'Data':<12} {'Umidade':<8} {'Vento':<6}")
        for d in dados_filtrados:
            print(f"{d['data'].strftime('%d/%m/%Y'):<12} {d['umidade']:<8.2f} {d['vento']:<6.2f}")
    else:
        print("Opção inválida para visualização.")

def mes_mais_chuvoso(dados):
    """
    Calcula e exibe o mês e ano com maior precipitação acumulada.
    """
    chuva_mensal = {}
    for d in dados:
        chave = (d['data'].year, d['data'].month)
        chuva_mensal[chave] = chuva_mensal.get(chave, 0) + d['precipitacao']

    if not chuva_mensal:
        print("Nenhum dado de precipitação disponível.")
        return None

    mes_ano_mais_chuvoso = max(chuva_mensal, key=chuva_mensal.get)
    maior_precipitacao = chuva_mensal[mes_ano_mais_chuvoso]
    ano, mes = mes_ano_mais_chuvoso

    nome_mes = nome_mes_por_numero(mes)
    print(f"Mês mais chuvoso: {nome_mes} de {ano} com {maior_precipitacao:.2f} mm de precipitação.")
    return mes_ano_mais_chuvoso, maior_precipitacao

def nome_mes_por_numero(mes):
    """
    Retorna o nome do mês por extenso a partir do número (1-12).
    """
    meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
             "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
    if 1 <= mes <= 12:
        return meses[mes-1]
    else:
        return "mês inválido"

def media_temp_min_mes_anos(dados, mes):
    """
    Calcula a média da temperatura mínima para o mês especificado
    de cada ano entre 2006 e 2016 (inclusive).
    """
    medias = {}
    for ano in range(2006, 2017):
        temp_min_mes_ano = [d['temp_min'] for d in dados if d['data'].year == ano and d['data'].month == mes]
        chave = f"{nome_mes_por_numero(mes)}{ano}"
        if temp_min_mes_ano:
            media = sum(temp_min_mes_ano) / len(temp_min_mes_ano)
            medias[chave] = media
        else:
            medias[chave] = None  # Sem dados
    return medias

def plotar_grafico_barras(medias, mes):
    """
    Plota um gráfico de barras da média da temperatura mínima do mês especificado,
    para os anos 2006 a 2016.
    """
    anos = []
    medias_valores = []
    for chave, valor in medias.items():
        ano = chave[-4:]
        anos.append(ano)
        medias_valores.append(valor if valor is not None else 0)

    plt.figure(figsize=(10,6))
    plt.bar(anos, medias_valores, color='skyblue')
    plt.title(f'Média da Temperatura Mínima de {nome_mes_por_numero(mes)} (2006-2016)')
    plt.xlabel('Ano')
    plt.ylabel('Temperatura Mínima (°C)')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

def media_geral_temp_min(medias_mes_ano):
    """
    Calcula a média geral da temperatura mínima considerando todos os anos de um mês.
    """
    soma = 0
    contador = 0
    for valor in medias_mes_ano.values():
        if valor is not None:
            soma += valor
            contador += 1
    if contador == 0:
        return None
    return soma / contador

def validar_mes(mes_str):
    """
    Valida se a string é um número inteiro entre 1 e 12.
    """
    try:
        mes = int(mes_str)
        if 1 <= mes <= 12:
            return mes
    except:
        pass
    return None

def validar_ano(ano_str):
    """
    Valida se a string é um número inteiro entre 1900 e 2100.
    """
    try:
        ano = int(ano_str)
        if 1900 <= ano <= 2100:
            return ano
    except:
        pass
    return None

def salvar_dados_csv(dados, nome_arquivo):
    """
    Salva a lista de dados meteorológicos em um arquivo CSV.
    Garante que o arquivo tenha extensão '.csv'.
    """
    if not nome_arquivo.lower().endswith('.csv'):
        nome_arquivo += '.csv'
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for d in dados:
            linha = [
                d['data'].strftime('%d/%m/%Y'),
                f"{d['precipitacao']:.2f}",
                f"{d['temp_max']:.2f}",
                f"{d['temp_min']:.2f}",
                f"{d['umidade']:.2f}",
                f"{d['vento']:.2f}"
            ]
            writer.writerow(linha)
    print(f"Dados salvos no arquivo '{nome_arquivo}'.")

def salvar_medias_em_csv(medias, nome_arquivo):
    """
    Salva as médias calculadas em arquivo CSV.
    Garante que o arquivo tenha extensão '.csv'.
    """
    if not nome_arquivo.lower().endswith('.csv'):
        nome_arquivo += '.csv'
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['MêsAno', 'MediaTempMin'])
        for chave, valor in medias.items():
            writer.writerow([chave, f"{valor:.2f}" if valor is not None else ''])
    print(f"Médias salvas no arquivo '{nome_arquivo}'.")

def excluir_registro(dados):
    """
    Permite ao usuário excluir um registro com base em uma data.
    Retorna True se um registro foi excluído, False caso contrário.
    """
    data_str = input("Informe a data do registro a ser excluído (dd/mm/aaaa): ")
    try:
        data = datetime.strptime(data_str, '%d/%m/%Y')
    except ValueError:
        print("Data inválida.")
        return False

    registros_antes = len(dados)
    dados[:] = [d for d in dados if d['data'] != data]

    if len(dados) < registros_antes:
        print(f"Registro da data {data_str} excluído.")
        return True
    else:
        print("Nenhum registro encontrado para a data informada.")
        return False

def corrigir_registro(dados):
    """
    Permite corrigir os dados de um registro específico baseado na data.
    """
    data_str = input("Informe a data do registro a ser corrigido (dd/mm/aaaa): ")
    try:
        data = datetime.strptime(data_str, '%d/%m/%Y')
    except ValueError:
        print("Data inválida.")
        return False

    for d in dados:
        if d['data'] == data:
            try:
                precipitacao = float(input(f"Precipitação atual {d['precipitacao']}, novo valor: "))
                temp_max = float(input(f"Temperatura Máx atual {d['temp_max']}, novo valor: "))
                temp_min = float(input(f"Temperatura Min atual {d['temp_min']}, novo valor: "))
                umidade = float(input(f"Umidade atual {d['umidade']}, novo valor: "))
                vento = float(input(f"Vento atual {d['vento']}, novo valor: "))
            except ValueError:
                print("Entrada inválida para os valores numéricos.")
                return False

            d['precipitacao'] = precipitacao
            d['temp_max'] = temp_max
            d['temp_min'] = temp_min
            d['umidade'] = umidade
            d['vento'] = vento

            print("Registro atualizado com sucesso.")
            return True

    print("Registro não encontrado para a data informada.")
    return False

def main():
    print("Selecione o arquivo CSV com os dados meteorológicos.")
    arquivo = selecionar_arquivo()
    if not arquivo:
        print("Nenhum arquivo selecionado. Encerrando.")
        return

    dados = carregar_dados(arquivo)
    print(f"{len(dados)} registros carregados do arquivo '{arquivo}'.")

    medias_cache = None
    mes_cache = None

    while True:
        print("\nMenu:")
        print("1 - Visualizar intervalo de dados (texto)")
        print("2 - Mês/ano mais chuvoso")
        print("3 - Média geral da temperatura mínima de um mês (2006-2016)")
        print("4 - Média da temperatura mínima de um mês por ano (2006-2016) e gráfico")
        print("5 - Salvar dados atualizados")
        print("6 - Salvar médias calculadas")
        print("7 - Excluir registro")
        print("8 - Corrigir registro")
        print("9 - Sair")

        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            mes_ini = validar_mes(input("Mês inicial (1-12): "))
            ano_ini = validar_ano(input("Ano inicial (ex: 1961): "))
            mes_fim = validar_mes(input("Mês final (1-12): "))
            ano_fim = validar_ano(input("Ano final (ex: 2016): "))
            if None in (mes_ini, ano_ini, mes_fim, ano_fim):
                print("Entrada inválida para mês ou ano.")
                continue
            if (ano_ini, mes_ini) > (ano_fim, mes_fim):
                print("O período inicial deve ser anterior ao final.")
                continue

            print("1 - Todos os dados")
            print("2 - Apenas precipitação")
            print("3 - Apenas temperatura")
            print("4 - Apenas umidade e vento")
            opcao = input("Escolha a visualização desejada: ")
            if opcao not in ['1', '2', '3', '4']:
                print("Opção inválida.")
                continue

            visualizar_intervalo(dados, mes_ini, ano_ini, mes_fim, ano_fim, int(opcao))

        elif escolha == '2':
            mes_mais_chuvoso(dados)

        elif escolha == '3':
            mes = validar_mes(input("Informe o mês para calcular a média (1-12): "))
            if mes is None:
                print("Mês inválido.")
                continue
            medias_cache = media_temp_min_mes_anos(dados, mes)
            mes_cache = mes
            print("Médias anuais calculadas:")
            for chave, valor in medias_cache.items():
                if valor is not None:
                    print(f"{chave}: {valor:.2f} °C")
                else:
                    print(f"{chave}: Sem dados")

        elif escolha == '4':
            if medias_cache is None:
                print("Por favor, calcule a média do mês primeiro (opção 3).")
                continue
            plotar_grafico_barras(medias_cache, mes_cache)

        elif escolha == '5':
            nome_arquivo = input("Informe o nome do arquivo para salvar os dados atualizados (ex: dados_atualizados.csv): ")
            salvar_dados_csv(dados, nome_arquivo)

        elif escolha == '6':
            if medias_cache is None:
                print("Nenhuma média calculada. Calcule a média primeiro (opção 3).")
                continue
            nome_arquivo = input("Informe o nome do arquivo para salvar as médias (ex: medias.csv): ")
            salvar_medias_em_csv(medias_cache, nome_arquivo)

        elif escolha == '7':
            if excluir_registro(dados):
                print("Lembre-se de salvar os dados após exclusão para manter as alterações.")

        elif escolha == '8':
            if corrigir_registro(dados):
                print("Lembre-se de salvar os dados após correção para manter as alterações.")

        elif escolha == '9':
            print("Encerrando o programa.")
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    main()
