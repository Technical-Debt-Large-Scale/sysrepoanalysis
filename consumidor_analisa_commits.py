# Consumidor e Produtor
# Consumidor da fila 'fila_analise_commits'
# Produtor na fila 'fila_operacoes_arquivos_local'

import pika
import msr.utils as util
from tqdm import tqdm
import time
from pydriller import Repository
import json
import logging

# Remove all handlers associated with the root logger object.
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    datefmt='%d/%m/%Y %H:%M:%S', filename='logs/my_app_consumidor_analisa_commits.log', filemode='w')
 
rabbitmq_broker_host = 'localhost'
my_fila1 = 'fila_analise_commits'
my_fila2 = 'fila_operacoes_arquivos_local'
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_broker_host, heartbeat=0))

channel_to_analysis = connection.channel() 
channel_to_analysis.queue_declare(queue=my_fila1, durable=True)

channel_to_generate_file = connection.channel()
channel_to_generate_file.queue_declare(queue=my_fila2, durable=True)

# List all Commits from Authors
# return a dictionary like this: hash, author, date, list of files in commit
# dictionary = {'hash': ['author', 'date of commit', [file1, file2, ...]]}
def dictionaryWithAllCommmits(client, repository):
    dictionaryAux = {}
    try: 
        for commit in Repository(repository).traverse_commits():
            commitAuthorNameFormatted = '{}'.format(commit.author.name)
            commitAuthorDateFormatted = '{}'.format(commit.author_date)
            listFilesModifiedInCommit = []
            for modification in commit.modified_files:
                itemMofied = '{}'.format(modification.filename)
                listFilesModifiedInCommit.append(itemMofied)
            dictionaryAux[commit.hash] = [commitAuthorNameFormatted, commitAuthorDateFormatted, listFilesModifiedInCommit] 
        logging.info(f'Dicionário gerado com sucesso')
        logging.info(dictionaryAux)
    except Exception as e:
        print(f'Error during processing dictionaryWithAllCommmits in {repository} error: {e}')
        logging.error("Exception occurred", exc_info=True)
        dictionaryAux = None
    return dictionaryAux

def analisar_repositorio(user, repositorio, nome_repositorio):
    msg1 = f'Analisando o {repositorio}, na area do usuario: {user} ...' 
    print(msg1)
    logging.info(msg1)
    path_repositorio = util.Constants.PATH_REPOSITORIES + '/' + user + '/' + nome_repositorio
    return dictionaryWithAllCommmits(user, path_repositorio)

def analise_callback(ch, method, properties, body):
    body = body.decode('utf-8')
    if 'user' in body:
        try:
            user, repositorio, nome_repositorio, status = util.parser_body(body)
            resultado_analise = analisar_repositorio(user, repositorio, nome_repositorio)  
            resultado_analise = json.dumps(resultado_analise)        
            msg1 = f'Análise do repositório {repositorio} concluida!' 
            print(msg1)
            logging.info(msg1)
            # 5.8. Enfilera pedido de gerar arquivo JSON do repositório (20) (produtor)
            msg_generate_file_repositorio(canal=channel_to_generate_file, fila=my_fila2, usuario=user, repositorio=repositorio, status=status, resultado=resultado_analise)
        except Exception as ex:
            print(f'Erro: {str(ex)}')     

# 5.7. Dispara uma solicitação para gerar o JSON com as respostas da análise do repositório (19)
def msg_generate_file_repositorio(canal=channel_to_generate_file, fila=my_fila2, usuario='', repositorio='', status='', resultado=''):
    tipo = 'gerar arquivo JSON'
    util.enfilera_pedido_msg_com_json(canal, fila, usuario, repositorio, status, tipo, resultado)
 
channel_to_analysis.basic_consume(my_fila1, analise_callback, auto_ack=True)

print(' [*] Waiting for messages to analysis queue. To exit press CTRL+C') 
channel_to_analysis.start_consuming()