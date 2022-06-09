from pydriller import Repository, Git
from git import Repo, GitCommandError

def list_all_commits(path_repository):
  """
  List all commits in the repository
  @param: str path_repository: repositorio que sera analisado
  @return a list of pydryiller commits
  """
  commits = []
  for commit in Repository(path_repository).traverse_commits():
      commits.append(commit)
  return commits

def list_single_commit(path_repository, commit_hash):
  """
  List a single commit 
  @param: str commit_hash: a hash of commit
  @return a pydryiller commit
  """
  commit = Repository(path_repository, single=commit_hash).traverse_commits()
  return next(commit)

def list_all_modified_files_in_commits(path_repository):
  """
  List all modified files in all commits in the repository
  @return a dictionary where the each key contains the hash of a commit 
  and the value associated contains a list of pydriller modified_file
  of this commit
  """
  modified_files = {}
  for commit in list_all_commits(path_repository):
      modified_files[commit.hash] = commit.modified_files
  return modified_files

def list_all_modified_files_in_single_commit(path_repository, commit_hash):
  """
  List all modified files in a specific commit
  @param: str commit_hash: a hash of commit
  @return a list of pydriller modified_file
  """
  commit = list_single_commit(path_repository,commit_hash)
  return commit.modified_files

def list_all_authors_in_repository(path_repository):
  """
  List all authors who have made at least one commit in the repository
  @return a list of pydriller developer
  """
  authors = []
  for commit in list_all_commits(path_repository):
      if commit.author not in authors:
          authors.append(commit.author)
  return authors

def list_all_tags(path_repository):
  """
  List all tags in the repositpory
  @return a list of strings (tags names)
  """
  repository = Repo(path_repository)
  return repository.tags

def list_all_modified_files_in_tags(path_repository):
  """
  List all modified files in all tags in the repository
  @return a dictionary where the each key contains the tag name
  and the value associated contains a list of pydriller modified_file
  of this commit
  """
  modified_files_in_tags = {}
  for tag in list_all_tags(path_repository):
      modified_files_in_tags[tag.name] = Git(path_repository).get_commit_from_tag(tag.name).modified_files
  return modified_files_in_tags

def list_modified_files_in_tag(path_repository, tag_name):
  """
  List all modified files in a specific tag in the repository
  @return a list of modified files in the tag name
  of this commit
  """
  modified_files_in_tag = Git(path_repository).get_commit_from_tag(tag_name).modified_files
  return modified_files_in_tag

def list_all_commits_between_tags(path_repository, initial_tag, final_tag):
  """
  List all commits starting at initial_tag and ending at final_tag
  @param: str initial_tag: a tag name
  @param: str final_tag: a tag name
  @return a list of pydriller commit
  """
  commits = []
  for commit in Repository(path_to_repo=path_repository, from_tag=initial_tag, to_tag=final_tag).traverse_commits():
      commits.append(commit)
  return commits

def get_files_frequency_in_commits(path_repository, from_commit=None, to_commit=None):
  """
  List how often each file appears in commits 
  @param: str from_commit: a hash of commit
  @param: str to_commit: a hash of commit
  @return a dictionary where the each key contains the filename
  and the value associated contains the frequency
  """
  commits = Repository(path_to_repo=path_repository, from_commit=from_commit, to_commit=to_commit).traverse_commits()

  file_frequency = {}
  for commit in commits:
      for modified_file in commit.modified_files:
          if modified_file.filename in file_frequency.keys(): # save full object
              file_frequency[modified_file.filename] += 1
          else:
              file_frequency[modified_file.filename] = 1
  return file_frequency

def get_number_of_lines_of_code_changes_in_commits(path_repository, from_commit=None, to_commit=None):
  """
  List amount of code line changes of each file 
  @param: str from_commit: a hash of commit
  @param: str to_commit: a hash of commit
  @return a dictionary where the each key contains the filename
  and the value associated contains the number of lines of code changes
  """

  commits = Repository(path_to_repo=path_repository, from_commit=from_commit, to_commit=to_commit).traverse_commits()

  number_of_line_changes = {}
  for commit in commits:
      for modified_file in commit.modified_files:
          if modified_file.filename in number_of_line_changes.keys(): # save full object
              number_of_line_changes[modified_file.filename] += modified_file.added_lines + modified_file.deleted_lines
          else:
              number_of_line_changes[modified_file.filename] = modified_file.added_lines + modified_file.deleted_lines
  return number_of_line_changes

