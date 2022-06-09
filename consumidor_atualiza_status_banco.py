# Consumidor e Produtor
# Consumidor da fila 'fila_status_banco'
# Produtor na fila 'fila_analise_commits'

import pika
import msr.utils as util
from msr.dao import Repository, Repositories
import logging

# Remove all handlers associated with the root logger object.
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    datefmt='%d/%m/%Y %H:%M:%S', filename='logs/my_app_consumidor_atualiza_status_banco.log', filemode='w')

# Collection to manipulate repositories in data base
repositoriesCollection = Repositories()
 
rabbitmq_broker_host = 'localhost'
my_fila1 = 'fila_status_banco'
my_fila2 = 'fila_analise_commits'

connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_broker_host, heartbeat=0))

channel_to_update_db = connection.channel() 
channel_to_update_db.queue_declare(queue=my_fila1, durable=True)

channel_to_analysis = connection.channel()
channel_to_analysis.queue_declare(queue=my_fila2, durable=True)


def atualizar_status_no_banco(user, repositorio, status):
    msg1 = f'Atualiza o status {status} do {repositorio} no banco na area do usuario: {user}' 
    msg2 = f'Status {status} do repositorio {repositorio} atualizdo com sucesso!'
    try:
        print(msg1)
        logging.info(msg1)
        nome_repositorio = util.pega_nome_repositorio(repositorio)
        repositoriesCollection.update_repository_by_name(nome_repositorio, user, 1)
        print(msg2)
        logging.info(msg2)
    except Exception as e:
        print(f'Erro: {str(e)}')
        logging.error("Exception occurred", exc_info=True)

def update_db_callback(ch, method, properties, body):
    body = body.decode('utf-8')
    if 'user' in body:
        try:
            user, repositorio, nome_repositorio, status = util.parser_body(body)
            atualizar_status_no_banco(user, repositorio, status)
            # 4.2. Enfilera pedido de análise de commits do repositório (14) (produtor)
            msg_analysis_db_repositorio(canal=channel_to_update_db, fila=my_fila2, usuario=user, repositorio=repositorio, status='Em analise')
            
        except Exception as ex:
            print(f'Erro: {str(ex)}')     

# 4.1. Dispara uma solicitação para analisar os commits do repositório (13)
def msg_analysis_db_repositorio(canal=channel_to_update_db, fila=my_fila2, usuario='', repositorio='', status=''):
    tipo = 'analysis'
    util.enfilera_pedido_msg(canal, fila, usuario, repositorio, status, tipo)


channel_to_update_db.basic_consume(my_fila1, update_db_callback, auto_ack=True)
 
print(' [*] Waiting for messages to update in DB. To exit press CTRL+C')
channel_to_update_db.start_consuming()