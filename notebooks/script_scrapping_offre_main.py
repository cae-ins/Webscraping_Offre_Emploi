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
import os
#Importation du module d'envoi de mail
from send_mail_offre import send_mail_success_offre, send_mail_error_offre

import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
#from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By


import dateparser

import os
RECEIVERS = ['2250779535153']
def send_sms(msg: str, title: str="Offre d'emploi disponible sur le web", receivers: list=RECEIVERS):
    # msg += " Priere de mener des actions"
    msg = msg.replace(' ', '+')
    for receiver in receivers:
        os.system(f'''curl -X GET "http://10.1.60.190:9802/dispatcher/httpconnectserver/smsaffaires.jsp?UserName=application_smsaffaires_sva&Password=sva&SenderAppId=1&DA={receiver}&SOA={title}&Flags=264192&Content={msg}"''')


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

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
import urllib3

def emploi_educarriere():
    # Ignorer les avertissements SSL
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
    # Fonction pour extraire le texte d'un élément HTML
    def extract_text(element, class_name=None, style=None, text_contains=None):
        if element:
            tag = element.find(class_=class_name, style=style, text=text_contains)
            return tag.text.strip() if tag else ""
        else:
            return ""

    # Fonction pour nettoyer le texte
    def clean_text(text):
        if text is not None:
            cleaned_text = text.replace('D\x92', ' ').replace('d\x92', ' ').replace('\x92', ' ').replace('\r\n', '').replace('\xa0', '')
            return cleaned_text.strip() if cleaned_text else None
        else:
            return None

    # Fonction pour extraire la date à partir d'un élément HTML
    def extract_date(element, text_contains):
        date_elements = element.find_all('a', class_='text')
        date = next((e.find('span', style='color:#FF0000;').text.strip() for e in date_elements if text_contains in e.text), "")
        return date

    # Fonction pour extraire les détails des offres d'emploi
    def scrap_job_details(urls):
        # En-tête pour éviter d'être bloqué
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        options = webdriver.ChromeOptions()
        #options.add_argument("--headless")  # Pour exécuter le navigateur en arrière-plan
        #options.add_argument("--disable-gpu")  # Désactiver l'accélération GPU en mode headless
        chrome_driver_path = 'C:\\Program Files (x86)\\chromedriver.exe'
        options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"  # Remplacez par l'emplacement réel de votre Chrome binary
        options.add_argument(f"webdriver.chrome.driver={chrome_driver_path}")
        driver = webdriver.Chrome(options=options)

        # Liste pour stocker les détails de chaque emploi
        all_job_details = []

        # Parcourir les liens
        for url in urls:
            req = requests.get(url, headers=headers)
            soup = BeautifulSoup(req.text, 'html.parser')
            time.sleep(5)  # Attendre 5 secondes avant la prochaine requête

            offres = soup.find_all('div', class_='box row')

            # Parcourir les offres d'emploi sur la page principale
            for offre in offres:
                # Trouver la balise <h4> dans la structure HTML pour extraire le lien
                offre_link_tag = offre.find('h4')

                # Vérifier si la balise <h4> a été trouvée
                if offre_link_tag:
                    # Extraire le lien de l'attribut 'href'
                    offre_link = offre_link_tag.find('a')['href']
                    all_job_details.append({'Offre_Link': offre_link})

        # Fermer le pilote Selenium à la fin
        driver.quit()

        # Concaténer tous les détails des emplois en un seul DataFrame
        if all_job_details:
            all_job_details_df = pd.DataFrame(all_job_details)
            return all_job_details_df
        else:
            print("Aucun détail d'offre d'emploi trouvé.")
            return None

    # Fonction pour récupérer les données des offres d'emploi
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
                'Poste': clean_text(poste),
                'Sous_titre': sous_titre,
                'Code': clean_text(code),
                'Date_DEdition': date_edition,
                'Date_limite': date_limite,
                'Pays': clean_text(pays),
                'URL': url  # Ajout de la colonne 'URL'
            })

        df = pd.DataFrame(data_list)
        return df

    # Fonction pour ajouter la colonne 'Offre_Link' à un DataFrame existant
    def add_offre_link_column(result_df):
        job_details_df = scrap_job_details(list(result_df["URL"]))
        if job_details_df is not None:
            # Join des DataFrames
            result_df = pd.concat([result_df, job_details_df], axis=1)
            return result_df
        else:
            print("Impossible d'ajouter la colonne 'Offre_Link' au DataFrame.")
            return None

    # Fonction pour extraire les informations de l'offre d'emploi
    def extract_job_information(soup, url):
        try:
            # Extraction des informations de l'offre d'emploi
            poste = soup.select_one('li.list-group-item:-soup-contains("Poste")').strong.next_sibling.strip()
            type_offre = soup.select_one('li.list-group-item:-soup-contains("Type d\'offre")').strong.next_sibling.strip()
            metiers = soup.select_one('li.list-group-item:-soup-contains("Métier(s):")').strong.next_sibling.strip()
            niveaux = soup.select_one('li.list-group-item:-soup-contains("Niveau(x):")').strong.next_sibling.strip()
            experience = soup.select_one('li.list-group-item:-soup-contains("Expérience:")').strong.next_sibling.strip()
            lieu = soup.select_one('li.list-group-item:-soup-contains("Lieu:")').strong.next_sibling.strip()
            
            # Extraction des dates de publication et de limite
            date_publication = soup.find('strong', string='Date de publication:').find_next('span').text.strip()
            date_limite = soup.find('strong', string='Date limite:').find_next('span').text.strip()
            
            # description = soup.select_one('div.text-col.post.small-post.col-md-9.col-xs-12 ul.list-group').text.strip()
            description = soup.select_one('div.entry-content').text.strip()

            return {
                "Poste": [poste],
                "Type d'offre": [type_offre],
                "Métier(s)": [metiers],
                "Niveau(x)": [niveaux],
                "Expérience": [experience],
                "Lieu": [lieu],
                "Offre_Link": [url],
                "Date de publication": [date_publication],
                "Date limite": [date_limite],
                "Description": [description]
            }
        except Exception as e:
            print(f"An error occurred while extracting job information for URL {url}: {e}")
            # Retourner un dictionnaire avec l'URL en cas d'erreur
            return {"Offre_Link": [url]}

    # Liste des liens
    urls = ["https://emploi.educarriere.ci/nos-offres?page1={}&codes=&mots_cles=&typeemploi1=&niveau1=&anciennete=&typeoffre1=&recruteur=".format(category) for category in range(30)]

    # Créer un DataFrame à partir des liens
    result_df = pd.concat([scrape_emploi_ci(url) for url in urls], ignore_index=True)

    # Ajouter la colonne 'Offre_Link'
    result_df = add_offre_link_column(result_df)
    # Supprimer les lignes avec plus de 80% de valeurs NaN
    threshold = int(result_df.shape[1] * 0.8)  # 80% des colonnes
    result_df = result_df.dropna(thresh=threshold)
    result_df = result_df.reset_index(drop=True)
    
    # Liste des URLs à scraper
    urls = list(result_df['Offre_Link'])

    # Liste pour stocker les DataFrames
    dfs = []

    # Boucle sur chaque URL
    for url in urls:
        try:
            # Envoyer une requête GET au site avec un délai de 120 secondes
            response = requests.get(url, headers=headers, verify=True, timeout=120)

            # Vérifier si la requête a réussi (statut 200)
            if response.status_code == 200:
                # Analyser le contenu de la page avec BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extraire les informations sur l'emploi
                job_info = extract_job_information(soup, url)

                # Créer un DataFrame
                df = pd.DataFrame(job_info)

                # Ajouter le DataFrame à la liste
                dfs.append(df)
            else:
                print(f"Échec de la requête pour l'URL {url}. Statut : {response.status_code}")
                # Ajouter une ligne avec l'URL en cas d'erreur
                dfs.append(pd.DataFrame({"Offre_Link": [url]}))

        except requests.exceptions.Timeout:
            print(f"Timeout lors de la requête pour l'URL {url}")
            # Ajouter une ligne avec l'URL en cas d'erreur
            dfs.append(pd.DataFrame({"Offre_Link": [url]}))
        except requests.exceptions.RequestException as e:
            print(f"Une erreur s'est produite lors de la requête pour l'URL {url}: {e}")
            # Ajouter une ligne avec l'URL en cas d'erreur
            dfs.append(pd.DataFrame({"Offre_Link": [url]}))

        # Ajouter un délai de 5 secondes entre les requêtes pour éviter d'être bloqué
        time.sleep(5)

    # Concaténer tous les DataFrames en un seul DataFrame
    df_Educarriere = pd.concat(dfs, ignore_index=True)

    # Ajouter les listes existantes en tant que colonnes au DataFrame
    df_Educarriere = pd.merge(df_Educarriere, result_df, on='Offre_Link')
    df_Educarriere = df_Educarriere.drop_duplicates()
    df_Educarriere.reset_index(drop=True, inplace=True)
    
    equivalences = {
    "Poste_y": "INTITULE_DU_POSTE",
    "Type d'offre": "TYPE_DE_CONTRAT_DU_POSTE",
    "Métier(s)": "SPECIALITE",
    "Niveau(x)": "DIPLOME",
    "Expérience": "EXPERIENCE_PROFESSIONNELLE",
    "Lieu": "LIEU_DU_POSTE_DE_TRAVAIL",
    "Offre_Link": "SITE_WEB_DE_L_ENTREPRISE",
    "Date de publication": "DATE_DE_DEBUT_DE_L_OFFRE",
    "Date limite": "DATE_D_EXPIRATION_DE_L_OFFRE",
    "Poste_x": "BRANCHE_D_ACTIVITE",
    "Description": None,
    "Sous_titre": None,
    "Code": None,
    "Date_DEdition": None,
    "Date_limite": None,
    "Pays": "PAYS_DU_POSTE_DE_TRAVAIL"}
    # Fonction pour renommer les colonnes du DataFrame en conservant les colonnes sans équivalence
    def renommer_colonnes(df, equivalences):
        colonnes_renommees = {ancien_nom: nouvel_nom for ancien_nom, nouvel_nom in equivalences.items() if nouvel_nom is not None}
        df_renomme = df.rename(columns=colonnes_renommees)
        return df_renomme
    
    
    # Renommer les colonnes du DataFrame
    df_Educarriere = renommer_colonnes(df_Educarriere, equivalences)
    df_Educarriere[["EXPERIENCE_PROFESSIONNELLE", 'Unite_EXPERIENCE_PROFESSIONNELLE']] = df_Educarriere["EXPERIENCE_PROFESSIONNELLE"].str.extract(r"([0-9]+)\s*([a-zA-Z]+)")


    # Réorganiser les colonnes selon vos besoins
    # Vous pouvez réorganiser les colonnes ici

    # Afficher ou retourner le DataFrame selon votre besoin
    return df_Educarriere

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re

