from pydriller import Repository
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from git import Repo
from subprocess import check_output
import os

def clona_repositorio(url_repositorio, local_salva_repositorio):
  try:
    Repo.clone_from(url_repositorio, local_salva_repositorio)
  except Exception as ex:
    print(f'Erro: {str(ex)}')

def temp_user_directory(user_id, tipo):
    user_path = './' + str(user_id) + '/' + tipo

    if os.path.exists(user_path):
        return user_path
    else: 
        os.makedirs(user_path)
        return user_path   

def get_list_of_files_and_directories_updated(user_id, nome_repositorio, tipo):
  path_user = temp_user_directory(user_id, tipo)
  path_repositorio = path_user + '/' + nome_repositorio
  list_of_files_and_directories = check_output(f"cd {path_repositorio} && tree -i -f", shell=True).decode("utf-8").splitlines()
  print(f'list_of_files_and_directories: {list_of_files_and_directories}')
  temp = f'{nome_repositorio}/'
  result = [each.replace('./', temp) for each in list_of_files_and_directories]
  print(f'get_list_of_files_and_directories_updated: {result}')
  return result

def get_list_of_files_and_directories_src(user_id, nome_repositorio, folder_src='src', folder_java='src/main/java/', tipo='sp'):
  # Escolhe o diretorio do source java
  # Lista apenas arquivos e diretorios do src/main/java
  result = []
  for item in get_list_of_files_and_directories_updated(user_id, nome_repositorio, tipo):
    if folder_src in item:
      if folder_java in item:
        result.append(item)
  print(f'get_list_of_files_and_directories_src: {result}')
  return result

def get_list_locs_of_files(user_id, nome_repositorio, tipo):
  path_user = temp_user_directory(user_id, tipo)
  path_repositorio = path_user + '/' + nome_repositorio
  # Cria um arquivo contendo a quantidade de LOC por arquivo
  os.system(f"find {path_repositorio} -name *.java | xargs wc -l > {path_repositorio}/locarquivosjava.txt")
  # !find {repositorio} -name *.java | xargs wc -l > locarquivosjava.txt
  list_locs_of_files = check_output(f"cat {path_repositorio}/locarquivosjava.txt", shell=True).decode("utf-8").splitlines()
  # Cria uma lista com elementos que representam o LOC e o arquivo
  # (Loc, arquivo)
  result = []
  for each in list_locs_of_files:
    elementos = each.split(' ') 
    item = elementos[-2], elementos[-1]
    result.append(item)
  print(f'get_list_locs_of_files: {result}')
  return result

def get_dict_java_frequency_commits(dict_frequency_files_commits):
  dict_java_frequency_commits = {}
  for file, frequency in dict_frequency_files_commits.items():
    if '.java' in file:
      dict_java_frequency_commits[file] = frequency
  return dict_java_frequency_commits

def get_dict_java_lines_modified(dict_lines_modified_in_files):
  dict_java_lines_modified = {}
  for file, lines_modified in dict_lines_modified_in_files.items():
    if '.java' in file:
      dict_java_lines_modified[file] = lines_modified
  return dict_java_lines_modified

def convert_dict_java_frequency_to_dataframe(dict_java_frequency_commits):
  # Converte o dicionário dict_java_frequency_commits em um dataframe
  df_java_frequency_commits = pd.DataFrame(dict_java_frequency_commits.items(), columns=['File', 'Frequency'])
  return df_java_frequency_commits

def convert_dict_java_lines_modified_to_dataframe(dict_java_lines_modified):
  # Converte o dicionário dict_java_lines_modified em um dataframe
  df_java_lines_modified = pd.DataFrame(dict_java_lines_modified.items(), columns=['File', 'lines_modified'])
  return df_java_lines_modified

def merge_dataframes_java_frequency(df_java_frequency_commits, df_java_lines_modified):
  # Faz o merge das informações para criar um dataframe contendo o arquivo, 
  # a frequência de Commits e Linhas Modificadas de cada arquivo ao longo do tempo
  df = df_java_frequency_commits[['File', 'Frequency']]
  df['lines_modified'] = df_java_lines_modified['lines_modified']
  return df

