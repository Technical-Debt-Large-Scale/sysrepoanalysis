# Sysrepoanalysis

SysRepoAnalysis is an open-source, multi-user web tool that allows online analysis of git repositories by extracting historical information from source code files over time, using mining software repository techniques. Such data can be useful for the development team to find critical areas of the code repository that have a high maintenance effort over time. The main metrics used are cyclomatic complexity, accumulation of LOC modifications (based on code-churn), and frequency of occurrence of files in commits over time. In addition, we use the composition of these metrics to find very complex source code files that are frequently modified and have many LOCs changed over time. Besides,  to calculate these metrics, the tool allows the generation and display of a treemap of the repository's directory and file structure and the rendering of a heatmap based on the metric chosen to be analyzed. Such features can be useful in helping the development team to find critical source code files or areas that contain such files. In this way, it can help the development team to make decisions regarding the choice of candidate files for refactorings that can generate a great maintenance effort. Among the main features of SysRepoAnalysis, we can highlight: control of user authentication and authorization, cloning and asynchronous analysis of user repositories (via message broker using producers and consumers), historical analysis and export of modified commits and files, calculation and export of results of the analyzed metrics (cyclomatic complexity, accumulation of LOC modifications (based on code-churn) and frequency of occurrence of files in commits over time) and treemap generation of the repository's directory and file structure, as well as the rendering of heatmap based on the metric chosen to be analyzed. 

[Demo Video](https://youtu.be/AN36ICUpmRI)

[![License](https://img.shields.io/badge/License-BSD%202--Clause-orange.svg)](https://github.com/myplayareas/sysrepository/blob/master/LICENSE)

# Main modules

Server1 - Application Server (Flask Web App)

Server2 - Message broker (RabbitMQ)

## 1. Installing requirement (Server1)

On Server1, prepare the virtual environment to immediately run the main flask application.

Clone the repository
```bash
git clone https://github.com/Technical-Debt-Large-Scale/sysrepoanalysis.git
```

Go to folder sysrepoanalysis
```bash
cd sysrepoanalysis
```

Virtual environment
```bash
python3 -m venv venv
```

Activate virtual environment
```bash
source venv/bin/activate
```

Install requirements
```bash
pip3 install -r requirements.txt
```

## 2. repositoryanalysis (Server2)
Repository Analysis - Allows asynchronous analysis of multiple git repositories in the form of order fulfillment.

Given a git repository, it is saved in the database and soon after it is cloned to allow a local analysis. At the end of the repository analysis, it generates a JSON file with the analysis results.

For our example, Server2 will be a docker container hosted on Server1. With that, ensure you have docker installed and running on Server1.

### To run RabbitMQ with docker, just run the following command line:

No Server1 execute o seguinte comando: 
```
docker run --rm -p 5672:5672 -p 8080:15672 rabbitmq:3-management
```

On Server1, you can access the RabbitMQ web app via http://localhost:8080

When the Server1 application runs, the following queues will be created:

fila_repositorio_local - Queue that organizes requests to clone repositories

fila_status_banco - Queue that organizes status update requests from each repository in the database

fila_analyse_commits - Queue that organizes analysis requests from repositories

queue_operacoes_arquivo_local - Queue that organizes the generation of JSON files containing the analysis results of each repository

fila_geracao_json - Queue that organizes JSON generation requests (treemap/heatmap) according to past metrics

queue_analyse_metrics - Queue that organizes requests for analysis of the repository's metrics

queue_analyzer - Queue that organizes treemap analysis requests

fila_scatter_plot - Queue that organizes requests for special metrics to generate scatter plots for the most "critical" files

Login with the guest/guest user to view the message broker operations in real time.

### To view messages from a queue in RabbitMQ (Server2):

Access the docker container running Server2

```
rabbitmqadmin get queue=fila_operacoes_arquivos_local count=10
```

## 3. Run application (Server1)

To run the application, it is necessary to install all the modules and extensions mentioned above. In addition, you need to set the following environment variables:

For the Posix environment:
```bash
# Shell 1
export FLASK_APP=run.py && export FLASK_ENV=development
```
More details at [CLI Flask](https://flask.palletsprojects.com/en/2.0.x/cli/)

Run the application via CLI:
```bash
# Shell 1
flask run --host=0.0.0.0 --port=5000
```

### 3.1 Running Producers and Consumers

producer of the queue_repositorio_local - updates in the database and requests cloning - (producer)
```
running in main.py
```

(Server1) - Consumer of queue_repositorio_local and producer of queue_status_banco - clones and requests DB update - (consumer and producer)

Activate virtual environment
```bash
# shell 2
source venv/bin/activate
```
```
python3 consumer_clona_repository.py
```

(Server1) - Consumer of the queue_status_banco and producer of the queue_analyse_commits - updates the DB and requests analysis from the repository - (consumer and producer)

Activate virtual environment
```bash
# shell 3
source venv/bin/activate
```
```
python3 consumer_update_status_database.py
```

(Server1) - Consumer of the queue_analyze_commits and producer of the queue_operacoes_arquivos_local - analyzes the commits of the repository and requests to generate JSON - (consumer and producer)

Activate virtual environment
```bash
# Shell 4
source venv/bin/activate
```
```
python3 consumer_analyses_commits.py
```

(Server1) - Consumer of queue_local_files - Generates the JSON file with the results of the analysis of the repository.

Activate virtual environment
```bash
# Shell 5
source venv/bin/activate
```
```
python3 consumer_gera_json.py
```

(Server1) - Consumer of the queue_analyse_metrics - Calculates the repository metrics and generates .csv files of the results.

Activate virtual environment
```bash
# Shell 6
source venv/bin/activate
```
```
python3 consumer_analyses_metrics.py
```

(Server1) - Consumer of the queue_scatter_plot - Calculates the special metrics of the repository and generates the boxplot and scatter plot images of the "critical" files

Activate virtual environment
```bash
# Shell 7
source venv/bin/activate
```
```
python3 consumer_scatter_plot.py
```

(Server1) - The "agent" (consumer) [repository parser for treemap] parses (consumes from parser_queue ) the repository and corresponding json files.

Activate virtual environment
```bash
# Shell 8
source venv/bin/activate
```
```
python3 consumer_treemap_analyzer.py
```

### 3.2 Calling the web application

http://localhost:5000

# More details

[Wiki](https://github.com/Technical-Debt-Large-Scale/sysrepoanalysis/wiki)

[On-line sample](https://armandossrecife.github.io/kafka-treemap/)
