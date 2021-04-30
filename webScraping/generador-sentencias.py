# %%
import pandas as pd
counter = 0


sentencias = pd.read_csv('sentencias_test_abril.csv')


print(sentencias.info())
print(sentencias.head())

print(sentencias.head())

~# %% 
# dicc. del equipo de integrantes del equipo
correos_equipo = {
     'Fede': '',
     'Arturo': 'lierarturo@gmail.com',
     'Fernando':'fernadogomez210398@gmail.com',
     'Ricardo':'ricardobenacres@gmail.com',
     'David':'david.velozs@outlook.com',
     'Victor':'amayalvictor@hotmail.com',
     'Les':'lesliepbv@gmail.com',
     'Raquel':'',
     'Vale':'',
     'Yosshua':''}

team = []
for key in correos_equipo:
    team.append(key)


# %%
# %%
import numpy as np

def assign_person(id, team):
    return (team[id % len(team)])

sentencias['responsable'] = sentencias.reset_index()['index'].apply(lambda x: assign_person(x, team)) 

# %%
sentencias['responsable']
# %%
sentencias[sentencias['responsable']=='Fede']




# %%
import requests
import time
from bs4 import BeautifulSoup
from random import randint

def make_soup(url):
    no_soup = True
    attempts = 0
    while no_soup and attempts < 10:
        try:
            html = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}).content
            no_soup = False
        except:
            attempts += 1
            time.sleep(randint(50, 200)/10)
    if no_soup: 
        return 'No-soup'
    else:
        return BeautifulSoup(html, "html.parser")

def get_pdf_url(url):
    import re
    prefix = 'https://www.pjenl.gob.mx/SentenciasPublicas/PDFVisor/'
    soup = make_soup(url)
    pattern = re.compile(r"var DEFAULT_URL = '(.*?)';")
    script = soup.find('script', text = pattern)
    pdf_url = prefix + re.search(pattern, str(script)).group(1)
    #print(str(counter)+':\t',pdf_url,'\n')
    print(pdf_url)
    return (pdf_url)

# url = 'https://www.pjenl.gob.mx/SentenciasPublicas/PDFVisor/Visor.aspx?p=6IQayxSGvfKFFaLn0+VVEnXvePaFpPmHaMDnyyY0kx3kX26ZRaGN9nkgG6miCfe4SMJyPDa5Hs9ekSBKnzPKe21D3NAM2AVZj8rF7HRJMuqKfTNJxuW5KB1zGO1TeKSaE5niCNeq5TqwmG7tCPRmUuqv31z/h0nt9a4Ricgr8LfjY7/26R311Oa1dbFsvXtUcPX+ZMurhjFqSvkzC55L+WBk+WzaJAYY9NiN0zggLhA='
# print(get_pdf_url(url))




# %%
import requests
import os



def descargar_pdfs(id, download_url,person = ''):
    pdf_path = r'C:\Users\dvdve\OneDrive - INSTITUTO TECNOLOGICO AUTONOMO DE MEXICO\DataLab'
    if person != '':
        pdf_path += '\\' + person 
    else:
        pdf_path += '\\' + 'new_pdfs'
    headers = {'Content-type': 'application/pdf'}
    response = requests.get(download_url, headers = headers)    
    try:
        with open(pdf_path + "\\sentencia_{}.pdf".format(id), 'wb') as f:
            f.write(response.content)
    except:
        os.makedirs(pdf_path)
        with open(pdf_path + "\\sentencia_{}.pdf".format(id), 'wb') as f:
            f.write(response.content)


# %%

#sentencias.reset_index(inplace=True) 
for person in team:
    aux = sentencias[sentencias['responsable']==person]
    aux.apply(lambda x: descargar_pdfs(x['index'], x['Sentencia'],  x['responsable']), axis = 1)


# %%
# Generamos nuevos links
sentencias_all = pd.read_csv('All_Sentencias.csv')
sentencias_all['real_url'] = sentencias_all['Sentencia'].apply(lambda x: get_pdf_url(x))
sentencias_all.to_csv('sentencias_with_url.csv')
sentencias_new = sentencias_all.drop(index = range(100))
sentencias_new.to_csv('sentencias_nuevas.csv')

# %%
import pandas as pd
sentencias_new = pd.read_csv('sentencias_with_url.csv', index_col=0)
sentencias_new.drop(index = range(1481), inplace = True)
(sentencias_new.reset_index()).apply(lambda x: descargar_pdfs(x['index'],x['real_url']), axis = 1)

# %%
# %%
