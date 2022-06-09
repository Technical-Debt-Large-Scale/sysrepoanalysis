# Consumidor da fila 'fila_operacoes_arquivos_local'
import pika
import msr.utils as util
from msr.dao import Repository, Repositories
import logging
import pandas as pd
import msr.miner as miner
import msr.analysis_scatter_plot as analysis

# Remove all handlers associated with the root logger object.
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                datefmt='%d/%m/%Y %H:%M:%S', filename='logs/my_app_consumidor_gera_json.log', filemode='w')

#user_id = 1
#nome_repositorio1 = "promocityteste"
#url_repositorio1 = "https://github.com/myplayareas/promocityteste.git"

repositoriesCollection = Repositories()
rabbitmq_broker_host = 'localhost'
my_fila1 = 'fila_sccatter_plot'
my_fila3 = 'fila_analise_metricas'

connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_broker_host, heartbeat=0))

channel_to_scatter_plot = connection.channel()
channel_to_scatter_plot.queue_declare(queue=my_fila1, durable=True)

channel_to_analysis_metrics = connection.channel()
channel_to_analysis_metrics.queue_declare(queue=my_fila3, durable=True)


def clona_repositorio_local(user_id, url_repositorio1, nome_repositorio1):
    temp_user_directory = analysis.temp_user_directory(user_id, 'sp') 
    print(f'Clona o repositorio {nome_repositorio1} detro do diretorio {temp_user_directory}')
    path_to_save_clone = temp_user_directory + '/' + nome_repositorio1 
    analysis.clona_repositorio(url_repositorio1, path_to_save_clone)
    return path_to_save_clone

def prepare_files_and_directories(user_id, nome_repositorio1):
    # Substitui o . pelo repositorio/
    list_of_files_and_directories = analysis.get_list_of_files_and_directories_updated(user_id, nome_repositorio1, 'sp')
    # Escolhe o diretorio do source java
    # Lista apenas arquivos e diretorios do src/main/java
    list_of_files_and_directories_src = analysis.get_list_of_files_and_directories_src(user_id, nome_repositorio1)
    # Cria um arquivo contendo a quantidade de LOC por arquivo
    list_locs_of_files_updated = analysis.get_list_locs_of_files(user_id, nome_repositorio1, 'sp')
    # Lista todos os commits de um repositorio
    return list_of_files_and_directories, list_of_files_and_directories_src, list_locs_of_files_updated

def performing_scatter_plot(path_to_save_clone, nome_repositorio1, path_repository_user):
    list_commits_promocity = miner.list_all_commits(path_to_save_clone)
    # Lista todos os arquivos modificados em cada commit
    dict_modified_files_promocity = miner.list_all_modified_files_in_commits(path_to_save_clone)
    # Lista todos os commits e seus arquivos modificados
    #for commit, lista_files in dict_modified_files_promocity.items(): 
    #  print(commit, [file.filename for file in lista_files])

    # 5. Lista a frequência dos arquivos nos commits
    dict_frequency_files_commits = miner.get_files_frequency_in_commits(path_to_save_clone)

    # 6. Lista a Quantidade de Linhas de Código Modificadas em cada Arquivo
    dict_lines_modified_in_files = miner.get_number_of_lines_of_code_changes_in_commits(path_to_save_clone)
    dict_java_frequency_commits = analysis.get_dict_java_frequency_commits(dict_frequency_files_commits)
    if len(dict_java_frequency_commits) > 0: 
        dict_java_lines_modified = analysis.get_dict_java_lines_modified(dict_lines_modified_in_files)

        # Converte o dicionário dict_java_frequency_commits em um dataframe
        df_java_frequency_commits = analysis.convert_dict_java_frequency_to_dataframe(dict_java_frequency_commits)
        # Converte o dicionário dict_java_lines_modified em um dataframe
        df_java_lines_modified = analysis.convert_dict_java_lines_modified_to_dataframe(dict_java_lines_modified)

        # Faz o merge das informações para criar um dataframe contendo o arquivo, a frequência de Commits e Linhas Modificadas de cada arquivo ao longo do tempo
        df_fc_ml = analysis.merge_dataframes_java_frequency(df_java_frequency_commits, df_java_lines_modified)
        df_fc_ml
        #print(f'{df_fc_ml}')

        analysis.generate_sccater_plot(df_fc_ml, nome_repositorio1, path_repository_user)
        # generate_sccater_plot_2(df_fc_ml, repositorio1)

        df_boxplot_fc = analysis.generate_box_plot_frequency(df_fc_ml, nome_repositorio1, path_repository_user)
        fc_q1, fc_q2, fc_q3, fc_q4 = analysis.get_quartiles_frequency(df_boxplot_fc)
        print(f'Quartis da Frequencia de Commits Q1: {fc_q1}, Q2: {fc_q2}, Q3: {fc_q3}, Q4: {fc_q4}')

        df_boxplot_lm = analysis.generate_box_plot_lines_modified(df_fc_ml, nome_repositorio1, path_repository_user)
        lm_q1, lm_q2, lm_q3, lm_q4 = analysis.get_quartiles_lines_modified(df_boxplot_lm)
        print(f'Quartis da Linhas Modificadas Q1: {lm_q1}, Q2: {lm_q2}, Q3: {lm_q3}, Q4: {lm_q4}')

        # Gera o arquivo .csv dos quartils
        path_file_quadrants_fc_lm = path_repository_user + '/' + nome_repositorio1 + '_' + 'quadrants_fc_lm' + '.csv'
        dict_quadrants = {'qfc_q1':fc_q1[0], 'qfc_q2':fc_q2[0], 'qfc_q3':fc_q3[0], 'qfc_q4':fc_q4[0], 'qlm_q1':lm_q1[0], 'qlm_q2':lm_q2[0], 'qlm_q3':lm_q3[0], 'qlm_q4':lm_q4[0]}
        df_quadrants = pd.DataFrame([dict_quadrants])
        df_quadrants.to_csv(path_file_quadrants_fc_lm)
        
        # Lista os arquivos com maior frequência de commits e mais linhas modificadas ao longo do tempo
        my_query = f"Frequency >= {fc_q3[0]} and lines_modified >= {lm_q3[0]}"
        print(my_query)
        df_arquivos_criticos = df_fc_ml.query(my_query)
        util.create_csv_from_df(path_repository_user, nome_repositorio1, 'arquivos_criticos', df_arquivos_criticos)
        print(f'Arquivos críticos: {df_arquivos_criticos}')

        qtd_arquivos_criticos = df_arquivos_criticos.shape[0]
        qtd_arquivos_java = df_fc_ml.shape[0]
        print(f'Qtd arquivos críticos: {qtd_arquivos_criticos}, Total de Arquivos .java {qtd_arquivos_java}')
        print(f'{round(qtd_arquivos_criticos/qtd_arquivos_java, 2)*100}% dos arquivos .java são críticos')

        total_linhas_modificadas = sum(df_fc_ml['lines_modified'])
        linhas_modificadas_arquivos_criticos = sum(df_arquivos_criticos['lines_modified'])
        print(f'Qtd de linhas modificadas pelos arquivos críticos: {linhas_modificadas_arquivos_criticos}, Total de linhas de código alteradas ao longo do tempo: {total_linhas_modificadas}')
        print(f'{round(linhas_modificadas_arquivos_criticos/total_linhas_modificadas, 2)*100}% do esforço de modificação é com arquivos críticos')

        qaj = [qtd_arquivos_java]
        laaj = [total_linhas_modificadas]
        qac = [qtd_arquivos_criticos]
        pac = [round(qtd_arquivos_criticos/qtd_arquivos_java,2)*100]
        laac = [linhas_modificadas_arquivos_criticos]
        plaac = [round(linhas_modificadas_arquivos_criticos/total_linhas_modificadas, 2)*100]

        dict_ = {'Repository': [nome_repositorio1], 'qaj': qaj, 'qac': qac, 'laaj': laaj, 'laac': laac, 'pac': pac, 'plaac': plaac}
        df_from_dict = pd.DataFrame.from_dict(dict_)
        print(f'{df_from_dict}')
        if path_repository_user is not None:
            util.create_csv_from_df(path_repository_user, nome_repositorio1, 'resumo', df_from_dict)

        return True
    else: 
        print('Repositorio não é projeto java!')
        return False

