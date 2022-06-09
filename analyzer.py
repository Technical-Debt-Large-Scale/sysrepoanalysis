import logging
import os
import json
from enum import Enum
from pathlib import Path
from pydriller import Repository
from subprocess import check_output

# Define Type Directory or File
class Type(Enum):
  DIR = 0
  FILE = 1

# Define The code metric to be used
class HeatmapMetric(Enum):
  FREQUENCY = 0
  COMPLEXITY = 1
  LOC_CHANGES = 2
  COMPOSITION = 3

# Define the Tree Node 
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

# Define the structure of node in json
def create_json_object(node):
  return {
    "name": node.name,
    "type": node.node_type.name,
    "weight": node.loc,
    "depth": node.depth,
    "heatmap": node.heatmap,
    "children": []
  }

# For each node traverse the tree
def traverse(node):
  children = []
  for child in node.children:
    node = create_json_object(child)
    children.append(node)
    node["children"] = traverse(child)
  return children

# Create the final json file
def create_json(root):
  print('Criando o arquivo JSON...')
  json_output = create_json_object(root)
  json_output["children"] = traverse(root)

  with open(f'{root.name}.json', 'w') as outfile:
    outfile.write(json.dumps(json_output))

  print(f"Analysis completed. Available in: {root.name}.json")

# Define the rule to ignore files in repository
def should_ignore(name):
  list_of_files_and_directories_to_ignore = ['.git']
  return True in [i in name for i in list_of_files_and_directories_to_ignore]

# Method to count lines from file using os call
def count_lines_of_code_of_files(name):
    try:
        os.system(f"find {name} | xargs wc -l > locfiles.txt")
        with open("locfiles.txt", "r") as locfiles:
            return locfiles.readlines()[:-1]
    except Exception as e:
        print(f'Erro no count_lines_of_code_files: {str(e)}')

# Get the list of 100 last commits in repository
def get_list_of_commits(name):
  limit = 100
  commits = []
  for commit in Repository(name, order='reverse').traverse_commits():
    if limit == 0:
      break
    commits.append(commit)
    limit -= 1
  print('Os 100 commits foram recurepados com sucesso!')
  return commits

# For each file, calculate file frequency in commits
def get_files_frequency_in_commits(name):
  file_frequency = {}
  for commit in get_list_of_commits(name):
    for modified_file in commit.modified_files:
      if modified_file.filename in file_frequency.keys():
        file_frequency[modified_file.filename] += 1
      else:
        file_frequency[modified_file.filename] = 1
  return file_frequency

# For each file, calculate the modifed LOCs 
def get_number_of_lines_of_code_changes_in_commits(name):
  number_of_line_changes = {}
  for commit in get_list_of_commits(name):
    for modified_file in commit.modified_files:
      if modified_file.filename in number_of_line_changes.keys():
        number_of_line_changes[modified_file.filename] += modified_file.added_lines + modified_file.deleted_lines
      else:
        number_of_line_changes[modified_file.filename] = modified_file.added_lines + modified_file.deleted_lines
  return number_of_line_changes

# For each file, calculate the cyclomatic complexity 
def get_files_cyclomatic_complexity_in_commits(name):
  print(f'Pegando a complexidade ciclomática de {name}')
  complexity = {}
  for commit in get_list_of_commits(name):
    for modified_file in commit.modified_files:
      complexity[modified_file.filename] = 0 if modified_file.complexity is None else modified_file.complexity
  print(f'{name} Passou pelo get cc com sucesso!')
  return complexity

# Calculate the factor: (modified LOC) x (file frequency in commits) x (cyclomatic complexity)
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

# Calculate the LOC of root node that accumulated all LOC children
def calculate_loc_tree(node):
  loc = 0
  for each in node.children:
    loc += each.loc + calculate_loc_tree(each)
  if len(node.children) > 0:
    node.loc = loc
  if node.parent is not None:
    return loc

