# Produtor da fila 'fila_repositorio_local'
import pika
import msr.utils as util
import logging

# Remove all handlers associated with the root logger object.
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S', filename='./logs/my_app_produtor_clona_repositorio.log', filemode='w')

rabbitmq_host = 'localhost'
my_fila = 'fila_repositorio_local'

connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host, heartbeat=0))
channel_to_clone = connection.channel() 
channel_to_clone.queue_declare(queue=my_fila, durable=True)

# 2.2. Enfilera pedido de clonagem do repositório (6) (produtor)
def msg_clona_repositorio(canal=channel_to_clone, fila=my_fila, usuario='', repositorio='', status=''):
    tipo = 'clonagem'
    logging.info(f"User: {usuario}, Repository {repositorio} queued in queue {my_fila}")
    util.enfilera_pedido_msg(canal, fila, usuario, repositorio, status, tipo)
    