from selenium import webdriver

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

# Appel de la fonction pour obtenir le DataFrame


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
import requests
from bs4 import BeautifulSoup
import pandas as pd

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

# Liste des URLs des pages d'offres d'emploi
urls_rmo = [
    "https://rmo-jobcenter.com/fr/nos-offres-emploi.html",
    # Ajoutez d'autres URLs au besoin
]

# Appel de la fonction pour récupérer les données





# Appeler la fonction rmo_jobcenter pour obtenir le DataFrame combiné
rmo_jobcenter_df = rmo_jobcenter(urls_rmo)

# Afficher le DataFrame combiné
 
rmo_jobcenter_df[['candidature','Data_cloture']] = rmo_jobcenter_df['SOUS_POSTE'].str.split('-', n=1, expand=True)
rmo_jobcenter_df.drop(columns=['candidature'], inplace=True)
# Fonction de nettoyage pour extraire uniquement la date
def clean_date(date_str):
    return date_str.split('expire le ')[1].strip() if isinstance(date_str, str) else date_str

# Appliquer la fonction de nettoyage à toute la colonne 'Data_cloture'
rmo_jobcenter_df['Data_cloture'] = rmo_jobcenter_df['Data_cloture'].apply(clean_date)

# Afficher le DataFrame après nettoyage


