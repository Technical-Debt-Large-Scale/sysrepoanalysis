import os
import logging
from pydriller import Repository
import pandas as pd

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                        datefmt='%d/%m/%Y %H:%M:%S', filename='my_app_produtor_clona_repositorio.log', filemode='w')

class Constants:
    PATH_MYADMIN = os.path.abspath(os.getcwd())
    PATH_MYAPP = PATH_MYADMIN + '/msr'
    PATH_STATIC = PATH_MYADMIN + '/msr/static'
    PATH_IMG = PATH_MYADMIN + '/msr/static/img'
    PATH_JSON = PATH_MYADMIN + '/msr/static/json'
    PATH_UPLOADS = PATH_MYADMIN + '/msr/static/uploads'
    PATH_REPOSITORIES = PATH_MYADMIN + '/msr/static/repositories'

def parser_body(body):
    user = ''
    repositorio = ''
    nome_repositorio = ''
    status = ''
    try:
        str_temp = body.split(',')
        user = str_temp[0].split('=')[1]
        repositorio = str_temp[1].split('=')[1] 
        status = str_temp[2].split('=')[1]      
        separa_ponto = repositorio.split('.')
        nome_repositorio_temp = separa_ponto[1]
        nome_repositorio = nome_repositorio_temp.split('/')[-1]
    except Exception as e:
        print(f'Error parser body - {e}')
        logging.error("Exception occurred", exc_info=True)
    return user, repositorio, nome_repositorio, status

def parser_body_com_json(body):
    user = ''
    repositorio = ''
    nome_repositorio = '' 
    status = ''
    my_json = ''
    try: 
        str_temp = body.split('#')
        user = str_temp[0].split('=')[1]
        repositorio = str_temp[1].split('=')[1] 
        status = str_temp[2].split('=')[1] 
        my_json = str_temp[3].split('=')[1]     
        separa_ponto = repositorio.split('.')
        nome_repositorio_temp = separa_ponto[1]
        nome_repositorio = nome_repositorio_temp.split('/')[-1]
    except Exception as e:
        print(f'Erro: {str(e)}')
        logging.error("Exception occurred", exc_info=True)
    return user, repositorio, nome_repositorio, status, my_json

def parser_body_com_json_metrica(body):
    user = ''
    repositorio = ''
    nome_repositorio = '' 
    status = ''
    metrica = ''
    my_json = ''
    try: 
        str_temp = body.split('#')
        user = str_temp[0].split('=')[1]
        repositorio = str_temp[1].split('=')[1] 
        status = str_temp[2].split('=')[1] 
        metrica = str_temp[3].split('=')[1]
        my_json = str_temp[4].split('=')[1]     
        separa_ponto = repositorio.split('.')
        nome_repositorio_temp = separa_ponto[1]
        nome_repositorio = nome_repositorio_temp.split('/')[-1]
    except Exception as e:
        print(f'Erro: {str(e)}')
        logging.error("Exception occurred", exc_info=True)
    return user, repositorio, nome_repositorio, status, metrica, my_json

def enfilera_pedido_msg(canal, fila, usuario, repositorio, status, tipo):
    msg1 = f'Conectando ao canal {canal} na fila {fila}'
    msg2 = f'Enviando o pedido de {tipo} do repositório {repositorio} do usuário {usuario}'
    print(msg1)
    print(msg2)
    logging.info(msg1) 
    logging.info(msg2)
    conteudo = 'user=' + usuario + ',' + 'repository=' + repositorio + ',' + 'status='+status
    canal.basic_publish(exchange='', routing_key=fila, body=conteudo)

def enfilera_pedido_msg_com_json(canal, fila, usuario, repositorio, status, tipo, resultado):
    msg1 = f'Conectando ao canal {canal} na fila {fila}'
    msg2 = f'Enviando o pedido de {tipo} do repositório {repositorio} do usuário {usuario}'
    print(msg1)
    print(msg2)
    logging.info(msg1) 
    logging.info(msg2)
    conteudo = 'user=' + usuario + '#' + 'repository=' + repositorio + '#' + 'status=' + status + '#' + 'resultado=' + resultado
    canal.basic_publish(exchange='', routing_key=fila, body=conteudo)

def enfilera_pedido_msg_com_json_metrica(canal, fila, usuario, repositorio, status, tipo, metrica, resultado):
    msg1 = f'Conectando ao canal {canal} na fila {fila}'
    msg2 = f'Enviando o pedido de {tipo} do repositório {repositorio} do usuário {usuario}, metríca: {metrica}'
    print(msg1)
    print(msg2)
    logging.info(msg1) 
    logging.info(msg2)
    conteudo = 'user=' + usuario + '#' + 'repository=' + repositorio + '#' + 'status=' + status + '#' + 'metrica=' + metrica + '#' + 'resultado=' + resultado
    canal.basic_publish(exchange='', routing_key=fila, body=conteudo)

