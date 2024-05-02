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

from selenium import webdriver
#from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import dateparser


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def yop_l_frii():
    # List of URLs
    urls = [
        f"https://yop.l-frii.com/offres-demplois/{category}/" for category in range(3276)
        # Add more URLs as needed
    ]

    job_data = []

    for url in urls:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
            soup = BeautifulSoup(response.content, 'html.parser')

            job_articles = soup.find_all('article', class_='type-emploi')

            for article in job_articles:
                job_title_element = article.find('h2', class_='elementor-heading-title')
                job_title = job_title_element.text.strip() if job_title_element else None

                job_link = article.find('a', href=True)['href']

                job_image_element = article.find('img', class_='attachment-large')
                job_image = job_image_element['src'] if job_image_element else None

                job_data.append({
                    "Job Title": job_title,
                    "Job Link": job_link,
                    "Job Image": job_image,
                    "Source URL": url
                })
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching data from {url}: {e}")

    df_yop_l_frii = pd.DataFrame(job_data)

    # Définition de l'équivalence entre les variables
    equivalences = {
        "Job Title": "INTITULE_DU_POSTE",
        "Job Link": "URL_DU_POSTE",
        "Job Image": None,
        "Source URL": None
    }

    # Fonction pour renommer les colonnes du DataFrame en conservant les colonnes sans équivalence
    def renommer_colonnes(df, equivalences):
        colonnes_renommees = {ancien_nom: nouvel_nom for ancien_nom, nouvel_nom in equivalences.items() if
                              nouvel_nom is not None}
        df_renomme = df.rename(columns=colonnes_renommees)
        return df_renomme

    # Renommer les colonnes du DataFrame
    df_yop_l_frii = renommer_colonnes(df_yop_l_frii, equivalences)

    # Afficher le DataFrame avec les colonnes renommées
    return df_yop_l_frii





def extract_job_information(url):
    try:
        # Envoyer une requête GET à l'URL
        response = requests.get(url)
        response.raise_for_status()  # Lever une exception en cas d'erreur HTTP
        # Utiliser BeautifulSoup pour analyser le contenu HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # Rechercher les éléments contenant les informations sur l'emploi
        job_info_elements = soup.find_all('div', class_='elementor-widget-container')

        # Initialiser un dictionnaire pour stocker les informations
        job_info = {'URL_DU_POSTE': url}

        # Parcourir les éléments et extraire les informations
        for element in job_info_elements:
            # Trouver le titre de l'emploi
            title_element = element.find('h2', class_='elementor-heading-title')
            if title_element:
                job_info['Titre du Poste'] = title_element.text.strip()

            # Trouver les autres informations sur l'emploi
            other_info_elements = element.find_all('h2', class_='elementor-heading-title')
            for info_element in other_info_elements:
                info_text = info_element.text.strip()
                # Vérifier chaque élément d'information et l'ajouter au dictionnaire
                if 'Niveau Requis' in info_text:
                    job_info['Niveau Requis'] = info_text.split(':')[-1].strip()
                elif 'Année d\'Expérience Requise' in info_text:
                    job_info['Année d\'Expérience Requise'] = info_text.split(':')[-1].strip()
                elif 'Lieu du Travail' in info_text:
                    job_info['Lieu du Travail'] = info_text.split(':')[-1].strip()
                elif 'Date de Soumission' in info_text:
                    job_info['Date de Soumission'] = info_text.split(':')[-1].strip()

        return job_info
    except Exception as e:
        print(f"Erreur lors de l'extraction des informations pour l'URL {url}: {e}")
        return {'URL_DU_POSTE': url}

def extract_job_info_from_urls(urls):
    # Initialiser une liste pour stocker les informations sur les emplois
    job_info_list = []
    # Parcourir les URLs et extraire les informations sur les emplois
    for url in urls:
        job_info = extract_job_information(url)
        job_info_list.append(job_info)
    # Créer un DataFrame à partir de la liste des informations sur les emplois
    df = pd.DataFrame(job_info_list)
    return df

