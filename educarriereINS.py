#!/usr/bin/env python
# coding: utf-8

# In[24]:


urls = ["https://emploi.educarriere.ci/nos-offres?page1={}&codes=&mots_cles=&typeemploi1=&niveau1=&anciennete=&typeoffre1=&recruteur=".format(category) for category in range(30)]


# # Novojob.com

# In[67]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

# Liste des liens pour chaque catégorie
category_links = [
    'https://www.novojob.com/cote-d-ivoire/offres-d-emploi?q=comptabilit%C3%A9',
    'https://www.novojob.com/cote-d-ivoire/offres-d-emploi?q=finance',
    'https://www.novojob.com/cote-d-ivoire/offres-d-emploi?q=marketing',
    'https://www.novojob.com/cote-d-ivoire/offres-d-emploi?q=statistique',
    'https://www.novojob.com/cote-d-ivoire/offres-d-emploi?q=gestion-de-projets'
]

intitules_list = []
entreprises_list = []
pays_list = []
dates_list = []
lien_list = []
niveau_list = []  
experience_list = []

# Utilisation d'un en-tête pour éviter d'être bloqué
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Parcourir les liens de chaque catégorie
for category_link in category_links:
    req = requests.get(category_link, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    time.sleep(5)  # Attendre 5 secondes avant la prochaine requête
    
    offres = soup.find_all('h2', class_='ellipsis row-fluid')
    entreprises = soup.find_all('h6', class_='ellipsis')
    niveaux = soup.find_all('span', class_='spaced-right phone-display-blok')

    for offre, entreprise, niveau in zip(offres, entreprises, niveaux):
        bloc_bottom = offre.find_next('div', class_='bloc-bottom')
        intitules_list.append(offre.get_text().strip())
        entreprises_list.append(entreprise.get_text().strip())
        lien_list.append(category_links.index(category_link))

        # Les informations (pays, date, niveau, expérience) sont contenues dans la même span, nous devons les séparer
        pays_info = bloc_bottom.find('i', class_='fa fa-map-marker icon-left')
        pays = pays_info.find_parent().text.strip() if pays_info else None
        pays_list.append(pays)

        date_info = bloc_bottom.find('i', class_='fa fa-clock-o icon-left')
        date = date_info.find_parent().text.strip() if date_info else None
        dates_list.append(date)

        # Ajout des colonnes pour le niveau du poste et l'expérience demandée
        niveau_info = niveau.find('i', class_='fa fa-bookmark icon-left')
        niveau_text = niveau_info.find_parent().text.strip() if niveau_info else None

        # Utiliser une expression régulière pour extraire les informations de niveau et d'expérience
        match = re.match(r'(.+) \((.+)\)', niveau_text)

        if match:
            niveau_col, experience_col = match.groups()
        else:
            niveau_col, experience_col = None, None

        niveau_list.append(niveau_col)
        experience_list.append(experience_col)

# Convertir les offres d'emploi en DataFrame
df_offers = pd.DataFrame({
    'Intitule': intitules_list,
    'Entreprise': entreprises_list,
    'Pays': pays_list,
    'Date': dates_list,
    'Niveau': niveau_list,
    'Experience_lettre': experience_list,
    'Lien': lien_list
})

# Afficher le DataFrame
# Mapping dictionary for experience classes

experience_mapping = {
    'Moins d’un an': 1,
    'Sans expérience' : 1,
    '1 à 2 ans': 2,
    '3 à 5 ans': 4,
    '6 à 10 ans': 8,
    'Plus de 10 ans': 15  # Assuming "Plus de 10 ans" corresponds to more than 10 years
}
# Apply the mapping to the 'Experience' column
df_offers['Experience'] = df_offers['Experience_lettre'].map(experience_mapping)

# Display the updated DataFrame
# Apply the mapping to the 'Experience' column
df_offers['Experience'] = df_offers['Experience_lettre'].map(experience_mapping)
#Ajout de la colonne ID
df_offers['ID'] = range(1, len(df_offers) + 1)
df_offers.insert(0, 'ID', df_offers.pop('ID'))

# Create quartile bins
# Créer les intervalles de quartile
quartile_bins = pd.qcut(df_offers['Experience'], q=4, labels=False, duplicates='drop')

# Créer la colonne 'Classe'
# Créer la colonne 'Classe' avec seulement trois labels
df_offers['Classe'] = pd.qcut(df_offers['Experience'], q=4, labels=['Q1', 'Q2', 'Q3'], duplicates='drop')



# Display the updated DataFrame
df_offers



# In[68]:


import pyodbc
import pandas as pd
from datetime import datetime

# Paramètres de connexion à la base de données SQL Server
server = 'DESKTOP-UPJK2FT\\SQLEXPRESS'
database = 'INS'
# Trouver le nom d'utilisateur Windows (echo %USERNAME% dans le terminal)
username = 'DESKTOP-UPJK2FT\HP'

# Définissez le pilote séparément
driver = "ODBC Driver 17 for SQL Server"

# Obtenez la date actuelle au format yyyymmdd
current_datetime = datetime.now()

# Générez un nom de table unique avec la date et l'heure actuelles sans les minutes et les secondes
table_name = f'Emploi_Offers_{current_datetime.strftime("%Y%m%d_%H")}'

# Créer une connexion à la base de données avec PyODBC
conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      f'Server={server};'
                      f'Database={database};'
                      'Trusted_Connection=yes;', autocommit=True)