def gerar_scatter_plot(user, repositorio, nome_repositorio):
    try:
        status = 'Scatter plot gerado'
        path_to_save_clone = clona_repositorio_local(user_id=user, url_repositorio1=repositorio, nome_repositorio1=nome_repositorio)
        path_repositorio = util.Constants.PATH_REPOSITORIES + '/' + user + '/' + nome_repositorio
        # list_of_files_and_directories, list_of_files_and_directories_src, list_locs_of_files_updated = prepare_files_and_directories(user_id=user, nome_repositorio1=nome_repositorio)
        projeto_java = performing_scatter_plot(path_to_save_clone, nome_repositorio1=nome_repositorio, path_repository_user=path_repositorio)
        if projeto_java:
            print(f'Scatter plot gerado para o usuario: {user}, repositorio: {repositorio}, nome do repositorio: {nome_repositorio}')
        else:
            print(f'Não foi geraado o scatter plot no usuário: {user}, por que o repositorio {repositorio} não é java')
    except Exception as ex:
        print(f'Erro: {str(ex)}')
        logging.error("Exception occurred", exc_info=True)

def generate_scatter_plot_callback(ch, method, properties, body):
    body = body.decode('utf-8')
    if 'user' in body:
        try:
            user, repositorio, nome_repositorio, status = util.parser_body(body)
            path_repositorio = util.Constants.PATH_REPOSITORIES + '/' + user + '/' + nome_repositorio
            gerar_scatter_plot(user, repositorio, nome_repositorio)
            msg_analysis_metrics_repositorio(canal=channel_to_analysis_metrics, fila=my_fila3, usuario=user, repositorio=repositorio, status='Analisando Métricas')
        except Exception as ex:
            print(f'Erro: {str(ex)}')     
            logging.error("Exception occurred", exc_info=True)

# 4.1. Dispara uma solicitação para analisar as metricas do repositório (13)
def msg_analysis_metrics_repositorio(canal=channel_to_analysis_metrics, fila=my_fila3, usuario='', repositorio='', status=''):
    tipo = 'analysis metrics'
    util.enfilera_pedido_msg(canal, fila, usuario, repositorio, status, tipo)
 
channel_to_scatter_plot.basic_consume(my_fila1, generate_scatter_plot_callback, auto_ack=True)
 
print(' [*] Waiting for messages to generate scatter plot from repository. To exit press CTRL+C')
channel_to_scatter_plot.start_consuming()