# Liste des URLs à analyser
detail_urls = list(rmo_jobcenter_df['DETAILS_URL'])

# Initialiser une liste pour stocker les données extraites de chaque URL
data_list = []

# Boucle sur chaque URL dans la liste
for detail_url in detail_urls:
    try:
        # Envoyer une requête GET pour récupérer le contenu de la page
        response = requests.get(detail_url)

        # Vérifier si la requête a réussi (code 200)
        if response.status_code == 200:
            # Extraire le contenu HTML
            html = response.text

            # Analyser la structure HTML avec BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')

            # Extraire les informations de la page
            informations = {'DETAILS_URL': detail_url}

            # Extraire le poste s'il existe
            poste_element = soup.find('h4', text='Le Poste')
            if poste_element:
                poste = poste_element.find_next('div').get_text(strip=True)
                informations['Le Poste'] = poste

            # Extraire le profil du candidat s'il existe
            profil_element = soup.find('h4', text='Profil du Candidat')
            if profil_element:
                profil_candidat = profil_element.find_next('div').get_text(strip=True)
                informations['Profil du Candidat'] = profil_candidat

            # Extraire les critères client s'ils existent
            critere_client_element = soup.find('h6', class_='le_grd_titre', text='Critères Client')
            if critere_client_element:
                critere_client_rows = critere_client_element.find_next('tbody').find_all('tr')
                critere_client = {row.find('th').get_text(strip=True): row.find('td').get_text(strip=True) for row in critere_client_rows}
                informations.update(critere_client)
            else:
                print(f"Les critères client n'ont pas été trouvés sur la page : {detail_url}")

            # Extraire les autres informations
            autres_informations_element = soup.find('h4', text='Autres Informations')
            if autres_informations_element:
                autres_informations_rows = autres_informations_element.find_next('tbody').find_all('tr')
                autres_informations = {row.find('th').get_text(strip=True): row.find('td').get_text(strip=True) for row in autres_informations_rows}
                informations.update(autres_informations)

            # Ajouter les informations extraites à la liste
            data_list.append(informations)
        else:
            print(f"La requête GET a échoué pour l'URL : {detail_url}")

    except Exception as e:
        print(f"Une erreur s'est produite lors de l'analyse de l'URL {detail_url}: {str(e)}")