# Create the tree of directories and files
def create_tree(name, list_of_files_and_directories, list_locs_of_files, dict_of_heatmap_metric, to_remove):
  print(f'Entrou no create_tree...')
  to_remove = name
  print(f'to remove: {to_remove}')
  root = Node(name=name,loc=0, heatmap=1, node_type=Type.DIR, depth=0, children=[])

  nodes = [root]
  print(f'Lista de arquivos e diretorios de {name} : {list_of_files_and_directories}')
  list_of_files_and_directories2 = []
  for each in list_of_files_and_directories: 
    each = each.replace(to_remove, '')
    list_of_files_and_directories2.append(each)
  
  print(list_of_files_and_directories2)

  print(f'Lista de locs_of_files name: {list_locs_of_files}')
  list_locs_of_files2 = [] 
  for each in list_locs_of_files:
    each = each.replace(to_remove, '')
    list_locs_of_files2.append(each)
  print(list_locs_of_files2)

  for key in list_of_files_and_directories2:
    last_name = key.split('/')[-1]
    depth = key.count('/')
    loc = 0
    heatmap = 0

    if os.path.isdir(key):
      key_type = Type.DIR
      heatmap = 0
    else:
      key_type = Type.FILE
      if key in list_locs_of_files2:
        loc = list_locs_of_files2[key]
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

#Calculate the LOC list of files
def get_list_of_files_loc(name):
    print(f'Pega a lista de arquivos com seus LOCs do repositorio {name}')
    list_locs_of_files = {}
    try:
        for each in count_lines_of_code_of_files(name):
            if not should_ignore(each):
                elements = each.split(' ') 
                if(elements[-1] != "" and elements[-2] != ""):
                    list_locs_of_files[elements[-1].replace('\n', '')] = int(elements[-2])
    except Exception as e:
        print(f'entrou no get_list_of_files_loc mas deu erro: {str(e)}')
    return list_locs_of_files

# Get the files and directories from repository
def get_list_of_files_and_directories(name):
  print(f'Pega a lista de arquivos e diretorios do {name}')
  try:
    list_of_files_and_directories = check_output(f"cd {name} && tree -i -f", shell=True).decode("utf-8").splitlines()
  except Exception as e:
    print(f'Erro no get_list_of_files_and_directories: {str(e)}')
  return [each.replace('./', name + '/') for each in list_of_files_and_directories][1:-2]

# Main method do analyze repository commits
# name - path_to_repo
def analize_repository(name, heatmap_metric, name_repository, to_remove):
    print("Analyzing...")
    print(f'name: {name}')
    print(f'heatmap: {heatmap_metric}')
    dict_of_heatmap_metric = {}

    try:
        if heatmap_metric == HeatmapMetric.FREQUENCY:
            dict_of_heatmap_metric = get_files_frequency_in_commits(name)
        elif heatmap_metric == 'COMPLEXITY':
            print('Pega as CC dos arquivos do repositorio {name}')
            dict_of_heatmap_metric = get_files_cyclomatic_complexity_in_commits(name)
        elif heatmap_metric == HeatmapMetric.LOC_CHANGES:
            dict_of_heatmap_metric = get_number_of_lines_of_code_changes_in_commits(name)
        elif heatmap_metric == HeatmapMetric.COMPOSITION:
            dict_of_heatmap_metric = get_composition(name)
        else:
            raise IndexError
        root = create_tree(name_repository, get_list_of_files_and_directories(name), get_list_of_files_loc(name), dict_of_heatmap_metric, to_remove)
        create_json(root)
    except Exception as e:
        print(f'Erro no analize_repository: {str(e)}')

# Prepare the environment to run the analysis
#def initialize():
#  url = os.environ['REPOSITORY_URL']
#  name = url.split('/')[-1]
#  heatmap_metric = os.environ['HEATMAP_METRIC']
#  return url, name, heatmap_metric

# Cloning repository in local directory using OS calls
# def clone_repository(url, name, heatmap_metric):
#  try:
#    print("Cloning repository...")
#    os.system(f"git clone {url}")
#    analize_repository(name, heatmap_metric)
#  except IndexError:
#    print("Heatmap metric is out of range")
#  
#  finally:
#    os.system(f"rm -r {name}")
#    os.system(f"rm -r locfiles.txt")
  
# Execute the analysis of commit from repository
#def run():
#  try:
#    url, name, heatmap_metric = initialize()
#    try:
#      heatmap_metric = HeatmapMetric[heatmap_metric.upper()]
#      clone_repository(url, name, heatmap_metric)
#    except KeyError as e:
#      print(f"Heatmap metric is out of range: {e}")
#  except KeyError as e:
#    print(f"Environmental variable was not properly assigned: {e}")

#if __name__ == "__main__":
#  run()

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