# Créez la table dans la base de données en utilisant pyodbc
table_creation_query = f'''
CREATE TABLE {table_name} (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    Intitule NVARCHAR(255),
    Entreprise NVARCHAR(255),
    Pays NVARCHAR(255),
    Date NVARCHAR(255),
    Niveau NVARCHAR(255),
    Experience_lettre NVARCHAR(255),
    Lien INT,
    Experience INT,
    Classe NVARCHAR(255)
)
'''

with conn.cursor() as cursor:
    cursor.execute(table_creation_query)

# Replace df_offers with your actual DataFrame

# Assuming df_offers is a DataFrame with columns like Intitule, Entreprise, etc.
# Exclude the 'ID' column if it's an identity column with auto-increment.
table_name = f'Emploi_Offers_{current_datetime.strftime("%Y%m%d_%H")}'
# Use parameterized query to avoid SQL injection
insert_query = f"INSERT INTO INS.dbo.{table_name} (Intitule, Entreprise, Pays, Date, Niveau, Experience_lettre, Lien, Experience, Classe) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"

# Iterate over rows in the DataFrame
for index, row in df_offers.iterrows():
    # Get values for the current row
    values = (
        str(row['Intitule']),
        str(row['Entreprise']),
        str(row['Pays']),
        str(row['Date']).strip(),  # Utiliser la date actuelle avec l'heure (sans les minutes et secondes)
        str(row['Niveau']),
        str(row['Experience_lettre']),
        int(row['Lien']),
        int(row['Experience']),
        str(row['Classe']),
    )

    # Execute the query with the values
    cursor.execute(insert_query, values)

# Fermez la connexion après l'insertion
conn.close()


# # Educarriere.ci

# In[51]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_text(element, class_name=None, style=None, text_contains=None):
    if element:
        tag = element.find(class_=class_name, style=style, text=text_contains)
        return tag.text.strip() if tag else ""
    else:
        return ""

def clean_text(text):
    return text.replace('D\x92', ' ').replace('d\x92', ' ').replace('\x92', ' ').replace('\r\n', '').replace('\xa0', '')

def extract_date(element, text_contains):
    date_elements = element.find_all('a', class_='text')
    date = next((e.find('span', style='color:#FF0000;').text.strip() for e in date_elements if text_contains in e.text), "")
    return date

