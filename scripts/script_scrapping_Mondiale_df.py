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


def mondiale_ci():
    # Fonction pour extraire les données d'une page
    def scrape_page(url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Lèvera une exception si la requête a échoué
            soup = BeautifulSoup(response.content, "html.parser")
            job_rows = soup.find("table", class_="results-table").find("tbody").find_all("tr")

            # Listes pour stocker les données de cette page
            job_titles = []
            locations = []
            job_families = []
            deadlines = []

            # Parcourir chaque ligne du tableau et extraire les informations nécessaires
            for row in job_rows:
                # Récupérer le titre de l'emploi
                job_title = row.find("a").text.strip()
                job_titles.append(job_title)

                # Récupérer l'emplacement
                location = row.find_all("td")[1].text.strip()
                locations.append(location)

                # Récupérer la famille d'emploi
                job_family = row.find_all("td")[2].text.strip()
                job_families.append(job_family)

                # Récupérer la date limite d'application
                deadline = row.find_all("td")[3].text.strip()
                deadlines.append(deadline)

            # Retourner les données de cette page sous forme de DataFrame
            data = {
                "Job Title": job_titles,
                "Location": locations,
                "Job Family": job_families,
                "Deadline": deadlines
            }
            return pd.DataFrame(data)
        except requests.exceptions.RequestException as e:
            print("Une erreur s'est produite lors de la requête:", e)
            return pd.DataFrame()  # Retourner un DataFrame vide en cas d'erreur

    # URL de la première page
    base_url = "https://worldbankgroup.csod.com/ats/careersite/search.aspx?site=1&c=worldbankgroup&sid=%5e%5e%5eFLGscZMYY2RrwVaMR%2ftHYw%3d%3d"

    # Créer une liste pour stocker les DataFrames de chaque page
    dfs = []

    # Extraire les données de la première page
    dfs.append(scrape_page(base_url))

    # Trouver le nombre total de pages
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "html.parser")
    pagination_span = soup.find("span", class_=re.compile(r"\btext\b"), text=re.compile(r"\d+"))
    if pagination_span:
        num_pages = int(pagination_span.text.strip())
    else:
        num_pages = 1

    # Boucle à travers chaque page et extraire les données
    for page_num in range(1, num_pages + 1):
        page_url = f"{base_url}&pg={page_num}"
        df = scrape_page(page_url)
        if not df.empty:  # Vérifier si le DataFrame n'est pas vide
            dfs.append(df)

    # Concaténer tous les DataFrames en un seul
    df_mondiale = pd.concat(dfs, ignore_index=True)

    # Définition de l'équivalence entre les variables
    equivalences = {
        "Job Title": "INTITULE_DU_POSTE",
        "Location": "LIEU_DU_POSTE_DE_TRAVAIL",
        "Job Family": "SECTEUR",
        "Deadline": "DATE_D_EXPIRATION_DE_L_OFFRE"
    }

    # Fonction pour renommer les colonnes du DataFrame en conservant les colonnes sans équivalence
    def renommer_colonnes(df, equivalences):
        colonnes_renommees = {ancien_nom: nouvel_nom for ancien_nom, nouvel_nom in equivalences.items() if nouvel_nom is not None}
        df_renomme = df.rename(columns=colonnes_renommees)
        return df_renomme

    # Renommer les colonnes du DataFrame
    df_mondiale = renommer_colonnes(df_mondiale, equivalences)

    # Afficher le DataFrame avec les colonnes renommées
    return df_mondiale