def get_files_cyclomatic_complexity_in_commits(path_repository, from_commit=None, to_commit=None):
  """
  List cyclomatic complexity of each file 
  @param: str from_commit: a hash of commit
  @param: str to_commit: a hash of commit
  @return a dictionary where the each key contains the filename
  and the value associated contains the cyclomatic complexity
  """
  commits = Repository(path_to_repo=path_repository, from_commit=from_commit, to_commit=to_commit).traverse_commits()

  complexity = {}
  for commit in commits:
      for modified_file in commit.modified_files:
          if modified_file.complexity is not None:
            complexity[modified_file.filename] = modified_file.complexity
          else:
            complexity[modified_file.filename] = 0
  return complexity

# Funcoes especificas para capturar apenas arquivos .java

def list_java_modified_files_in_commits(path_repository):
  """
  List java modified files in all commits in the repository
  @return a dictionary where the each key contains the hash of a commit 
  and the value associated contains a list of pydriller modified_file
  of this commit
  """
  java_modified_files = {}
  list_java_files = []
  for commit in list_all_commits(path_repository):
    list_java_files = [f for f in commit.modified_files if ('.java' in f.filename)]
    java_modified_files[commit.hash] = list_java_files
    list_java_files = []
  return java_modified_files

def list_java_modified_files_in_single_commit(path_repository, commit_hash):
  """
  List java modified files in a specific commit
  @param: str commit_hash: a hash of commit
  @return a list of pydriller java modified_file
  """
  commit = list_single_commit(path_repository, commit_hash)
  list_java_files = [f for f in commit.modified_files if ('.java' in f.filename)]
  return list_java_files

def list_java_modified_files_in_tags(path_repository):
  """
  List java modified files in all tags in the repository
  @return a dictionary where the each key contains the tag name
  and the value associated contains a list of pydriller java modified_file
  of this commit
  """
  modified_files_in_tags = {}
  list_java_files = []
  list_temp = []
  for tag in list_all_tags(path_repository):
    list_temp = Git(path_repository).get_commit_from_tag(tag.name).modified_files
    list_java_files = [f for f in list_temp if ('.java' in f.filename)]
    modified_files_in_tags[tag.name] = list_java_files
    list_java_files = []
  return modified_files_in_tags

def get_java_files_frequency_in_commits(path_repository, from_commit=None, to_commit=None):
  """
  List how often each java file appears in commits 
  @param: str from_commit: a hash of commit
  @param: str to_commit: a hash of commit
  @return a dictionary where the each key contains the java filename
  and the value associated contains the frequency
  """
  commits = Repository(path_to_repo=path_repository, from_commit=from_commit, to_commit=to_commit).traverse_commits()

  file_frequency = {}
  for commit in commits:
      for modified_file in commit.modified_files:
        if '.java' in modified_file.filename:
          if modified_file.filename in file_frequency.keys(): # save full object
              file_frequency[modified_file.filename] += 1
          else:
              file_frequency[modified_file.filename] = 1
  return file_frequency

def get_java_number_of_lines_of_code_changes_in_commits(path_repository, from_commit=None, to_commit=None):
  """
  List amount of code line changes of each java file 
  @param: str from_commit: a hash of commit
  @param: str to_commit: a hash of commit
  @return a dictionary where the each key contains the java filename
  and the value associated contains the number of lines of code changes
  """

  commits = Repository(path_to_repo=path_repository, from_commit=from_commit, to_commit=to_commit).traverse_commits()

  number_of_line_changes = {}
  for commit in commits:
      for modified_file in commit.modified_files:
        if '.java' in modified_file.filename:
          if modified_file.filename in number_of_line_changes.keys(): # save full object
              number_of_line_changes[modified_file.filename] += modified_file.added_lines + modified_file.deleted_lines
          else:
              number_of_line_changes[modified_file.filename] = modified_file.added_lines + modified_file.deleted_lines
  return number_of_line_changes

def get_java_files_cyclomatic_complexity_in_commits(path_repository, from_commit=None, to_commit=None):
  """
  List cyclomatic complexity of each java file 
  @param: str from_commit: a hash of commit
  @param: str to_commit: a hash of commit
  @return a dictionary where the each key contains the java filename
  and the value associated contains the cyclomatic complexity
  """
  commits = Repository(path_to_repo=path_repository, from_commit=from_commit, to_commit=to_commit).traverse_commits()

  complexity = {}
  for commit in commits:
      for modified_file in commit.modified_files:
        if '.java' in modified_file.filename:
          if modified_file.complexity is not None:
            complexity[modified_file.filename] = modified_file.complexity
          else:
            complexity[modified_file.filename] = 0
  return complexity