def scrape_emploi_ci(url):
    try:
        response = requests.get(url, timeout=200)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion à {url} : {e}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, 'html.parser')

    job_description_wrappers = soup.find_all('div', class_='box row')

    data_list = []

    for wrapper in job_description_wrappers:
        h4_tag = wrapper.find('h4')
        poste = extract_text(h4_tag)

        entry_title_tag = wrapper.find('p', class_='entry-title')
        sous_titre = extract_text(entry_title_tag)

        a_text_tag = wrapper.find('a', class_='text')
        code = extract_text(a_text_tag, style='color:#FF0000;')

        date_edition = extract_date(wrapper, "Date d'édition:")
        date_limite = extract_date(wrapper, "Date limite:")

        pays_tag = wrapper.find('a', class_='text')
        pays = pays_tag.find_parent().text.strip().split()[-1] if pays_tag else None

        sous_titre = clean_text(sous_titre)

        data_list.append({
            'Poste': poste,
            'Sous_titre': sous_titre,
            'Code': code,
            'Date_DEdition': date_edition,
            'Date_limite': date_limite,
            'Pays': pays
        }) 

    df = pd.DataFrame(data_list)
    return df

# Liste des liens
urls = ["https://emploi.educarriere.ci/nos-offres?page1={}&codes=&mots_cles=&typeemploi1=&niveau1=&anciennete=&typeoffre1=&recruteur=".format(category) for category in range(30)]

# Créer un DataFrame à partir des liens
result_df = pd.concat([scrape_emploi_ci(url) for url in urls], ignore_index=True)

# Afficher le DataFrame
result_df


# In[66]:


import pyodbc
import pandas as pd
from datetime import datetime

# Paramètres de connexion à la base de données SQL Server
server = 'DESKTOP-UPJK2FT\\SQLEXPRESS'
database = 'INS'
# Trouver le nom d'utilisateur Windows (echo %USERNAME% dans le terminal)
username = 'DESKTOP-UPJK2FT\HP'

# Définissez le pilote séparément
driver = "ODBC Driver 17 for SQL Server"

# Obtenez la date actuelle au format yyyymmdd
current_datetime = datetime.now()

# Générez un nom de table unique avec la date et l'heure actuelles sans les minutes et les secondes
table_name = f'Emploi_educarriere_{current_datetime.strftime("%Y%m%d_%H")}'

# Créer une connexion à la base de données avec PyODBC
conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      f'Server={server};'
                      f'Database={database};'
                      'Trusted_Connection=yes;', autocommit=True)

# Créez la table dans la base de données en utilisant pyodbc
table_creation_query = f'''
CREATE TABLE {table_name} (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    Poste NVARCHAR(255),
    Sous_titre NVARCHAR(1000),
    Date_DEdition NVARCHAR(255),
    Date_limite NVARCHAR(255),
    Pays NVARCHAR(255),

)
'''

with conn.cursor() as cursor:
    cursor.execute(table_creation_query)

# Replace df_offers with your actual DataFrame

# Assuming df_offers is a DataFrame with columns like Intitule, Entreprise, etc.
# Exclude the 'ID' column if it's an identity column with auto-increment.
table_name = f'Emploi_educarriere_{current_datetime.strftime("%Y%m%d_%H")}'
# Use parameterized query to avoid SQL injection
insert_query = f"INSERT INTO INS.dbo.{table_name} (Poste, Sous_titre, Date_DEdition, Date_limite, Pays) VALUES (?, ?, ?, ?, ?)"

# Iterate over rows in the DataFrame
for index, row in result_df.iterrows():
    # Get values for the current row
    values = (
        str(row['Poste']),
        str(row['Sous_titre']),
        str(row['Date_DEdition']).strip(), 
        str(row['Date_limite']).strip(),# Utiliser la date actuelle avec l'heure (sans les minutes et secondes)
        str(row['Pays']),
    )

    # Execute the query with the values
    cursor.execute(insert_query, values)

# Fermez la connexion après l'insertion
conn.close()


# In[23]:


df.to_csv('df_offers2.csv', index=False)


# # Emploi.ci

# In[61]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_text(element, tag_name=None):
    tag = element.find(tag_name)
    return tag.text.strip() if tag else ""

def clean_text(text):
    return text.replace('D\x92', ' ').replace('d\x92', ' ').replace('\x92', ' ').replace('\r\n', '').replace('\xa0', '')

