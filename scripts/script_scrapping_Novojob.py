import time
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
from selenium import webdriver
#from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import dateparser

import os


def scrap_novojob():
    # Liste des liens pour chaque catégorie
    categories = [
        "toutes les offres d'emploi",
        "juridique,fiscal,audit,conseil",
        "administrations,moyens généraux",
        "assistanat,secrétariat",
        "metiers banque et assurances",
        "RH,personnel,formation",
        "education,enseignement",
        "direction générale,direction d'unité",
        "vente,televente,assistanat",
        "commercial,technico commercial,service client",
        "responsable commercial,grands comptes",
        "créatio, design",
        "marketing, communication",
        "journalisme,médias,traduction",
        "informatique,systèmes d'information,internet",
        "télécommunication,réseaux",
        "chantier,métiers BTP,architecture",
        "ingénierie,etudes,projet,R&D",
        "logistique,achat,stock,transport",
        "production,méthode,industrie",
        "maintenance,entretien",
        "Qualité,sécurité,Environnement",
        "Santé,Médical,Pharmacie",
        "Hotellerie,Tourisme,Restauration, Loisirs",
        "Ouvriers qualifiés, Chauffeur",
        "autre",
        "Métiers de l'agriculture"
    ]

    base_url = "https://www.novojob.com/cote-d-ivoire/offres-d-emploi?q="
    category_links = [f"{base_url}{'+'.join(category.split(','))}" for category in categories]

    # Utilisation d'un en-tête pour éviter d'être bloqué
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    intitules_list = []
    entreprises_list = []
    pays_list = []
    dates_list = []
    niveau_list = []
    experience_list = []

    url_list = []
    all_job_lien = []

    # Parcourir les liens de chaque catégorie
    for category_link in category_links:
        req = requests.get(category_link, headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        time.sleep(5)  # Attendre 5 secondes avant la prochaine requête

        offres = soup.find_all('div', class_='row-fluid job-details pointer')

        for offre in offres:
            offre_link_tag = offre.find('a')
            if offre_link_tag:
                offre_link = offre_link_tag['href']
                all_job_lien.append(offre_link)

            entreprise_tag = offre.find('h6', class_='ellipsis')
            entreprise = entreprise_tag.get_text().strip() if entreprise_tag else None

            intitule_tag = offre.find('h2', class_='ellipsis row-fluid')
            intitule = intitule_tag.get_text().strip() if intitule_tag else None

            bloc_bottom = offre.find_next('div', class_='bloc-bottom')

            pays_info = bloc_bottom.find('i', class_='fa fa-map-marker icon-left')
            pays = pays_info.find_parent().text.strip() if pays_info else None

            date_info = bloc_bottom.find('i', class_='fa fa-clock-o icon-left')
            date = date_info.find_parent().text.strip() if date_info else None

            niveau_info = bloc_bottom.find('i', class_='fa fa-bookmark icon-left')
            niveau_text = niveau_info.find_parent().text.strip() if niveau_info else None

            match = re.match(r'(.+) \((.+)\)', niveau_text)
            niveau_col, experience_col = match.groups() if match else (None, None)

            intitules_list.append(intitule)
            entreprises_list.append(entreprise)
            pays_list.append(pays)
            dates_list.append(date)
            niveau_list.append(niveau_col)
            experience_list.append(experience_col)
            
            url_list.append(category_link)

    # Création du DataFrame
    df_offers = pd.DataFrame({
        'Intitule': intitules_list,
        'Entreprise': entreprises_list,
        'Pays': pays_list,
        'Date': dates_list,
        'Niveau': niveau_list,
        'Experience_lettre': experience_list,
        'url': url_list,
        'Offre_Link': all_job_lien
    })

    # Importer les détails de chaque offre d'emploi
    job_urls = list(df_offers['Offre_Link'])
    all_job_details = []

    for url in job_urls:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')

        job_details = {}
        
        # Ajouter le lien
        job_details["Offre_Link"] = url
        
        # Extraction des détails de l'offre d'emploi
        details_section = soup.find('ul', class_='text-small')
        if details_section:
            for li in details_section.find_all('li', class_='row-fluid'):
                key = li.find('span', class_='span4').text.strip()
                value = li.find('span', class_='span8').text.strip()
                job_details[key] = value

        # Extraction du texte fourni
        description_section = soup.find('div', class_='spaced details-description')
        if description_section:
            provided_text = description_section.text.strip()
            job_details['Provided Text'] = provided_text

        all_job_details.append(job_details)

    # Création d'un DataFrame pour les détails des offres d'emploi
    df_Novojob = pd.DataFrame(all_job_details)
    # Ajouter les listes existantes en tant que colonnes au DataFrame
    df_Novojob = pd.merge(df_offers,df_Novojob, on='Offre_Link')
    df_Novojob = df_Novojob.drop_duplicates()
    df_Novojob.reset_index(drop=True, inplace=True)

    
    equivalences = {
    "Offre_Link": "SITE_WEB_DE_L_ENTREPRISE",
    "Nom de l'entreprise": "RAISON_SOCIALE_DE_L_ENTREPRISE",
    "Secteur d'activité": "BRANCHE_D_ACTIVITE",
    "Lieu de travail": "LIEU_DU_POSTE_DE_TRAVAIL",
    "Date d'expiration": "DATE_D_EXPIRATION_DE_L_OFFRE",
    "Nombre de postes": "NOMBRE_DE_POSTES_A_POURVOIR",
    "Niveau de poste": None,
    "Niveau d'étude (diplôme)": "NIVEAU_D_ETUDES",
    "Type de contrat": "TYPE_DE_CONTRAT_DU_POSTE",
    "Provided Text": "Texte_fourni",
    "Intitule": "INTITULE_DU_POSTE",
    "Entreprise": None,
    "Pays": "PAYS_DU_POSTE_DE_TRAVAIL",
    "Date": "DATE_DE_DEBUT_DE_L_OFFRE",
    "Niveau": None,
    "Experience_lettre": None,
    "url_Lien": "Offre_Link1"}
    # Fonction pour renommer les colonnes du DataFrame en conservant les colonnes sans équivalence
    def renommer_colonnes(df, equivalences):
        colonnes_renommees = {ancien_nom: nouvel_nom for ancien_nom, nouvel_nom in equivalences.items() if nouvel_nom is not None}
        df_renomme = df.rename(columns=colonnes_renommees)
        return df_renomme
    df_Novojob = renommer_colonnes(df_Novojob, equivalences)
    df_Novojob['NOMBRE_DE_POSTES_A_POURVOIR'] = df_Novojob['NOMBRE_DE_POSTES_A_POURVOIR'].str.extract(r"([0-9,]+)")
    df_Novojob[["VILLE_DU_POSTE_DE_TRAVAIL","PAYS_DU_POSTE_DE_TRAVAIL"]] = df_Novojob['LIEU_DU_POSTE_DE_TRAVAIL'].str.split(',', expand=True)
    for i in range(len(df_Novojob["PAYS_DU_POSTE_DE_TRAVAIL"])):
        if df_Novojob["PAYS_DU_POSTE_DE_TRAVAIL"][i] is None :
            df_Novojob.loc[i, "PAYS_DU_POSTE_DE_TRAVAIL"] = df_Novojob["VILLE_DU_POSTE_DE_TRAVAIL"][i]
            df_Novojob.loc[i, "VILLE_DU_POSTE_DE_TRAVAIL"]= " "


    # Réorganiser les colonnes selon vos besoins

    return df_Novojob

