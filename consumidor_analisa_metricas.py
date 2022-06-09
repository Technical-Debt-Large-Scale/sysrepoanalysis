# Consumidor
# Consumidor da fila 'fila_analise_metricas'
import pika
import msr.utils as util
import logging
import msr.miner as miner
import pandas as pd

# Remove all handlers associated with the root logger object.
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    datefmt='%d/%m/%Y %H:%M:%S', filename='logs/my_app_consumidor_analisa_metricas.log', filemode='w')
 
rabbitmq_broker_host = 'localhost'
my_fila1 = 'fila_analise_metricas'
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_broker_host, heartbeat=0))

channel_to_analysis = connection.channel() 
channel_to_analysis.queue_declare(queue=my_fila1, durable=True)

# 1. Lista todos os commmits do repositorio
def get_all_commits(local_salva_repositorio, nome_repositorio):
    try:
        all_commits = miner.list_all_commits(local_salva_repositorio)
        print(f'Foram encontrados {len(all_commits)} commits no repositorio {nome_repositorio}')
    except Exception as ex:
        print(f'Erro get_all_commits: {str(ex)}')
    return all_commits

def get_df_from_all_commits(local_salva_repositorio, nome_repositorio, all_commits):
    try:
        dict_from_all_commits = util.craete_dict_commits(nome_repositorio, all_commits)
        df_from_all_commits = util.get_dataframe_from_all_commits(dict_from_all_commits)
        filename = util.create_csv_from_all_commits(local_salva_repositorio, nome_repositorio, df_from_all_commits)
        print(df_from_all_commits.info())
        print(f'Arquivo gerado: {filename}')
    except Exception as ex:
        print(f'Erro df_from_all_commits: {str(ex)}')
    return df_from_all_commits

def get_df_all_modified_files(local_salva_repositorio, nome_repositorio, all_commits):
    try:
        dict_all_modified_files = util.create_dict_from_all_modified_files_from_all_commits(all_commits)
        df_all_modified_files = util.get_dataframe_from_all_modified_files(dict_all_modified_files)
        filename = util.create_csv_from_all_modified_files(local_salva_repositorio, nome_repositorio, df_all_modified_files)
        print(f'{df_all_modified_files.info()}')
        print(f'Arquivos modificados: {filename}')
    except Exception as ex:
        print(f'Erro get_df_all_modified_files: {str(ex)}')
    return df_all_modified_files

# 3. Lista a frequencia de commits de cada arquivo no repositorio
# Frequencia de commits dos arquivos
## Gerar o dataframe
## Exportar dados da análise para arquivo .csv
def get_df_frequencia_commits(local_salva_repositorio, nome_repositorio):
    try:
        print('\n Frequencia de commits')
        # 9. Mostra a frequencia de commits de cada arquivo ao longo de todos os commits do repositorio
        files_frequency = miner.get_files_frequency_in_commits(local_salva_repositorio)
        dict_ff = util.create_dict_files_frequency(files_frequency)
        df_ff = util.get_dataframe_from_files_metric(dict_ff)
        filename_ff = util.create_csv_from_files_metric(local_salva_repositorio, nome_repositorio, df_ff, metric='files_frequency')
        print(f'Arquivo: {filename_ff}')
    except Exception as ex:
        print(f'Erro: {str(ex)}')
    return df_ff

        # 4. Lista as MLOCs de cada arquivo ao longo do tempo
        # 10. Mudancas de linhas dos arquivos ao longo de todos os commits
        ## Gerar o dataframe
        ## Exportar dados da análise para arquivo .csv
def get_df_mlocs(local_salva_repositorio, nome_repositorio):
    try:
        print('\n L changes')
        # 10. Mudancas de linhas dos arquivos ao longo de todos os commits
        files_lines_changes = miner.get_number_of_lines_of_code_changes_in_commits(local_salva_repositorio)
        dict_flc = util.create_dict_files_lines_changes(files_lines_changes)
        df_flc = util.get_dataframe_from_files_metric(dict_flc)
        filename_flc = util.create_csv_from_files_metric(local_salva_repositorio, nome_repositorio, df_flc, metric='files_lines_changes')
        print(f'Arquivo: {filename_flc}')
    except Exception as ex:
        print(f'Erro mlocs: {str(ex)}')
    return df_flc

    # 5. Lista a CC de cada arquivo ao longo do tempo
    # 11 CC dos arquivos ao longo de todos os commits
    ## Gerar o dataframe
    ## Exportar dados da análise para arquivo .csv
