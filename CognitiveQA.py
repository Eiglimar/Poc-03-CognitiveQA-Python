import json
import pymysql
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import watson_developer_cloud
from watson_developer_cloud import LanguageTranslatorV2 as LanguageTranslator
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, EntitiesOptions, KeywordsOptions, SentimentOptions
from jira.client import JIRA
#----------------------------------Início das Declarações-----------------------------------------#
assistant = watson_developer_cloud.AssistantV1(
    username='xxxxxx',#----->Your Assistant service username here
    password='xxxxxx',#----->Your Assistant service password here
    version='2018-02-16'
)

natural_language_understanding = NaturalLanguageUnderstandingV1(
  username='xxxxxx',#----->Your NLU service username here
  password='xxxxxx',#----->Your NLU service password here
  version='2018-03-16')

language_translator = LanguageTranslator(
username='xxxxxx',#----->Your Translate service username here
password='xxxxxx')#----->Your Translate service password here
#----------------------------------Fim das Declarações--------------------------------------------#

#-----------------------------------Início dasFunções---------------------------------------------#
logFile = open('/log_api_sagram_06-02-2018.txt','r')#----> path of your files here
logMessageRaw = logFile.read()
logFile.close()

# print(logMessageRaw)
logMessageOk = re.sub(u'[^a-zA-Z0-9áéíóúÁÉÍÓÚâêîôÂÊÎÔãõÃÕ: ]', ' ', logMessageRaw)

responseWA = assistant.message(
    workspace_id='xxxxxx',#----->Your Assistant service Workspace ID here
    input={
        'text': logMessageOk
    }
)
#print(json.dumps(responseWA['entities'][0], indent=2))
# print(json.dumps(responseWA['entities'][0]['confidence'], indent=2))
identifiedError = []
for identifiedError in responseWA['entities']:
    
    df = pd.read_excel('/myFile.xlsx', sheet_name='Sheet1')#----->The path of your file here
    causaerro = ''

    for aux in df.index:
        nomeErro = str(df['Erro'][aux])
        tipoErro = str(df['Tipo de Erro'][aux])
        prioridade = str(df['Prioridade'][aux])
        responsavelSolucao = str(df['Responsavel'][aux])
        #print(nomeErro)
        if nomeErro.lower() == identifiedError['value']:
            causaErro = str(df['Causas'][aux])
            solucaoErro = str(df['Solucao'][aux])

            print(nomeErro)
            print(causaErro)
            print(solucaoErro)

            options={'server': #'your Jira server here'}

            jira=JIRA(options,basic_auth=('xxxxxx', 'xxxxxx'))#----->Your Jira service account details here


            root_dict = {
            'project' : { 'key': 'DTS' },
            'summary' : 'Teste de criação de issue #XX -'+nomeErro+' econtrado',
            'description' : 'Essa task foi criada dinamicamente e encontrou um '+nomeErro+' , as possiveis causas desse erro são: '+causaErro+'.',
            'issuetype' : { 'name' : 'Occurrence' },
            'priority': {'name': prioridade},
            'assignee':{'name': responsavelSolucao}
            }

            my_issue= jira.create_issue(fields=root_dict)


    