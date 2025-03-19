from influxdb_client import InfluxDBClient
from openpyxl import Workbook
from datetime import datetime
import pandas as pd

def salvar_arquivo_excel(measurements, tables, workbook):
    print("Preparando as guias para os measurements:", measurements)

    # Criar guias no workbook para cada measurement
    for measurement in measurements:
        sheet = workbook.create_sheet(title=measurement)

        # Preencher a primeira linha com os nomes das colunas
        columns = []
        for table in tables:
            if not table.empty and table['_measurement'].unique()[0] == measurement:
                columns += table.columns.tolist()
        sheet.append(columns)

        # Preencher as células com os dados do DataFrame
        contador_iteracao = 0
        for table in tables:
            if not table.empty:
                records = table.loc[table['_measurement'] == measurement].to_records(index=False)

                for record in records:
                    values = list(record)
                    contador_iteracao += 1
                    # converter datas para UTC
                    values = [value.strftime('%Y-%m-%d-%H:%M:%S') if isinstance(value, datetime) else value for value in values]
                    sheet.append(values)
                    if contador_iteracao <= 50:
                        print("#", end='')
        print(f'\nGuia para o measurement {measurement} pronta!')

# Configurações do InfluxDB
url = "http://192.168.0.250:8086"
token = "AtSpC6Roh28nNlhY2jgcyNwFhj93Fjw11j0Ks2L_TSy__xvkOduUCl1ORJyccLfqhCh1IF14o0fablsI7beTnA=="
org = "Femsa"

# Measurements a serem processados
measurements = ["Filtracao", "CIP_ciclos", "Dissol25m3h", "Pasteurizador", "RegenClarifica","Dissol12m3h", "Est_de_Conc", "Desaerador"]

# Iniciar o cliente InfluxDB
client = InfluxDBClient(url=url, token=token, org=org)

# Criar um novo arquivo do Excel
print('\nPreparando o Workbook!!!')
workbook = Workbook()

# Consulta para recuperar dados para todos os measurements
query = f'from(bucket:"XAROPARIA") |> range(start:-24h, stop: now()) |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'
result = client.query_api().query_data_frame(query=query)
tables = result

# Salvar os dados em guias separadas para cada measurement
salvar_arquivo_excel(measurements, tables, workbook)

# Fechar a conexão com o InfluxDB
client.close()

# Salvar o arquivo do Excel
excel_filename = 'dados_measurements.xlsx'
workbook.save(excel_filename)
workbook.close()

print(f"\nTodos os dados foram salvos no arquivo Excel: {excel_filename}")

# nova implementação


# Supondo que 'seu_workbook.xlsx' seja o nome do arquivo Excel com várias planilhas
nome_do_workbook = 'dados_measurements.xlsx'

# Carregar o workbook usando pandas
xls = pd.ExcelFile(nome_do_workbook)

# Criar um dicionário para armazenar DataFrames de últimas linhas por planilha
nomes_planilhas = []
valvulas = []
ciclos = []

# Iterar sobre as planilhas no workbook
for sheet_name in xls.sheet_names:
    # Carregar cada planilha
    df = pd.read_excel(nome_do_workbook, sheet_name=sheet_name)
    # Excluir as linhas de 1 a 5
    #df = df.iloc[5:]

    # Verificar se a planilha tem pelo menos uma linha
    if not df.empty:
        # Obter o nome da planilha
        nomes_planilhas.extend([sheet_name]* len(df.columns[1:]))
        
        # Obter os rótulos das medidas e os valores correspondentes
        medidas = df.columns[1:]
        valores = df.iloc[0, 1:]
        
        # obter os rotulos e os valores das medidas
        valvulas.extend(df.columns[1:])
        ciclos.extend(df.iloc[0, 1:].tolist())

# Criar um DataFrame com os dados finais
dados_finais_df = pd.DataFrame({'Processo': nomes_planilhas, 'Válvulas': valvulas, 'Ciclos': ciclos})

#Excluir linhas
dados_finais_df = dados_finais_df[~dados_finais_df['Válvulas'].isin(['table', '_start', '_stop', '_time', '_measurement'])]

# Salvar os dados finais em um novo arquivo Excel
dados_finais_df.to_excel('dados_finais.xlsx', index=False)

print("Arquivo 'dados_finais.xlsx' gerado com sucesso.")