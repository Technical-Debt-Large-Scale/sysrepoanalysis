# Consumidor da fila 'fila_operacoes_arquivos_local'
import pika
import msr.utils as util
from tqdm import tqdm
import time
from msr.dao import Repository, Repositories
import os
import json
import logging

# Remove all handlers associated with the root logger object.
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                datefmt='%d/%m/%Y %H:%M:%S', filename='logs/my_app_consumidor_gera_json.log', filemode='w')

# Collection to manipulate repositories in data base
repositoriesCollection = Repositories()
 
rabbitmq_broker_host = 'localhost'
my_fila1 = 'fila_operacoes_arquivos_local'
my_fila2 = 'fila_analisador'
my_fila3 = 'fila_sccatter_plot'

connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_broker_host, heartbeat=0))

channel_to_generate_file = connection.channel()
channel_to_generate_file.queue_declare(queue=my_fila1, durable=True)

channel_to_analysis = connection.channel()
channel_to_analysis.queue_declare(queue=my_fila2, durable=True)

channel_to_scatter_plot = connection.channel()
channel_to_scatter_plot.queue_declare(queue=my_fila3, durable=True)

def atualizar_status_no_banco(user, repositorio, status):
    msg1 = f'Atualiza o status {status} do {repositorio} no banco na area do usuario: {user}' 
    msg2 = f'Status {status} do {repositorio} salvo no banco com sucesso!' 
    try:
        print(msg1)
        logging.info(msg1)
        nome_repositorio = util.pega_nome_repositorio(repositorio)
        repositoriesCollection.update_repository_by_name(nome_repositorio, user, 2)
        print(msg2)
        logging.info(msg2)
    except Exception as e:
        print(f'Erro: {str(e)}')
        logging.error("Exception occurred", exc_info=True)

def user_directory(path_repositories, user_id):
    user_path = path_repositories + '/' + str(user_id)
    if os.path.exists(user_path):
        return user_path
    else: 
        os.makedirs(user_path)
        return user_path  

def save_dictionary_in_json_file(name, user_id, my_dictionary, path_repositories): 
    try: 
        singleName = name + ".json"
        #Create the user directory if not existe
        temp_path = user_directory(path_repositories, user_id)
        fileName =  temp_path + '/' + singleName
        msg1 = f'Saving the file {singleName}...' 
        print(msg1)
        logging.info(msg1)
        with open(fileName, 'w', encoding="utf-8") as jsonFile:
            json.dump(my_dictionary, jsonFile)
        msg2 = f'The file {singleName} was saved with success!' 
        print(msg2)
        logging.info(msg2)
    except Exception as e:
        print(f'Error when try to save the json file: {e}')
        logging.error("Exception occurred", exc_info=True)

def gerar_arquivos_json(user, repositorio, nome_repositorio, my_json):
    try:
        my_dictionary = json.loads(my_json)
        save_dictionary_in_json_file(nome_repositorio, user, my_dictionary, util.Constants.PATH_REPOSITORIES)
        status = 'Analisado'
        atualizar_status_no_banco(user, repositorio, status)
    except Exception as ex:
        print(f'Erro: {str(ex)}')
        logging.error("Exception occurred", exc_info=True)

def generate_file_callback(ch, method, properties, body):
    body = body.decode('utf-8')
    if 'user' in body:
        try:
            user, repositorio, nome_repositorio, status, my_json = util.parser_body_com_json(body)
            gerar_arquivos_json(user, repositorio, nome_repositorio, my_json)
            # 4.2. Enfilera pedido de análise de commits do repositório (14) (produtor)
            # dentro da funcao principal de callback
            msg_generate_scatter_plot(canal=channel_to_scatter_plot, fila=my_fila3, usuario=user, repositorio=repositorio, status=status)
            msg_analysis_treemap_repositorio(canal=channel_to_analysis, fila=my_fila2, usuario=user, repositorio=repositorio, status='Em analise')
        except Exception as ex:
            print(f'Erro: {str(ex)}')     
            logging.error("Exception occurred", exc_info=True)

def msg_generate_scatter_plot(canal=channel_to_scatter_plot, fila=my_fila3, usuario='', repositorio='', status=''):
    tipo = 'gera scatter plot'
    util.enfilera_pedido_msg(canal, fila, usuario, repositorio, status, tipo)

# 4.1. Dispara uma solicitação para analisar os commits do repositório (13)
def msg_analysis_treemap_repositorio(canal=channel_to_analysis, fila=my_fila2, usuario='', repositorio='', status=''):
    tipo = 'analysis'
    util.enfilera_pedido_msg(canal, fila, usuario, repositorio, status, tipo)
 
channel_to_generate_file.basic_consume(my_fila1, generate_file_callback, auto_ack=True)
 
print(' [*] Waiting for messages to generate JSON file from repository. To exit press CTRL+C')
channel_to_generate_file.start_consuming()