def pega_nome_repositorio(url):
    lista = []
    try: 
        temp = url.split('/')
        nome_com_extensao = ''
        for each in temp:
            if '.git' in each:
                nome_com_extensao = each
        lista = nome_com_extensao.split('.')
    except Exception as e:
        print(f'Error parser body - {e}')
        logging.error("Exception occurred", exc_info=True)
    return lista[0]

def craete_dict_commits(nome_repositorio, all_commits):
    dict_commits = {}

    hash = []
    msg = []
    author_name = []
    author_email = []
    committer_name = []
    committer_email = []
    author_date = []
    author_timezone = []
    committer_date = []
    committer_timezone = []
    branches = []
    in_main_branch = []
    merge = []
    modified_files_commit = []
    parents = []
    project_name = []
    project_path = []
    deletions = []
    insertions = []
    lines = []
    files = []
    dmm_unit_size = []
    dmm_unit_complexity = []
    dmm_unit_interfacing = []
    
    try:
        for commit in all_commits:
            hash.append(commit.hash)
            msg.append(commit.msg)
            author_name.append(commit.author.name)
            author_email.append(commit.author.email)
            committer_name.append(commit.committer.name)
            committer_email.append(commit.committer.email)
            author_date.append(commit.author_date)
            author_timezone.append(commit.author_timezone)
            committer_date.append(commit.committer_date)
            committer_timezone.append(commit.committer_timezone)
            branches.append(commit.branches)
            in_main_branch.append(commit.in_main_branch)
            merge.append(commit.merge)
            modified_files = []
            for each in commit.modified_files:
                modified_files.append(each.filename)
            modified_files_commit.append(modified_files)
            parents.append(commit.parents)
            project_name.append(commit.project_name)
            project_path.append(commit.project_path)
            deletions.append(commit.deletions)
            insertions.append(commit.insertions)
            lines.append(commit.lines)
            files.append(commit.files)
            dmm_unit_size.append(commit.dmm_unit_size)
            dmm_unit_complexity.append(commit.dmm_unit_complexity)
            dmm_unit_interfacing.append(commit.dmm_unit_interfacing)

        dict_commits['hash'] = hash
        dict_commits['msg'] = msg
        dict_commits['author_name'] = author_name
        dict_commits['author_email'] = author_email
        dict_commits['committer_name'] = committer_name
        dict_commits['committer_email'] = committer_email
        dict_commits['author_date'] = author_date
        dict_commits['author_timezone'] = author_timezone
        dict_commits['committer_date'] = committer_date
        dict_commits['committer_timezone'] = committer_timezone
        dict_commits['branches'] = branches
        dict_commits['in_main_branch'] = in_main_branch
        dict_commits['merge'] = merge
        dict_commits['modified_files_commit'] = modified_files_commit
        dict_commits['parents'] = parents
        dict_commits['project_name'] = project_name
        dict_commits['project_path'] = project_path
        dict_commits['deletions'] = deletions
        dict_commits['insertions'] = insertions
        dict_commits['lines'] = lines
        dict_commits['files'] = files
        dict_commits['dmm_unit_size'] = dmm_unit_size
        dict_commits['dmm_unit_complexity'] = dmm_unit_complexity
        dict_commits['dmm_unit_interfacing'] = dmm_unit_interfacing
        print(f'Dicionario de commits do {nome_repositorio} gerado com sucesso!')
    except Exception as ex:
        print(f'Erro create_dict_commits: {str(ex)}')
    return dict_commits

# 1. Lista todos os commits (hash, data_commit, msg_commit, commiter) do repositório
    ## Gerar o dataframe
def get_dataframe_from_all_commits(dict_commits):    
    try:
        df = pd.DataFrame(data=dict_commits)    
        print(f'dataframe dos commits gerado com sucesso!')
    except Exception as ex:
        print(f'Erro get_dataframe_from_all_commits: {str(ex)}')
    return df

## Exportar dados da análise para arquivo .csv
def create_csv_from_df(path, nome_repositorio, nome_df, df):    
    try:
        filename = nome_repositorio + '_' + nome_df + '.csv'
        df.to_csv(path + '/' + filename)
        print(f'Arquivo {filename} gerado com sucesso!')
    except Exception as ex:
        print(f'Erro create_csv_from_df: {str(ex)}')
    return filename

## Exportar dados da análise para arquivo .csv
def create_csv_from_all_commits(path, nome_repositorio, df):    
    try:
        filename = nome_repositorio + '_' + 'all_commits' + '.csv'
        df.to_csv(path + '/' + filename)
        print(f'Arquivo {filename} gerado com sucesso!')
    except Exception as ex:
        print(f'Erro create_csv_from_all_commits: {str(ex)}')
    return filename

