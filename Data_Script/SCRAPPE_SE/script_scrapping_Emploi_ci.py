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

def emploi_ci():
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
                'Région': region,
                'URL' : url
            })

        df = pd.DataFrame(data_list)
        return df

    # Liste des liens
    categories = ["31", "1127", "29", "37", "1115", "30", "1115", "32", "33", "34", "35", "36", "37", "39", "38", "40", "525", "41", "28"]
    #categories=["31"]
    # Liste d'URLs générées
    urls = ["https://www.emploi.ci/recherche-jobs-cote-ivoire/?f%5B0%5D=im_field_offre_metiers%3A{}".format(category) for category in categories]

    # Créer un DataFrame à partir des liens
    df = pd.concat([scrape_emploi_ci(url) for url in urls], ignore_index=True)


    from requests.exceptions import ChunkedEncodingError, ConnectionError, ReadTimeout

    # Liste des liens

    # En-tête pour éviter d'être bloqué
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Pour exécuter le navigateur en arrière-plan
    options.add_argument("--disable-gpu")  # Désactiver l'accélération GPU en mode headless
    chrome_driver_path = "C:\\Users\\ngora\\OneDrive\\Bureau\\INS_DATA\\chromedriver_win32\\chromedriver.exe"
    options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"  # Remplacez par l'emplacement réel de votre Chrome binary
    options.add_argument(f"webdriver.chrome.driver={chrome_driver_path}")
    driver = webdriver.Chrome(options=options)

    # Liste pour stocker les détails de chaque emploi
    all_job_details = []

    # Parcourir les liens
    for url in list(df["URL"]):
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        time.sleep(5)  # Attendre 5 secondes avant la prochaine requête

        offres = soup.find_all('div', class_="job-description-wrapper")

        # Parcourir les offres d'emploi sur la page principale
        for offre in offres:
            # Trouver la balise <h4> dans la structure HTML pour extraire le lien
            offre_link_tag = offre.find('h5')

            # Vérifier si la balise <h4> a été trouvée
            if offre_link_tag:
                # Extraire le lien de l'attribut 'href'
                offre_link = offre_link_tag.find('a')['href']
                all_job_details.append({'Offre_Link': "https://www.emploi.ci"+offre_link, 'URL' :url})

    # Fermer le pilote Selenium à la fin
    driver.quit()

    # Concaténer tous les détails des emplois en un seul DataFrame
    if all_job_details:
        all_job_details_df = pd.DataFrame(all_job_details)
        # Afficher le DataFrame
        #print(all_job_details_df)
    else:
        print("Aucun détail d'offre d'emploi trouvé.")

    # Fusionner les deux DataFrames sur la colonne 'URL'
    emploi_df = pd.merge(df, all_job_details_df, on='URL')
    emploi_df = emploi_df.drop_duplicates()
    
    #df["URL"]=list(all_job_details_df["URL"])
    #df["Offre_Link"]=list(all_job_details_df["Offre_Link"])

    # Fonction pour extraire les informations d'une page
    def extract_information(url):
        try:
            response = requests.get(url, timeout=120)  # Augmentation du délai à 20 secondes
            response.raise_for_status()
            response.encoding = 'utf-8'

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extraction des informations sur l'entreprise
            company_info = soup.select_one('.job-ad-company')
            entreprise = {
                "Offre_Link" : url,
                'Nom': company_info.select_one('.company-title a').text.strip() if company_info and company_info.select_one('.company-title a') else None,
                'Secteur d´activité': ', '.join(item.text.strip() for item in company_info.select('.sector-title .field-item')) if company_info and company_info.select('.sector-title .field-item') else None,
                'Description de l\'entreprise': soup.select_one('.job-ad-company-description label + *').text.strip() if soup.select_one('.job-ad-company-description label + *') else None
            }

            # Extraction des informations sur l'annonce
            annonce_info = soup.select_one('.job-ad-details')
            annonce = {
                'Poste': soup.select_one('.ad-ss-title').text.strip() if soup.select_one('.ad-ss-title') else None,
                'Missions': [li.text.strip() for li in soup.select('.content ul.missions li')] if soup.select('.content ul.missions') else None,
                'Profil recherché': [li.text.strip() for li in soup.select('.content ul.profil li')] if soup.select('.content ul.profil') else None,
                'Métier': soup.select_one('.job-ad-criteria .field-name-field-offre-metiers .field-item').text.strip() if soup.select_one('.job-ad-criteria .field-name-field-offre-metiers .field-item') else None,
                'Secteur d´activité (de l\'annonce)': soup.select_one('.job-ad-criteria .field-name-field-offre-secteur .field-item').text.strip() if soup.select_one('.job-ad-criteria .field-name-field-offre-secteur .field-item') else None,
                'Type de contrat': soup.select_one('.job-ad-criteria .field-name-field-offre-contrat-type .field-item').text.strip() if soup.select_one('.job-ad-criteria .field-name-field-offre-contrat-type .field-item') else None,
                'Région': soup.select_one('.job-ad-criteria .field-name-field-offre-region .field-item').text.strip() if soup.select_one('.job-ad-criteria .field-name-field-offre-region .field-item') else None,
                'Ville': soup.select_one('.job-ad-criteria .field-name-field-offre-ville .field-item').text.strip() if soup.select_one('.job-ad-criteria .field-name-field-offre-ville .field-item') else None,
                'Niveau d\'expérience': soup.select_one('.job-ad-criteria .field-name-field-offre-niveau-experience .field-item').text.strip() if soup.select_one('.job-ad-criteria .field-name-field-offre-niveau-experience .field-item') else None,
                'Niveau d\'études': soup.select_one('.job-ad-criteria .field-name-field-offre-niveau-etude .field-item').text.strip() if soup.select_one('.job-ad-criteria .field-name-field-offre-niveau-etude .field-item') else None,
                'Compétences clés': [li.text.strip() for li in soup.select('.job-ad-criteria .field-name-field-offre-tags .field-item')] if soup.select('.job-ad-criteria .field-name-field-offre-tags .field-item') else None,
                'Nombre de poste(s)': soup.select_one('.job-ad-criteria td:contains("Nombre de poste(s) :") + td').text.strip() if soup.select_one('.job-ad-criteria td:contains("Nombre de poste(s) :") + td') else None,
            }

            return {'entreprise': entreprise, 'annonce': annonce}

        except (ConnectionError, ReadTimeout, ChunkedEncodingError) as e:
            print(f"Erreur lors de la requête {url}: {e}")
            # Relancer la requête
            entreprise = {
                "Offre_Link" : url,
                'Nom': "",
                'Secteur d´activité': "",
                'Description de l\'entreprise':""}
            annonce = {'Poste':"",
                       'Missions': "",
                       'Profil recherché':"",
                       'Métier':"",
                       'Secteur d´activité (de l\'annonce)':"",
                       'Type de contrat':"",
                       'Région': "",
                       'Ville':"",
                       'Niveau d\'expérience':"",
                       'Niveau d\'études':"",
                       'Compétences clés':"",
                       'Nombre de poste(s)':""}


            return {'entreprise': entreprise, 'annonce': annonce}

    # Liste des URLs
    urls = list(emploi_df['Offre_Link'])

    # Initialisation d'une liste pour stocker les DataFrames
    df_list = []

    # Boucle à travers chaque URL
    for url in urls:
        data = extract_information(url)

        # Si la requête a échoué, passez à l'URL suivante
        if data is None:
            continue

        # Création du DataFrame pour chaque URL
        df = pd.DataFrame([data['entreprise'] | data['annonce']])

        # Ajout du DataFrame à la liste
        df_list.append(df)

    # Concaténation des DataFrames de chaque URL
    result_df = pd.concat(df_list, ignore_index=True)
    # Ajouter les listes existantes en tant que colonnes au DataFrame
    result_df = pd.merge(result_df, emploi_df, on='Offre_Link')
    result_df = emploi_df.drop_duplicates()


# Réorganiser les colonnes selon vos besoins
#Poste 	Entreprise 	Date 	Description 	Région 	URL 	Offre_Link

    return result_df