# Créer un DataFrame pandas à partir des informations extraites
data = pd.DataFrame(data_list)

# Afficher le DataFrame

data['Postes Disponibles :']=data['Postes Disponibles :'].str.extract(r"([0-9,]+)")
data[['annee_min', 'annee_max']] = data['Années d\'Expérience :'].str.extract(r'(\d+)\-\s*(\d+)\s*ans?')

# Remplir les valeurs manquantes dans annee_min avec les valeurs extraites de Année d'Expérience Requise
data['annee_min'].fillna(data['Années d\'Expérience :'], inplace=True)  # Remplissage des valeurs manquantes dans la colonne 'annee_min' avec les valeurs d'origine
data['annee_max'].fillna(data['Années d\'Expérience :'], inplace=True)  # Remplissage des valeurs manquantes dans la colonne 'annee_max' avec les valeurs d'origine
# Extraire uniquement les chiffres de chaque colonne
data['annee_min'] = data['annee_min'].str.extract(r"([0-9,]+)")  # Extraction des chiffres de la colonne 'annee_min'
data['annee_max'] = data['annee_max'].str.extract(r"([0-9,]+)")  # Extraction des chiffres de la colonne 'annee_max'
data[["VILLE_DU_POSTE_DE_TRAVAIL", "DU_POSTE_DE_TRAVAIL","PAYS_DU_POSTE_DE_TRAVAIL"]] = data['Localisation :'].str.split('-', expand=True)

for i in range(len(data["PAYS_DU_POSTE_DE_TRAVAIL"])):
    if data["PAYS_DU_POSTE_DE_TRAVAIL"][i] is None :
        data["PAYS_DU_POSTE_DE_TRAVAIL"][i]=data["DU_POSTE_DE_TRAVAIL"][i]
    if data["PAYS_DU_POSTE_DE_TRAVAIL"][i] != data["DU_POSTE_DE_TRAVAIL"][i]:
        ville = str(data["VILLE_DU_POSTE_DE_TRAVAIL"][i])  # Convertir en str pour éviter les problèmes de type
        du_poste = str(data["DU_POSTE_DE_TRAVAIL"][i])
        data["VILLE_DU_POSTE_DE_TRAVAIL"][i] = ville + " - " + du_poste    

#Supprimer la colonne 
data.drop(columns=["DU_POSTE_DE_TRAVAIL"], inplace=True)
# Affichage du DataFrame résultant
#data
  # Affichage du DataFrame résultant
rmo_jobcenter_df = pd.merge(data,rmo_jobcenter_df, on='DETAILS_URL')
rmo_jobcenter_df = rmo_jobcenter_df.drop_duplicates()
rmo_jobcenter_df.reset_index(drop=True, inplace=True)