def generate_sccater_plot(df_fc_ml, repositorio=None, path_to_save=None):
  plt.style.use('ggplot')
  plt.figure(figsize=(12,8))
  sns.scatterplot(data=df_fc_ml, x='lines_modified', y='Frequency')

  titulo_temp = f'{repositorio} - LoCs Modifications x Files Occurrence in Commits'
  abbr={'titulo':titulo_temp, 'lines_modified':'LoCs Modifications', 'Frequency':'Files Occurrence in Commits'}

  plt.title(f"Analysis of {repositorio} Repository : {abbr['lines_modified']} x {abbr['Frequency']}")
  plt.xlabel(abbr['lines_modified'])
  plt.ylabel(abbr['Frequency'])
          
  for i in range(df_fc_ml.shape[0]): 
    plt.text(df_fc_ml.lines_modified[i], y=df_fc_ml.Frequency[i], s=df_fc_ml.File[i], alpha=0.8, fontsize=8)

  #plt.show()
  file_to_save = 'scatter_plot' + '.png'
  if repositorio is not None and path_to_save is not None:
    file_to_save = path_to_save + '/' + repositorio + '.png'

  plt.savefig(file_to_save)

def generate_sccater_plot_2(df_fc_ml, repositorio=None):
  # array de complexidade ciclomatica
  array_cc = np.random.randint(1, 300, size=300)
  # Add traces
  fig = go.Figure(data=go.Scatter(
                      x=df_fc_ml.lines_modified, 
                      y=df_fc_ml.Frequency,
                      mode='markers',
                      name='markers',
                      customdata=df_fc_ml.File,
                      hovertext=df_fc_ml.File, 
                      marker=dict(size=8, color=array_cc, colorscale='Blues', showscale=True, colorbar={"title": 'CC'})
                      )
                    )
  
  titulo_temp = f'{repositorio} - LoCs Modifications x Files Occurrence in Commits'

  fig.update_layout({"title_text": titulo_temp},     
                    width=1000,
                    height=600
                    )
  fig.update_xaxes(
          title_text = "LoC Modifications",
          title_font = {"size": 10}
          )
  fig.update_yaxes(
          title_text = "Commit Frequency",
          title_font = {"size": 10}
          )

  fig.show()

def generate_box_plot_frequency(df_fc_ml, repositorio=None, path_to_save=None):
  s_boxplot_fc = df_fc_ml['Frequency']
  df_boxplot_fc = s_boxplot_fc.to_frame(name='Frequency')
  df_boxplot_fc['File'] = 'File'
  plt.figure(figsize=(6,4))
  sns.boxplot(x='File', y='Frequency', data=df_boxplot_fc)
  file_to_save = 'box_plot_frequency' + '.png'
  if repositorio is not None and path_to_save is not None: 
    file_to_save = path_to_save + '/' + 'box_plot_frequency' + '_' + repositorio + '.png'

  plt.savefig(file_to_save)
  return df_boxplot_fc

def get_quartiles_frequency(df_boxplot_fc):
  fc_q1 = np.percentile(df_boxplot_fc.Frequency , [25])
  fc_q2 = np.percentile(df_boxplot_fc.Frequency , [50])
  fc_q3 = np.percentile(df_boxplot_fc.Frequency , [75])
  fc_q4 = np.percentile(df_boxplot_fc.Frequency , [100])
  return fc_q1, fc_q2, fc_q3, fc_q4

def generate_box_plot_lines_modified(df_fc_ml, repositorio=None, path_to_save=None):
  s_boxplot_lm = df_fc_ml['lines_modified']
  df_boxplot_lm = s_boxplot_lm.to_frame(name='lines_modified')
  df_boxplot_lm['File'] = 'File'
  df_boxplot_lm
  plt.figure(figsize=(6,4))
  # Constroi o Boxsplot excluindo arquivos que apareceram em menos de 10 commits
  sns.boxplot(x='File', y='lines_modified', data=df_boxplot_lm)
  file_to_save = 'box_plot_lines_modified' + '.png'
  if repositorio is not None and path_to_save is not None: 
    file_to_save = path_to_save + '/' + 'box_plot_lines_modified' + '_' + repositorio + '.png'
  plt.savefig(file_to_save)
  return df_boxplot_lm

def get_quartiles_lines_modified(df_boxplot_lm):
  lm_q1 = np.percentile(df_boxplot_lm.lines_modified , [25])
  lm_q2 = np.percentile(df_boxplot_lm.lines_modified , [50])
  lm_q3 = np.percentile(df_boxplot_lm.lines_modified , [75])
  lm_q4 = np.percentile(df_boxplot_lm.lines_modified , [100])
  return lm_q1, lm_q2, lm_q3, lm_q4