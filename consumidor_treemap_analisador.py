import os
import pika
import json
import logging
from enum import Enum
import msr.utils as util
from pydriller import Repository
from subprocess import check_output
import shutil

rabbitmq_broker_host = 'localhost'
my_fila1 = 'fila_analisador'
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_broker_host, heartbeat=0))

channel_to_analysis = connection.channel() 
channel_to_analysis.queue_declare(queue=my_fila1, durable=True)

class Type(Enum):
  DIR = 0
  FILE = 1

class HeatmapMetric(Enum):
  FREQUENCY = 0
  COMPLEXITY = 1
  LOC_CHANGES = 2
  COMPOSITION = 3

class Node:
  def __init__(self, name, loc, heatmap, node_type, depth, children = []):
    self.name = name
    self.loc = loc
    self.node_type = node_type
    self.depth = depth
    self.children = children
    self.parent = None
    self.heatmap = heatmap
  
  def append_node(self, node):
    node.parent = self
    self.children.append(node)

def create_json_object(node):
  return {
    "name": node.name,
    "type": node.node_type.name,
    "weight": node.loc,
    "depth": node.depth,
    "heatmap": node.heatmap,
    "children": []
  }

def traverse(node):
  children = []
  for child in node.children:
    node = create_json_object(child)
    children.append(node)
    node["children"] = traverse(child)
  return children

def create_json(root, metrica, path_repositories, user_id, name):
  singleName = metrica
  #Create the user directory if not existe
  temp_path = user_directory(path_repositories, user_id, name)
  fileName =  temp_path + '/' + singleName
  msg1 = f'Saving the file {fileName}...' 
  print(msg1)
  logging.info(msg1)

  json_output = create_json_object(root)
  json_output["children"] = traverse(root)

  with open(f'{fileName}.json', 'w') as outfile:
    outfile.write(json.dumps(json_output))

  print(f"Analysis completed. Available in: {fileName}.json")

def should_ignore(name):
  list_of_files_and_directories_to_ignore = ['.git']
  return True in [i in name for i in list_of_files_and_directories_to_ignore]

def count_lines_of_code_of_files(name):
  os.system(f"find {name} | xargs wc -l > locfiles.txt")
  with open("locfiles.txt", "r") as locfiles:
    return locfiles.readlines()[:-1]

def get_list_of_commits(name, limit=100):
  commits = []
  for commit in Repository(name, order='reverse').traverse_commits():
    if limit == 0:
      break
    commits.append(commit)
    limit -= 1
  return commits

def get_files_frequency_in_commits(name):
  file_frequency = {}
  for commit in get_list_of_commits(name):
    for modified_file in commit.modified_files:
      if modified_file.filename in file_frequency.keys():
        file_frequency[modified_file.filename] += 1
      else:
        file_frequency[modified_file.filename] = 1
  return file_frequency

def get_number_of_lines_of_code_changes_in_commits(name):
  number_of_line_changes = {}
  for commit in get_list_of_commits(name):
    for modified_file in commit.modified_files:
      if modified_file.filename in number_of_line_changes.keys():
        number_of_line_changes[modified_file.filename] += modified_file.added_lines + modified_file.deleted_lines
      else:
        number_of_line_changes[modified_file.filename] = modified_file.added_lines + modified_file.deleted_lines
  return number_of_line_changes

def get_files_cyclomatic_complexity_in_commits(name):
  complexity = {}
  for commit in get_list_of_commits(name):
    for modified_file in commit.modified_files:
      complexity[modified_file.filename] = 0 if modified_file.complexity is None else modified_file.complexity
  return complexity

def get_composition(name):
  file_frequency = get_files_frequency_in_commits(name)
  number_of_line_changes = get_number_of_lines_of_code_changes_in_commits(name)
  complexity = get_files_cyclomatic_complexity_in_commits(name)
  composition = {}
  for key, value in file_frequency.items():
    fc = file_frequency[key]
    ml = number_of_line_changes[key]
    cc = complexity[key]
    composition[key] = fc*ml*cc
  return composition

def calculate_loc_tree(node):
  loc = 0
  for each in node.children:
    loc += each.loc + calculate_loc_tree(each)
  if len(node.children) > 0:
    node.loc = loc
  if node.parent is not None:
    return loc

def create_tree(name, list_of_files_and_directories, list_locs_of_files, dict_of_heatmap_metric):

  root = Node(name=name,loc=0, heatmap=1, node_type=Type.DIR, depth=0, children=[])

  nodes = [root]

  for key in list_of_files_and_directories:
    last_name = key.split('/')[-1]
    depth = key.count('/')
    loc = 0
    heatmap = 0

    if os.path.isdir(key):
      key_type = Type.DIR
      heatmap = 0
    else:
      key_type = Type.FILE
      if key in list_locs_of_files:
        loc = list_locs_of_files[key]
      if last_name in dict_of_heatmap_metric:
        heatmap = dict_of_heatmap_metric[last_name]

    if depth != len(nodes):
      diff = abs(depth - len(nodes))
      if depth < len(nodes):
        for i in range(0, diff):
          nodes.pop()
      else:
        nodes.append(node)

    node = Node(name=last_name, loc=loc, heatmap=heatmap, node_type=key_type, depth=depth, children=[])

    if len(nodes) > 0:
      nodes[len(nodes) - 1].append_node(node)

  calculate_loc_tree(root)
  return root

