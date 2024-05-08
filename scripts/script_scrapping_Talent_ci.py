#----------------------------------------------------------------------------------------------------------------------------------------------------------------
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

def talent_ci():
    def extract_text(element, tag_name=None):
        tag = element.find(tag_name)
        return tag.text.strip() if tag else ""

    def clean_text(text):
        return text.replace('\r\n', '').replace('\xa0', '')

    def scrape_talent_com(url):
        try:
            response = requests.get(url, timeout=500)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Erreur de connexion à {url} : {e}")
            return pd.DataFrame()

        soup = BeautifulSoup(response.text, 'html.parser')

        job_wrappers = soup.find_all('div', class_='card card__job')

        data_list = []

        for wrapper in job_wrappers:
            title_tag = wrapper.find('h2', class_='card__job-title')
            title = extract_text(title_tag, 'a')
            
            employer_location_tag = wrapper.find('div', class_='card__job-empnameLocation')
            #employer = extract_text(employer_location_tag.find('div', class_='card__job-location'))  # Extract location from the inner div
            location= extract_text(employer_location_tag, 'div')

            employer_location_tag = wrapper.find('div', class_='card__job-empname-label')
            
            # Extracting employer and description from the div
            employer = employer_location_tag.text.strip() if employer_location_tag else None  # Extract location from the inner div
            
            description_tag = wrapper.find('div', class_='card__job-snippet-logo')
            description = clean_text(extract_text(description_tag, 'p'))

            data_list.append({
                'Title': title,
                'Location': location,
                'Employer': employer,
                'Description': description,
                'URL': url
            })

        df = pd.DataFrame(data_list)
        return df

    # List of URLs for talent.com jobs
    urls = [
         "https://ci.talent.com/jobs?l=Abidjan%2C+Abidjan&radius=15&p={}&k=&context=serp_pagination".format(category) for category in range(8)
        # Add more URLs as needed "https://ci.talent.com/jobs",
    ]

    # Initialize an empty DataFrame to store the results
    ci_talent = pd.DataFrame()

    # Scrape job information for each URL and concatenate the results
    for url in urls:
        df = scrape_talent_com(url)
        ci_talent = pd.concat([ci_talent, df], ignore_index=True)

    # Définition de l'équivalence entre les variables
    equivalences = {
        "Title": "INTITULE_DU_POSTE",
        "Location": "LIEU_DU_POSTE_DE_TRAVAIL",
        "Employer": "RAISON_SOCIALE_DE_L_ENTREPRISE",
        "Description": "DESCRIPTION_DU_POSTE",
        "URL": "SITE_WEB_DE_L_ENTREPRISE"
    }

    # Fonction pour renommer les colonnes du DataFrame en conservant les colonnes sans équivalence
    def renommer_colonnes(df, equivalences):
        colonnes_renommees = {ancien_nom: nouvel_nom for ancien_nom, nouvel_nom in equivalences.items() if nouvel_nom is not None}
        df_renomme = df.rename(columns=colonnes_renommees)
        return df_renomme

    # Renommer les colonnes du DataFrame
    ci_talent = renommer_colonnes(ci_talent, equivalences)

    # Afficher le DataFrame avec les colonnes renommées
    return ci_talent

