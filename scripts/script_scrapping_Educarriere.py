
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from selenium import webdriver
import urllib3
import time
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
#Importation du module d'envoi de mail
from selenium import webdriver
#from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import dateparser

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