def scrape_emploi_ci(url):
    try:
        response = requests.get(url, timeout=500)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion à {url} : {e}")
        return pd.DataFrame()

    soup = BeautifulSoup(response.text, 'html.parser')

    job_description_wrappers = soup.find_all('div', class_='job-description-wrapper')

    data_list = []

    for wrapper in job_description_wrappers:
        h5_tag = wrapper.find('h5')
        poste = extract_text(h5_tag, 'a')

        job_recruiter_tag = wrapper.find('p', class_='job-recruiter')
        date_and_company = job_recruiter_tag.text.strip().split('|')
        date = date_and_company[0].strip() if date_and_company else ""
        entreprise = extract_text(job_recruiter_tag, 'a')

        description_tag = wrapper.find('div', class_='search-description')
        description = clean_text(description_tag.text.strip()) if description_tag else ""

        region_tag = wrapper.find('p', text='Région de :')
        region = extract_text(region_tag) if region_tag else ""

        data_list.append({
            'Poste': poste,
            'Entreprise': entreprise,
            'Date': date,
            'Description': description,
            'Région': region
        })

    df = pd.DataFrame(data_list)
    return df

# Liste des liens
categories = ["31", "1127", "29", "37", "1115", "30", "1115", "32", "33", "34", "35", "36", "37", "39", "38", "40", "525", "41", "28"]

# Liste d'URLs générées
urls = ["https://www.emploi.ci/recherche-jobs-cote-ivoire/?f%5B0%5D=im_field_offre_metiers%3A{}".format(category) for category in categories]

# Créer un DataFrame à partir des liens
df = pd.concat([scrape_emploi_ci(url) for url in urls], ignore_index=True)

# Afficher le DataFrame
df


# In[62]:


import pyodbc
import pandas as pd
from datetime import datetime

# Paramètres de connexion à la base de données SQL Server
server = 'DESKTOP-UPJK2FT\\SQLEXPRESS'
database = 'INS'
# Trouver le nom d'utilisateur Windows (echo %USERNAME% dans le terminal)
username = 'DESKTOP-UPJK2FT\HP'

# Définissez le pilote séparément
driver = "ODBC Driver 17 for SQL Server"

# Obtenez la date actuelle au format yyyymmdd
current_datetime = datetime.now()

# Générez un nom de table unique avec la date et l'heure actuelles sans les minutes et les secondes
table_name = f'Emploi_ci_{current_datetime.strftime("%Y%m%d_%H")}'

# Créer une connexion à la base de données avec PyODBC
conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      f'Server={server};'
                      f'Database={database};'
                      'Trusted_Connection=yes;', autocommit=True)

# Créez la table dans la base de données en utilisant pyodbc
table_creation_query = f'''
CREATE TABLE {table_name} (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    Poste NVARCHAR(255),
    Entreprise NVARCHAR(255),
    Date NVARCHAR(255),
    Description NVARCHAR(1000),
    Région NVARCHAR(255),

)
'''

with conn.cursor() as cursor:
    cursor.execute(table_creation_query)

# Replace df_offers with your actual DataFrame

# Assuming df_offers is a DataFrame with columns like Intitule, Entreprise, etc.
# Exclude the 'ID' column if it's an identity column with auto-increment.
table_name = f'Emploi_ci_{current_datetime.strftime("%Y%m%d_%H")}'
# Use parameterized query to avoid SQL injection
insert_query = f"INSERT INTO INS.dbo.{table_name} (Poste, Entreprise, Date, Description, Région) VALUES (?, ?, ?, ?, ?)"

# Iterate over rows in the DataFrame
for index, row in df.iterrows():
    # Get values for the current row
    values = (
        str(row['Poste']),
        str(row['Entreprise']),
        str(row['Date']).strip(), 
        str(row['Description']),# Utiliser la date actuelle avec l'heure (sans les minutes et secondes)
        str(row['Région']),
    )

    # Execute the query with the values
    cursor.execute(insert_query, values)

# Fermez la connexion après l'insertion
conn.close()


# In[73]:


pip install scipy