def get_list_of_files_loc(name):
    list_locs_of_files = {}

    for each in count_lines_of_code_of_files(name):
        if not should_ignore(each):
            elements = each.split(' ') 
            if(elements[-1] != "" and elements[-2] != ""):
                list_locs_of_files[elements[-1].replace('\n', '')] = int(elements[-2])
    return list_locs_of_files

def get_list_of_files_and_directories(name):
  list_of_files_and_directories = check_output(f"cd {name} && tree -i -f", shell=True).decode("utf-8").splitlines()
  return [each.replace('./', name + '/') for each in list_of_files_and_directories][1:-2]

def generate_root(name, metric):
    print(f"Analyzing {metric}...")
    dict_of_heatmap_metric = {}
    if metric == 'FREQUENCY':
        dict_of_heatmap_metric = get_files_frequency_in_commits(name)
    if metric == 'COMPLEXITY':
        dict_of_heatmap_metric = get_files_cyclomatic_complexity_in_commits(name)
    if metric == 'LOC_CHANGES':
        dict_of_heatmap_metric = get_number_of_lines_of_code_changes_in_commits(name)
    if metric == 'COMPOSITION':
        dict_of_heatmap_metric = get_composition(name)
    root = create_tree(name, get_list_of_files_and_directories(name), get_list_of_files_loc(name), dict_of_heatmap_metric)
    create_json(root, metric)

def analize_repository(name):
    generate_root(name, 'FREQUENCY')
    generate_root(name, 'COMPLEXITY')
    generate_root(name, 'LOC_CHANGES')
    generate_root(name, 'COMPOSITION')

def user_directory(path_repositories, user_id, name):
    user_path = path_repositories + '/' + str(user_id) + '/' + name
    if os.path.exists(user_path):
        return user_path
    else: 
        os.makedirs(user_path)
        return user_path 

def analisar_repositorio(user, repositorio, nome_repositorio, status):
    print(f'Analisando repositorio {nome_repositorio} from {repositorio}')
    # Frequency
    dict_of_heatmap_metric_frequency = get_files_frequency_in_commits(nome_repositorio)
    root_frequency = create_tree(nome_repositorio, get_list_of_files_and_directories(nome_repositorio), get_list_of_files_loc(nome_repositorio), dict_of_heatmap_metric_frequency)
    create_json(root_frequency, 'FREQUENCY', util.Constants.PATH_REPOSITORIES, user, nome_repositorio)

    # CC
    dict_of_heatmap_metric_cc =  get_files_cyclomatic_complexity_in_commits(nome_repositorio)
    root_cc = create_tree(nome_repositorio, get_list_of_files_and_directories(nome_repositorio), get_list_of_files_loc(nome_repositorio), dict_of_heatmap_metric_cc)
    create_json(root_cc, 'COMPLEXITY', util.Constants.PATH_REPOSITORIES, user, nome_repositorio)
    
    # MLOC
    dict_of_heatmap_metric_mloc =  get_number_of_lines_of_code_changes_in_commits(nome_repositorio)
    root_mloc = create_tree(nome_repositorio, get_list_of_files_and_directories(nome_repositorio), get_list_of_files_loc(nome_repositorio), dict_of_heatmap_metric_mloc)
    create_json(root_mloc, 'LOC_CHANGES', util.Constants.PATH_REPOSITORIES, user, nome_repositorio)

    # COMPOSITION
    dict_of_heatmap_metric_composition = get_composition(nome_repositorio)
    root_composition = create_tree(nome_repositorio, get_list_of_files_and_directories(nome_repositorio), get_list_of_files_loc(nome_repositorio), dict_of_heatmap_metric_composition)
    create_json(root_composition, 'COMPOSITION', util.Constants.PATH_REPOSITORIES, user, nome_repositorio)

def clone_repository(user, repositorio, nome_repositorio, status):
    try:
        # Remove o diretorio name caso ele exista
        if os.path.isdir(nome_repositorio): 
            shutil.rmtree(nome_repositorio)
        print(f"Cloning repository {nome_repositorio} from {repositorio} ...")
        os.system(f"git clone {repositorio}")
        print('Cloning finished!')
        #analize_repository(name)
        analisar_repositorio(user, repositorio, nome_repositorio, status)
    except OSError as e:
        print ("Error: %s - %s." % (e.filename, e.strerror))
    except IndexError:
        print("Heatmap metric is out of range")

def initialize(url):
    if '.git' in url:
        url = url.split('.git')[0]
    name = url.split('/')[-1]
    return url, name

def run(user, repositorio, status):
    try:
        url, name = initialize(repositorio)
        print(f'Inciando clonagem e analise de repositorio {name} baseado na {url}.')
        print('Aguarde...')
        clone_repository(user, url, name, status)
    except Exception as e:
        print(f"Erro na clonagem do repositorio: {e}")

def analise_callback(ch, method, properties, body): 
    body = body.decode('utf-8')
    if 'user' in body:
        try:
            user, repositorio, nome_repositorio, status = util.parser_body(body)
            #analisar_repositorio(user, repositorio, nome_repositorio, status)         
            run(user, repositorio, status)
            msg1 = f'Análise do repositório {nome_repositorio} from {repositorio} concluida!' 
            print(msg1)
            logging.info(msg1)
        except Exception as ex:
            print(f'Erro analise_callback: {str(ex)}')     

channel_to_analysis.basic_consume(my_fila1, analise_callback, auto_ack=True)

print(' [*] Waiting for messages to analysis queue to Treemap. To exit press CTRL+C') 
channel_to_analysis.start_consuming()