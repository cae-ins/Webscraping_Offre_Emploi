#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
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


def collect_job_info(url):
    try:
        # Envoyer une requête GET à l'URL spécifiée
        response = requests.get(url)
        
        # Vérifier si la requête a réussi
        if response.status_code == 200:
            # Utiliser BeautifulSoup pour analyser le contenu HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extracting job title
            job_title = soup.find('h3', class_='title').text.strip()
            
            # Extracting author
            author = soup.find('div', class_='info').find('li').text.strip()
            
            # Extracting date posted
            date_posted = soup.find('div', class_='info').find_all('li')[1].text.strip()
            
            # Extracting description
            description = soup.find('div', class_='content').p.text.strip()
            
            # Extracting post URL
            post_url = url
            
            # Return job data as a dictionary encapsulated in a list
            job_data = [{
                'Job Title': job_title,
                'Author': author,
                'Date Posted': date_posted,
                'Description': description,
                'Post URL': post_url
            }]
            
            return job_data
        else:
            print("Failed to fetch the page.")
            return []
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []

def scrape_additional_details(urls):
    # Initialiser une liste pour stocker les données
    job_data = []
    
    # Configurer Selenium pour s'exécuter en mode headless (sans ouvrir de fenêtre de navigateur)
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Boucle à travers chaque URL
    for url in urls:
        try:
            # Initialiser le pilote Selenium
            driver = webdriver.Chrome(options=chrome_options)

            # Envoyer une requête GET en utilisant Selenium
            driver.get(url)

            # Attendre quelques secondes (ajustez selon les besoins)
            time.sleep(30)

            # Attendre que la page soit entièrement chargée
            WebDriverWait(driver, 10).until(
                lambda x: x.execute_script("return document.readyState === 'complete'")
            )

            # Récupérer le code source de la page après l'exécution de JavaScript
            page_source = driver.page_source

            # Fermer le pilote Selenium
            driver.quit()

            # Utiliser BeautifulSoup pour analyser le HTML
            soup = BeautifulSoup(page_source, 'html.parser')

            # Extraire les détails de l'offre d'emploi
            job_title_element = soup.find('h1', class_='entry-title')
            job_title = job_title_element.text.strip() if job_title_element else None

            author_container = soup.find('div', class_='info')
            author_element = author_container.find_all('li')[0] if author_container else None
            author = author_element.text.strip() if author_element else None

            date_container = soup.find('div', class_='info')
            date_element = date_container.find_all('li')[1] if date_container else None
            date_posted = date_element.text.strip() if date_element else None

            views_element = soup.find('div', class_='td-post-views')
            views = views_element.find('span', class_='td-nr-views-19100').text.strip() if views_element and views_element.find('span', class_='td-nr-views-19100') else None

            image_url_element = soup.find('div', class_='td-post-featured-image')
            image_url = image_url_element.find('img')['src'] if image_url_element and image_url_element.find('img') else None

            # Ajouter les détails à la liste
            job_data.append({
                'Job_Title': job_title,
                'Author1': author,
                'Date Posted1': date_posted,
                'Views': views,
                'Image URL': image_url,
                'URL': url
            })
        except Exception as e:
            print(f"Une erreur s'est produite pour l'URL {url}: {str(e)}")
            job_data.append({
                'Job_Title': "",
                'Author1': "",
                'Date Posted1': "",
                'Views': "",
                'Image URL': "",
                'URL': url
            })

    return job_data
def alerte_emploi():
    # Liste des URLs des offres d'emploi
    job_listing_urls = [
        #"https://alerteemploi.net/toutes-les-offres/",
        "https://alerteemploi.net/category/emploi-stages/page/{}/".format(category) for category in range(52) #
        # Ajoutez d'autres URLs au besoin
    ]

    # Récupérer les informations initiales des offres d'emploi
    initial_job_info = []
    for url in job_listing_urls:
        initial_job_info.extend(collect_job_info(url))
    initial_job_info1 = pd.DataFrame(initial_job_info) 
   



    # Extraire les URLs des offres d'emploi
    urls = [job['Post URL'] for job in initial_job_info if isinstance(job, dict)]
    #[job['Post URL'] for job in initial_job_info if job]

    # Récupérer les détails supplémentaires des offres d'emploi en utilisant Selenium
    additional_job_info = scrape_additional_details(urls)
    additional_job_info = pd.DataFrame(additional_job_info) 
    

    # Fusionner les informations initiales et supplémentaires
    df = pd.merge( initial_job_info1,additional_job_info, on='Post URL')
    df = df.drop_duplicates()
    df.reset_index(drop=True, inplace=True) 
    return df