chemin_fichier_rmo_jobcenter_df = os.path.join('C:/Users/Dell/Documents/UB/IPC/CODE_IPC/COLLECTE_JOURNALIERE_offre_emploi','Data_Scrapping_rmo_jobcenter_df_'+datetime.now().strftime('%d%m%Y')+'.xlsx')
rmo_jobcenter_df.to_excel(chemin_fichier_rmo_jobcenter_df, index=False)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

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

# Appel de la fonction principale
yop_l_frii= yop_l_frii()
yop_l_frii['INTITULE_DU_POSTE'] = yop_l_frii['INTITULE_DU_POSTE'].str.replace(r'[()]', '')

# Utilisation de str.extract() pour extraire les parties de la chaîne
yop_l_frii['DATE_DE_DEBUT_DE_L_OFFRE'] = yop_l_frii['INTITULE_DU_POSTE'].str.extract(r'(\d+\s\w+\s\d+)$')



# Remplacer la partie extraite par une chaîne vide pour obtenir INTITULE_DU_POSTE
yop_l_frii['INTITULE_DU_POSTE'] = yop_l_frii['INTITULE_DU_POSTE'].str.replace(r'(\d+\s\w+\s\d+)$', '')
yop_l_frii['NOMBRE_DE_POSTE_DE_TRAVAIL'] = yop_l_frii['INTITULE_DU_POSTE'].str.extract(r'(\d+)\s*postes')



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

# Liste des URLs
urls = list(yop_l_frii["URL_DU_POSTE"])

# Extraire les informations sur les emplois à partir des URLs
df = extract_job_info_from_urls(urls)

# Afficher le DataFrame
# Utilisation de str.extract() pour extraire les nombres min et max
extracted_data = df['Année d\'Expérience Requise'].str.extract(r'(\d+)\s*ans,\s*(\d+)\s*ans?')  # Extraction des années min et max

# Renommer les colonnes extraites
extracted_data.columns = ['annee_min', 'annee_max']  # Renommage des colonnes extraites

# Remplir les valeurs manquantes dans annee_min avec les valeurs extraites de Année d'Expérience Requise
extracted_data['annee_min'].fillna(df["Année d'Expérience Requise"], inplace=True)  # Remplissage des valeurs manquantes dans la colonne 'annee_min' avec les valeurs d'origine
extracted_data['annee_max'].fillna(df["Année d'Expérience Requise"], inplace=True)  # Remplissage des valeurs manquantes dans la colonne 'annee_max' avec les valeurs d'origine

# Extraire uniquement les chiffres de chaque colonne
extracted_data['annee_min'] = extracted_data['annee_min'].str.extract(r"([0-9,]+)")  # Extraction des chiffres de la colonne 'annee_min'
extracted_data['annee_max'] = extracted_data['annee_max'].str.extract(r"([0-9,]+)")  # Extraction des chiffres de la colonne 'annee_max'

# Ajouter les colonnes extraites au DataFrame d'origine
df = pd.concat([df, extracted_data], axis=1)  # Ajout des colonnes extraites au DataFrame d'origine

# Affichage du DataFrame résultant
# Diviser la colonne 'Lieu du Travail' en ville et pays
df[['LIEU_DU_POSTE_DE_TRAVAIL', 'PAYS_DU_POSTE_DE_TRAVAIL']] = df['Lieu du Travail'].str.split(', ', n=1, expand=True)

for i in range(len(df["PAYS_DU_POSTE_DE_TRAVAIL"])):
    if df["PAYS_DU_POSTE_DE_TRAVAIL"][i] is None :
        df["PAYS_DU_POSTE_DE_TRAVAIL"][i] = df["LIEU_DU_POSTE_DE_TRAVAIL"][i]
yop_l_frii_total = pd.merge(yop_l_frii,df, on='URL_DU_POSTE')
yop_l_frii_total = yop_l_frii_total.drop_duplicates()
yop_l_frii_total.reset_index(drop=True, inplace=True)
yop_l_frii_total  # Affichage du DataFrame résultant
chemin_fichier_yop_l_frii_total = os.path.join('C:/Users/Dell/Documents/UB/IPC/CODE_IPC/COLLECTE_JOURNALIERE_offre_emploi','Data_Scrapping_yop_l_frii_total_'+datetime.now().strftime('%d%m%Y')+'.xlsx')
yop_l_frii_total.to_excel(chemin_fichier_yop_l_frii_total, index=False)

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

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

# Appel de la fonction principale

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
import requests
from bs4 import BeautifulSoup
import pandas as pd

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