def create_dict_from_all_modified_files_from_all_commits(all_commits):
    dict_all_modified_files = {}
    hash_commit = []
    filename = []
    old_path = []
    new_path = []
    change_type = []
    diff = []
    diff_parsed = []
    added_lines = []
    deleted_lines = []
    source_code = []
    source_code_before = []
    methods = []
    methods_before = []
    changed_methods = []
    nloc = []
    complexity = []
    token_count = []

    for commit in all_commits:
        for m in commit.modified_files:
            hash_commit.append(commit.hash)
            filename.append(m.filename)
            old_path.append(m.old_path)
            new_path.append(m.new_path)
            change_type.append(m.change_type)
            diff.append(m.diff)
            diff_parsed.append(m.diff_parsed)
            added_lines.append(m.added_lines)
            deleted_lines.append(m.deleted_lines)
            source_code.append(m.source_code)
            source_code_before.append(m.source_code_before)
            methods.append(m.methods)
            methods_before.append(m.methods_before)
            changed_methods.append(m.changed_methods)
            nloc.append(m.nloc)
            complexity.append(m.complexity)
            token_count.append(m.token_count)

    dict_all_modified_files['hash_commit'] = hash_commit
    dict_all_modified_files['filename'] = filename
    dict_all_modified_files['old_path'] = old_path
    dict_all_modified_files['new_path'] = new_path
    dict_all_modified_files['change_type'] = change_type
    dict_all_modified_files['diff'] = diff
    dict_all_modified_files['diff_parsed'] = diff_parsed
    dict_all_modified_files['added_lines'] = added_lines
    dict_all_modified_files['deleted_lines'] = deleted_lines
    dict_all_modified_files['source_code'] = source_code
    dict_all_modified_files['source_code_before'] = source_code_before
    dict_all_modified_files['methods'] = methods
    dict_all_modified_files['methods_before'] = methods_before
    dict_all_modified_files['changed_methods'] = changed_methods
    dict_all_modified_files['nloc'] = nloc
    dict_all_modified_files['complexity'] = complexity
    dict_all_modified_files['token_count'] = token_count
    return dict_all_modified_files

def get_dataframe_from_all_modified_files(dict_all_modified_files):    
    try:
        df = pd.DataFrame(data=dict_all_modified_files)    
        print(f'dataframe dos arquivos modificados gerado com sucesso!')
    except Exception as ex:
        print(f'Erro get_dataframe_from_all_modified_files: {str(ex)}')
    return df

## Exportar dados da análise para arquivo .csv
def create_csv_from_all_modified_files(path, nome_repositorio, df):    
    try:
        filename = nome_repositorio + '_' + 'all_modified_files' + '.csv'
        df.to_csv(path + '/'+ filename)
        print(f'Arquivo {filename} gerado com sucesso!')
    except Exception as ex:
        print(f'Erro create_csv_from_all_modified_files: {str(ex)}')
    return filename

def create_dict_files_frequency(files_frequency):
    dict_files_frequency = {}
    file = []
    frequency_in_commits = []
    for k,v in files_frequency.items():
        file.append(k)
        frequency_in_commits.append(v)
    dict_files_frequency['file'] = file
    dict_files_frequency['frequency_in_commits'] = frequency_in_commits
    return dict_files_frequency

def create_dict_files_lines_changes(files_lines_changes):
    dict_files_lines_changes = {}
    file = []
    list_files_lines_changes = []
    for k,v in files_lines_changes.items():
        file.append(k)
        list_files_lines_changes.append(v)
    dict_files_lines_changes['file'] = file
    dict_files_lines_changes['files_lines_changes'] = list_files_lines_changes
    return dict_files_lines_changes

def create_dict_files_cc(files_cc):
    dict_files_cc = {}
    file = []
    list_files_cc = []
    for k,v  in files_cc.items():
        file.append(k)
        list_files_cc.append(v)
    dict_files_cc['file'] = file
    dict_files_cc['files_cc'] = list_files_cc
    return dict_files_cc

def get_dataframe_from_files_metric(dict_files_metric):    
    try:
        df = pd.DataFrame(data=dict_files_metric)    
        print(f'dataframe dos dict_files gerado com sucesso!')
    except Exception as ex:
        print(f'Erro get_dataframe_from_files_metric: {str(ex)}')
    return df

def create_csv_from_files_metric(path, nome_repositorio, df, metric):    
    try:
        filename = nome_repositorio + '_' + metric + '.csv'
        df.to_csv(path + '/' + filename)
        print(f'Arquivo {filename} gerado com sucesso!')
    except Exception as ex:
        print(f'Erro create_csv_from_files_metric: {str(ex)}')
    return filename