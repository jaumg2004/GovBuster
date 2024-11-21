from escavador import CriterioOrdenacao, Ordem, config
from escavador.v2 import Processo
from flask import Flask, request, jsonify, render_template
import time
import os
import pandas as pd

app = Flask(__name__, template_folder='Template', static_folder='Static')

# Configurando a chave de API
config("eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIxIiwianRpIjoiNWVhYTcwYzc0MjYxNDBlZmI5MTQ2ZThlMjg2NDZlZDQzNzZmOGVmZjZhZjgwYTFlNmU5YWFjMjVhOWM0NDBjNDdjNDc1NWFhN2VkY2JhZDYiLCJpYXQiOjE3MzE3NzU0NDQuNDE3NzYyLCJuYmYiOjE3MzE3NzU0NDQuNDE3NzYzLCJleHAiOjIwNDczMDgyNDQuNDE1ODQxLCJzdWIiOiIyMDk2NzgyIiwic2NvcGVzIjpbImFjZXNzYXJfYXBpX3BhZ2EiXX0.qqz3MyDG_3opdd5ZeawVR6yQzysucN7aubQRQjG2c1v-2GrSFaIEwtxP_FqfTv6AEuHB9nmMAO7zp5MAKqiGrVkSXkiQ3kMd3xsnz5uU2ZgdYOcyLFwvQ-ESKAZ1n2_Bm8iAV_gvoTTBviYI1JE3AsqK-mRhJQ5viUEs523aYmw7C9NqpBbGa4s0k9WoRFtc8vYSNh4-ezw89GYyus53BHPyJ25KxnL3cPgAvlIuPR6MpGqKT_miPq_nbzCwP2cZBVR-GpAw712KmzHjS5zm-rpAyxdL7kDt7A74uhdBg-7roWnpc6bszgoTYJATQbE-Ak5VfY8HApMqwTyzgCe-N7Pedl2B-6nk0RW0MgFcnN7ptjn1Sl_l0SQTIMYhw5vnIxzjphdLx2XxKtRdcgIdrDTsIKBG-VI6ZkDmEC7LBtTHPkeRUYVzBx8HGZhpCxRegYnbGZyqy-TR_bXgHElU3TTzCI63H9_cz5sBDARSuOjWoBSMELyRxejwkxO0-JYUjSvVY0iuftDsz86sZyfmiy7v_oCGhrXIKBl8bVnBfg_rbTrWFwAcn2BIjaIUL-aECAG_8rfjz5sN1Sz2SngT8GumyyjBJ1IT6mTBQB8TQG-Eip-maSKb8p_-Vpfxbg2fg2Kkk7uXlCCtl1WHm_s_HGC6HsvPBdBYnxMufjLxz7I")

pasta_csv = r'C:\Users\Jaum\Documents\comand'

# Lista para armazenar os DataFrames
dataframes = []

# Loop pelos arquivos na pasta
for arquivo in os.listdir(pasta_csv):
    if arquivo.endswith(".csv"):  # Verifica se é um arquivo CSV
        caminho_arquivo = os.path.join(pasta_csv, arquivo)
        df = pd.read_csv(caminho_arquivo, encoding='latin1', delimiter=';')
        dataframes.append(df)  # Adiciona o DataFrame à lista

# Concatenar todos os DataFrames em um só (opcional)
df_final = pd.concat(dataframes, ignore_index=True)

# Função para verificar se o nome está nos arquivos CSV
def nome_presente_nos_csv(nome):
    if nome in df_final['NM_CANDIDATO'].values:
        return True
    return False  # Nome não encontrado

# Função para buscar o caminho da foto do candidato
def encontrar_foto(nome):
    # Verifique se a foto existe na pasta de imagens estáticas
    foto_path = f"Static/img/{nome}.jpg"
    if os.path.exists(foto_path):
        return foto_path
    else:
        return "static/images/default.jpg"  # Caminho para uma imagem padrão, caso não tenha foto


# Função para buscar o partido do candidato
def buscar_partido(nome):
    # Verifica se o nome está no DataFrame
    candidato = df_final[df_final['NM_CANDIDATO'] == nome]

    if not candidato.empty:
        # Retorna o partido do candidato
        return candidato['NM_PARTIDO'].values[0]
    else:
        return "Partido não encontrado"  # Caso o candidato não seja encontrado

# Controle de taxa
request_tracker = {}
MAX_REQUESTS = 5       # Limite de requisições permitido por IP
TIME_WINDOW = 60 * 60   # Janela de tempo para limite (1 hora)

# Função para limitar requisições
def is_rate_limited(ip):
    current_time = time.time()
    requests = request_tracker.get(ip, [])
    requests = [req_time for req_time in requests if current_time - req_time < TIME_WINDOW]
    request_tracker[ip] = requests
    if len(requests) >= MAX_REQUESTS:
        return True
    requests.append(current_time)
    return False

# Função para realizar a consulta de processos por nome
def consultar_processos(nome):
    # Primeiro verifica se o nome está nos arquivos CSV
    if not nome_presente_nos_csv(nome):
        return {"erro": "Nome não encontrado nos registros locais. Verifique os arquivos CSV."}

    # Se o nome estiver nos arquivos, realiza a consulta nos processos
    try:
        envolvido, processos = Processo.por_nome(nome=nome, ordena_por=CriterioOrdenacao.INICIO, ordem=Ordem.DESC)
        dados_processos = []
        if processos:
            for processo in processos:
                processo_data = {
                    "numero_cnj": processo.numero_cnj,
                    "fonte": processo.fontes[0].nome if processo.fontes else 'Fonte não disponível',
                    "data_inicio": processo.data_inicio
                }
                movimentacoes = Processo.movimentacoes(numero_cnj=processo.numero_cnj)
                if movimentacoes:
                    processo_data["ultima_movimentacao"] = movimentacoes[0].conteudo
                dados_processos.append(processo_data)
        return dados_processos
    except Exception as e:
        print(f"Ocorreu um erro ao consultar os processos: {e}")
        return {"erro": "Erro interno ao consultar os processos"}

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para buscar processos
@app.route('/govbuster', methods=['GET'])
def govbuster():
    ip = request.remote_addr
    if is_rate_limited(ip):
        return jsonify({"erro": "Limite de requisições excedido. Tente novamente mais tarde."}), 429

    nome = request.args.get('nome')
    if not nome:
        return jsonify({"erro": "Nome do candidato não fornecido"}), 400

    nome = nome.upper()

    # Buscar o partido do candidato
    partido = buscar_partido(nome)

    # Consultar os processos
    processos = consultar_processos(nome)
    foto_caminho = encontrar_foto(nome)

    if processos is None:
        return jsonify({"erro": "Erro ao consultar os processos"}), 500
    elif not processos:
        return jsonify({"mensagem": "Nenhum processo encontrado para o nome fornecido"}), 404
    else:
        return jsonify({
            "partido": partido,
            "processos": processos,
            "foto_url": foto_caminho
        }), 200

if __name__ == '__main__':
    app.run(debug=True)