# --------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

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

# Appeler la fonction projobivoire pour obtenir le DataFrame des offres d'emploi


#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------

try:

# Appel de la fonction principale
#Exportation de la donnée Finale
    df_novojob = scrap_novojob()
    chemin_fichier_df_novojob = os.path.join('C:/Users/Dell/Documents/UB/IPC/CODE_IPC/COLLECTE_JOURNALIERE_offre_emploi','Data_Scrapping_df_novojob_'+datetime.now().strftime('%d%m%Y')+'.xlsx')
    df_novojob.to_excel(chemin_fichier_df_novojob, index=False)

    emploi_df=emploi_ci()
    emploi_df.reset_index(drop=True, inplace=True)
    chemin_fichier_emploi_df = os.path.join('C:/Users/Dell/Documents/UB/IPC/CODE_IPC/COLLECTE_JOURNALIERE_offre_emploi','Data_Scrapping_emploi_df_'+datetime.now().strftime('%d%m%Y')+'.xlsx')
    emploi_df.to_excel(chemin_fichier_emploi_df, index=False)

    mondiale_df=mondiale_ci()
    chemin_fichier_mondiale_df = os.path.join('C:/Users/Dell/Documents/UB/IPC/CODE_IPC/COLLECTE_JOURNALIERE_offre_emploi','Data_Scrapping_mondiale_df_'+datetime.now().strftime('%d%m%Y')+'.xlsx')
    mondiale_df.to_excel(chemin_fichier_mondiale_df, index=False)


    df_talent_ci = talent_ci()
    chemin_fichier_df_talent_ci = os.path.join('C:/Users/Dell/Documents/UB/IPC/CODE_IPC/COLLECTE_JOURNALIERE_offre_emploi','Data_Scrapping_df_talent_ci_'+datetime.now().strftime('%d%m%Y')+'.xlsx')
    df_talent_ci.to_excel(chemin_fichier_df_talent_ci, index=False)

    df_projobivoire = projobivoire()
    chemin_fichier_df_projobivoire = os.path.join('C:/Users/Dell/Documents/UB/IPC/CODE_IPC/COLLECTE_JOURNALIERE_offre_emploi','Data_Scrapping_df_projobivoire_'+datetime.now().strftime('%d%m%Y')+'.xlsx')
    df_projobivoire.to_excel(chemin_fichier_df_projobivoire, index=False)

    
    send_mail_success_offre(["abdoulayebakayoko265@gmail.com", "doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci","moussakr@gmail.com"])
    #send_sms(f"le fichier {'Data_Scrapping_offre_'+datetime.now().strftime('%d%m%Y')+'.xlsx'} a été deposé avec succès.")

except Exception as e:

    print("Il y a une erreur dans le code principal:", e)

    send_mail_error_offre(["doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci"])
    #send_sms(f"Il y a une erreur dans le code principal", e )

try:

# Appel de la fonction principale
#Exportation de la donnée Finale

    df_educarriere = emploi_educarriere()
    chemin_fichier_df_educarriere = os.path.join('C:/Users/Dell/Documents/UB/IPC/CODE_IPC/COLLECTE_JOURNALIERE_offre_emploi','Data_Scrapping_df_educarriere_'+datetime.now().strftime('%d%m%Y')+'.xlsx')
    df_educarriere.to_excel(chemin_fichier_df_educarriere, index=False)

    df_final = pd.concat([df_novojob, df_educarriere,rmo_jobcenter_df], axis=0, ignore_index=True)
    chemin_fichier_collecte = os.path.join('C:/Users/Dell/Documents/UB/IPC/CODE_IPC/COLLECTE_JOURNALIERE_offre_emploi','Data_Scrapping_offre_'+datetime.now().strftime('%d%m%Y')+'.xlsx')
    df_final.to_excel(chemin_fichier_collecte, index=False)

    

    send_mail_success_offre(["abdoulayebakayoko265@gmail.com", "doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci","moussakr@gmail.com"])
    #send_sms(f"le fichier {'Data_Scrapping_offre_'+datetime.now().strftime('%d%m%Y')+'.xlsx'} a été deposé avec succès.")

except Exception as e:

    print("Il y a une erreur dans le code principal:", e)

    send_mail_error_offre(["doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci"])
    #send_sms(f"Il y a une erreur dans le code principal", e )