def get_df_cc_ao_longo_do_tempo(local_salva_repositorio, nome_repositorio):
    try:
        print('\n CC')
        # 11 CC dos arquivos ao longo de todos os commits
        files_cc = miner.get_files_cyclomatic_complexity_in_commits(local_salva_repositorio)
        dict_cc = util.create_dict_files_cc(files_cc)
        df_cc = util.get_dataframe_from_files_metric(dict_cc)
        filename_cc = util.create_csv_from_files_metric(local_salva_repositorio, nome_repositorio, df_cc, metric='files_cc')
        print(f'Arquivo: {filename_cc}')
    except Exception as ex:
        print(f'Erro: cc_ao_longo_do_tempo {str(ex)}')
    return df_cc

def get_df_composition(local_salva_repositorio, nome_repositorio, df_files_cc, df_files_frequency, df_files_lines_changes):
    try:
        print('\n Composition')
        # 10. Composicao das 3 metricas anteriores
        df_files_metrics_composition = pd.concat([df_files_cc, df_files_frequency, df_files_lines_changes], axis=1)
        df_files_metrics_composition = df_files_metrics_composition[['file', 'files_cc', 'frequency_in_commits', 'files_lines_changes']]
        df_files_metrics_composition = df_files_metrics_composition.drop(df_files_metrics_composition.columns[[1]], axis=1)
        df_files_metrics_composition['file'] = df_files_cc['file'] 
        df_files_metrics_composition['composition'] = df_files_metrics_composition['files_cc'] * df_files_metrics_composition['frequency_in_commits'] * df_files_metrics_composition['files_lines_changes']
        df_files_metrics_composition['ccxfc'] = df_files_metrics_composition['files_cc'] * df_files_metrics_composition['frequency_in_commits']
        df_files_metrics_composition['fcxflc'] = df_files_metrics_composition['frequency_in_commits'] * df_files_metrics_composition['files_lines_changes']
        df_files_metrics_composition = df_files_metrics_composition[['file', 'files_cc', 'frequency_in_commits', 'files_lines_changes', 'ccxfc', 'fcxflc', 'composition']]
        filename_fcomposition = util.create_csv_from_files_metric(local_salva_repositorio, nome_repositorio, df_files_metrics_composition, metric='files_composition')
        print(f'Arquivo: {filename_fcomposition}')
    except Exception as ex:
        print(f'Erro mlocs: {str(ex)}')
    return df_files_metrics_composition

def analisar_metricas(local_salva_repositorio, nome_repositorio):
    all_commits = get_all_commits(local_salva_repositorio, nome_repositorio)
    df_all_commits = get_df_from_all_commits(local_salva_repositorio, nome_repositorio, all_commits)
    df_all_modified_files = get_df_all_modified_files(local_salva_repositorio, nome_repositorio, all_commits)
    df_frequencia_commits = get_df_frequencia_commits(local_salva_repositorio, nome_repositorio)
    df_mlocs = get_df_mlocs(local_salva_repositorio, nome_repositorio)
    df_cc_ao_longo_do_tempo = get_df_cc_ao_longo_do_tempo(local_salva_repositorio, nome_repositorio)
    df_composition = get_df_composition(local_salva_repositorio, nome_repositorio, df_cc_ao_longo_do_tempo, df_frequencia_commits, df_mlocs)
    print(f'{df_all_commits.info()}')
    print(f'{df_all_modified_files.info()}')
    print(f'{df_frequencia_commits.info()}')
    print(f'{df_mlocs.info()}')
    print(f'{df_cc_ao_longo_do_tempo.info()}')
    print(f'{df_composition.info()}')

def analise_callback(ch, method, properties, body):
    body = body.decode('utf-8')
    if 'user' in body:
        try:
            user, repositorio, nome_repositorio, status = util.parser_body(body)
            path_repositorio = util.Constants.PATH_REPOSITORIES + '/' + user + '/' + nome_repositorio
            print(f'Path_repositorio: {path_repositorio}')
            print(f'Iniciando análise das métricas do {nome_repositorio}')
            analisar_metricas(path_repositorio, nome_repositorio)
            msg1 = f'Análise das métricas do repositório {repositorio} concluida!' 
            print(msg1)
            logging.info(msg1)
        except Exception as ex:
            print(f'Erro: {str(ex)}')     
 
channel_to_analysis.basic_consume(my_fila1, analise_callback, auto_ack=True)

print(' [*] Waiting for messages to analysis metrics queue. To exit press CTRL+C') 
channel_to_analysis.start_consuming()