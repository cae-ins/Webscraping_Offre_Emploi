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
#Importation du module d'envoi de mail
from selenium import webdriver
#from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import dateparser


def projobivoire():
    def extract_text(element, tag_name=None):
        if element and tag_name:
            tag = element.find(tag_name)
            return tag.text.strip() if tag else ""
        return ""

    def clean_text(text):
        return text.replace('\r\n', '').replace('\xa0', '')

    def scrape_projobivoire_page(page_url):
        job_data_list = []

        for url in page_url:
            try:
                response = requests.get(url, timeout=500)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                    print(f"Erreur de connexion à {url} : {e}")
                    continue

            soup = BeautifulSoup(response.text, 'html.parser')

            job_items = soup.find_all('div', class_='loop-item-wrap list')

            if not job_items:
                print(f"Aucun élément de travail trouvé pour l'URL : {url}")
                continue

            for job_item in job_items:
                title_tag = job_item.find('h3', class_='loop-item-title')
                title = extract_text(title_tag, 'a')

                job_type_tag = job_item.find('span', class_='job-type')
                job_type = extract_text(job_type_tag, 'span')

                job_date_posted = soup.find('span', class_='job-date__posted').text.strip()

                job_date_closing_tag = soup.find('span', class_='job-date__closing')
                job_date_closing = job_date_closing_tag.text.strip() if job_date_closing_tag else ""

                job_date_closing = job_date_closing.lstrip('-').strip()

                category_tag = job_item.find('span', class_='job-category')
                category = extract_text(category_tag, 'a')

                # Ajout de ces lignes pour extraire l'URL de l'e-mail
                email_url_tag = job_item.find('span', class_='noo-tool-email-job')
                email_url = email_url_tag['data-url'] if email_url_tag else ""

                data = {
                    'Title': title,
                    'Type': job_type,
                    'DatePosted': job_date_posted,
                    'DateClosing': job_date_closing,
                    'Category': category,
                    'EmailURL': email_url,
                    'URL': url
                }

                job_data_list.append(data)

        return job_data_list

    # Liste des URL de pages avec plusieurs offres d'emploi
    page_urls = ["https://projobivoire.com/page/{}/".format(category) for category in range(546)]

    # Scrape des détails de chaque offre d'emploi sur les pages
    job_data_list = scrape_projobivoire_page(page_urls)

    # Création d'un DataFrame à partir de la liste des données d'emploi
    df_projobivoire = pd.DataFrame(job_data_list)

    # Affichage du DataFrame

    # Définition de l'équivalence entre les variables
    equivalences = {
        "Title": "INTITULE_DU_POSTE",
        "Type": "TYPE_DE_CONTRAT_DU_POSTE",
        "DatePosted": "DATE_DE_PUBLICATION",
        "DateClosing": "DATE_D_EXPIRATION_DE_L_OFFRE",
        "Category": "CATEGORIE",
        "EmailURL": None,
        "URL": "SITE_WEB_DE_L_ENTREPRISE"
    }

    # Fonction pour renommer les colonnes du DataFrame en conservant les colonnes sans équivalence
    def renommer_colonnes(df, equivalences):
        colonnes_renommees = {ancien_nom: nouvel_nom for ancien_nom, nouvel_nom in equivalences.items() if nouvel_nom is not None}
        df_renomme = df.rename(columns=colonnes_renommees)
        return df_renomme

    # Renommer les colonnes du DataFrame
    df_projobivoire = renommer_colonnes(df_projobivoire, equivalences)

    # Afficher le DataFrame avec les colonnes renommées
    return df_projobivoire

