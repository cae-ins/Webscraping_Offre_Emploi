import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import os

from selenium import webdriver
#from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import dateparser
import os


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def rmo_jobcenter(urls):
    # Base URL du site Web
    base_url = "https://rmo-jobcenter.com"

    # Liste pour stocker les données des offres d'emploi
    all_job_data = []

    # Boucle à travers chaque URL
    for url in urls:
        # Récupération du contenu de la page avec les en-têtes personnalisés
        response = requests.get(url, headers=headers)
        
        # Vérifier si la requête a réussi
        if response.status_code == 200:
            # Analyse du contenu de la page avec BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Trouver la table contenant les offres d'emploi
            table = soup.find('table', class_='liste')

            # Vérifier si la table est trouvée
            if table:
                # Boucle à travers chaque ligne de la table (sauf la première qui contient les en-têtes)
                for row in table.find_all('tr')[1:]:
                    # Extrayez les données de chaque colonne
                    columns = row.find_all('td')
                    date = columns[0].text.strip()
                    filiale = columns[1].text.strip()
                    fonction = columns[2].text.strip()
                    secteur = columns[3].text.strip()
                    reference = columns[4].text.strip()
                    details_url = columns[5].find('a')['href']

                    # Rendez l'URL absolue en la combinant avec l'URL de base.
                    absolute_url = f"{base_url}/{details_url}"

                    # Stockez les données dans un dictionnaire
                    job_entry = {
                        'Date': date,
                        'Filiale': filiale,
                        'Fonction': fonction,
                        'Secteur': secteur,
                        'Référence / Statut': reference,
                        'Détails URL': absolute_url,
                        "URL": url
                    }

                    all_job_data.append(job_entry)

        else:
            print(f"Impossible de récupérer la page {url}")

    # Créez un DataFrame avec toutes les données extraites
    df_jobcenter = pd.DataFrame(all_job_data)

    # Si aucune donnée n'est extraite, retournez un DataFrame vide
    if df_jobcenter.empty:
        return df_jobcenter

    # Liste des URLs des pages d'offres d'emploi détaillées
    detail_urls = list(df_jobcenter['Détails URL'])

    # Liste pour stocker les données détaillées
    all_detail_data = []

    # Boucle à travers chaque URL détaillée
    for detail_url in detail_urls:
        # Récupération du contenu de la page détaillée avec les en-têtes personnalisés
        detail_response = requests.get(detail_url, headers=headers)

        # Vérifier si la requête a réussi
        if detail_response.status_code == 200:
            # Analyse du contenu de la page avec BeautifulSoup
            detail_soup = BeautifulSoup(detail_response.content, 'html.parser')

            # Trouver la div contenant les informations détaillées
            details_div = detail_soup.find('div', {'id': 'content_articles'})

            # Vérifier si la div est trouvée
            if details_div:
                # Extract details from the div
                job_title_element = details_div.find('div', {'id': 'h2_imprime'})
                job_title = job_title_element.text.strip() if job_title_element else None

                job_description_element = details_div.find('div', {'class': 'text-content'})
                job_description = job_description_element.text.strip() if job_description_element else None

                # Stockez les données dans un dictionnaire
                detail_entry = {
                    'Job Title': job_title,
                    'Job Description': job_description,
                    'Détails URL': detail_url
                    # Add more details as needed
                }

                # Ajoutez les données de cette URL à la liste globale
                all_detail_data.append(detail_entry)
            else:
                print("Aucune div avec l'ID 'content_articles' n'a été trouvée.")

    # Créez un DataFrame avec toutes les données détaillées extraites
    df_details = pd.DataFrame(all_detail_data)
    df_details[['Poste', 'Niveau', 'Sous Poste']] = df_details['Job Title'].str.split(' - ', expand=True)

    # Fusionner les deux DataFrames sur la colonne 'Détails URL'
    df_jobcenter = pd.merge(df_jobcenter, df_details, on='Détails URL')
    df_jobcenter = df_jobcenter.drop_duplicates().reset_index(drop=True)
    
    # Renommer les colonnes selon vos besoins
    equivalences = {
    "Date": "DATE",
    "Filiale": "FILIALE",
    "Fonction": "FONCTION",
    "Secteur": "SECTEUR",
    "Référence / Statut": "REFERENCE_STATUT",
    "Détails URL": "DETAILS_URL",
    "Job Title": "INTITULE_DU_POSTE",
    "Job Description": "DESCRIPTION_DU_POSTE",
    "Job URL": "URL_DU_POSTE",
    "Poste": "POSTE",
    "Niveau": "DIPLOME",
    "Sous Poste": "SOUS_POSTE"}

    df_jobcenter.rename(columns=equivalences, inplace=True)

    return df_jobcenter

