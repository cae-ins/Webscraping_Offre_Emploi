import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

def agence_emploi_jeunes():
    # Utilisation d'un en-tête pour éviter d'être bloqué
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Liste des URLs à scraper
    urls = ["https://agenceemploijeunes.ci/site/offres-emplois?page={}".format(category) for category in range(31)]

    # Listes pour stocker les données
    job_titles = []
    publication_dates = []
    application_deadlines = []
    locations = []
    job_descriptions = []
    job_types = []
    diploma_requirements = []
    url_lien = []

    # Loop à travers chaque URL
    for url in urls:
        # Envoyer une requête au site web
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')

        # Trouver les annonces d'emploi
        job_listings = soup.find_all('div', class_='post-bx')

        # Extract data from each job listing
        for job_listing in job_listings:
            url_lien.append(url)

            # Titre du poste
            job_title = job_listing.find('h4').text.strip()
            job_titles.append(job_title)

            # Dates de publication et de candidature
            date_info = job_listing.find_all('li', {'class': ''})
            if date_info:
                publication_date = date_info[0].text.replace('Publié le:', '').strip()
                application_deadline = date_info[1].text.replace('Date limite:', '').strip()
                publication_dates.append(publication_date)
                application_deadlines.append(application_deadline)

            # Localisation
            location = date_info[2].text.replace('ABENGOUROU', '').strip()
            locations.append(location)

            # Description du poste
            job_description = job_listing.find('p').text.strip()
            job_descriptions.append(job_description)

            # Type de poste
            job_type = job_listing.find('span', {'class': 'pull-right'}).text.strip()
            job_types.append(job_type)

            # Exigences en diplôme
            diploma_requirement = job_listing.find('div', {'class': 'salary-bx'}).text.strip()
            diploma_requirements.append(diploma_requirement)

    # Créer un DataFrame Pandas
    data = {
        'Job Title': job_titles,
        'Publication Date': publication_dates,
        'Application Deadline': application_deadlines,
        'Location': locations,
        'Job Description': job_descriptions,
        'Job Type': job_types,
        'Diploma Requirement': diploma_requirements,
        "URL": url_lien
    }

    df_agenceemploijeunes = pd.DataFrame(data)

    # Utiliser la méthode str.extract pour extraire la valeur après "Diplôme :"
    df_agenceemploijeunes['Diplome'] = df_agenceemploijeunes['Diploma Requirement'].str.extract(r'Diplôme :[ \t]([^\n\r])')

    # Scrapper les détails supplémentaires à partir des URL
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Pour exécuter le navigateur en arrière-plan
    options.add_argument("--disable-gpu")  # Désactiver l'accélération GPU en mode headless
    chrome_driver_path = 'C:\\Program Files (x86)\\chromedriver.exe'
    options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" 
    #C:\Program Files\Google\Chrome\Application# Remplacez par l'emplacement réel de votre Chrome binary
    options.add_argument(f"webdriver.chrome.driver={chrome_driver_path}")
    driver = webdriver.Chrome(options=options)

    # List to store job details
    all_job_details = []

    # Parcourir les liens
    for url in urls:
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        time.sleep(5)

        # Trouver toutes les offres d'emploi sur la page
        offer_links = soup.select('.post-bx h4 a')

        # Parcourir les liens d'offres
        for offer_link in offer_links:
            # Extraire l'URL de l'offre
            offer_url = offer_link.get('href')

            # Ajouter les détails à la liste
            all_job_details.append({'Offre_Link': offer_url, 'URL': url})

    # Fermer le navigateur à la fin
    driver.quit()

    # Créer un DataFrame avec les détails des offres d'emploi
    if all_job_details:
        all_job_details_df = pd.DataFrame(all_job_details)
    else:
        print("Aucun détail d'offre d'emploi trouvé.")

    # Fusionner les deux DataFrames sur la colonne 'URL'
    df_agenceemploi_jeunes = pd.merge(df_agenceemploijeunes, all_job_details_df, on='URL')
    df_agenceemploi_jeunes = df_agenceemploi_jeunes.drop_duplicates()
    df_agenceemploi_jeunes.reset_index(drop=True, inplace=True)

    # Création d'un dictionnaire pour stocker les données
    job_data = {
        'Job Title': [],
        'Location': [],
        'Reference': [],
        'Number of Positions': [],
        'Closing Date': [],
        'Diploma': [],
        'Job Type': [],
        'Experience': [],
        'Education Level': [],
        'Gender': [],
        'Job Description': [],
        'Offre_Link': []
    }

    # Loop through each URL
    for url in df_agenceemploi_jeunes["Offre_Link"]:
        offre_url = url  # Sauvegarder l'URL même en cas d'exception
        try:
            # Send a request to the website
            req = requests.get(url, headers=headers)
            req.raise_for_status()  # Raise an error for unsuccessful responses
            soup = BeautifulSoup(req.text, 'html.parser')

            # Extract job details
            job_details = soup.find('div', class_='widget_getintuch')

            if job_details:
                # Extract data from job details
                ul_element = job_details.find('ul')
                if ul_element:
                    details_list = ul_element.find_all('li')

                    # Initialize variables to store details
                    location = reference = num_positions = closing_date = diploma = job_type = experience = education_level = gender = None

                    # Iterate through details
                    for detail in details_list:
                        label = detail.find('strong')
                        value_span = detail.find('span', class_='text-black-light')

                        if label and value_span:
                            label_text = label.text.strip()
                            value_text = value_span.text.strip()

                            if 'Lieu de travail' in label_text:
                                location = value_text
                            elif 'Reference' in label_text:
                                reference = value_text
                            elif 'Nombre de poste' in label_text:
                                num_positions = value_text
                            elif 'Date de clôture' in label_text:
                                closing_date = value_text
                            elif 'Diplôme' in label_text:
                                diploma = value_text
                            elif 'Type de contrat' in label_text:
                                job_type = value_text
                            elif 'Expérience professionnelle' in label_text:
                                experience = value_text
                            elif 'Niveau d\'études' in label_text:
                                education_level = value_text
                            elif 'Sexe' in label_text:
                                gender = value_text

                    # Append extracted details to the dictionary
                    job_data['Location'].append(location)
                    job_data['Reference'].append(reference)
                    job_data['Number of Positions'].append(num_positions)
                    job_data['Closing Date'].append(closing_date)
                    job_data['Diploma'].append(diploma)
                    job_data['Job Type'].append(job_type)
                    job_data['Experience'].append(experience)
                    job_data['Education Level'].append(education_level)
                    job_data['Gender'].append(gender)

                # Extract job title and description
                job_title_element = soup.find('h3', {'class': 'title-head'})
                if job_title_element:
                    job_title = job_title_element.text.strip()
                    job_data['Job Title'].append(job_title)

                    job_description_info = soup.find('div', {'class': 'job-info-box'}).find('ul')
                    if job_description_info:
                        job_description_text = '\n'.join([li.text.strip() for li in job_description_info.find_all('li')])
                        job_data['Job Description'].append(job_description_text)
                    else:
                        job_data['Job Description'].append(None)
                else:
                    job_data['Job Title'].append(None)
                    job_data['Job Description'].append(None)
            else:
                job_data['Job Title'].append(None)
                job_data['Job Description'].append(None)

            # Append URL to the dictionary
            job_data['Offre_Link'].append(offre_url)

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while accessing URL: {url}")
            print(e)
            # Ajouter l'URL même en cas d'exception
            job_data['Location'].append(None)
            job_data['Reference'].append(None)
            job_data['Number of Positions'].append(None)
            job_data['Closing Date'].append(None)
            job_data['Diploma'].append(None)
            job_data['Job Type'].append(None)
            job_data['Experience'].append(None)
            job_data['Education Level'].append(None)
            job_data['Gender'].append(None)
            job_data['Job Title'].append(None)
            job_data['Job Description'].append(None)
            job_data['Offre_Link'].append(offre_url)

    # Create DataFrame from the collected data
    df_jobs = pd.DataFrame(job_data)
    agenceemploi_jeunes_df = pd.merge(df_agenceemploi_jeunes, df_jobs, on='Offre_Link')
    agenceemploi_jeunes_dfagenceemploi_jeunes_df = agenceemploi_jeunes_df.drop_duplicates()
    agenceemploi_jeunes_df.reset_index(drop=True, inplace=True)
    equivalences = {
    "Job Title_x": "INTITULE_DU_POSTE",
    "Publication Date": "DATE_DE_PUBLICATION",
    "Application Deadline": None,
    "Location_x": "LIEU_DU_POSTE_DE_TRAVAIL",
    "Job Description_x": "DESCRIPTION_DU_POSTE",
    "Job Type_x": "TYPE_DE_CONTRAT_DU_POSTE",
    "Diploma Requirement": None,
    "URL": None,
    "Diplome": "DIPLOME_REQUIS",
    "Offre_Link": "SITE_WEB_DE_L_ENTREPRISE",
    # Colonnes sans équivalence
    "Location_y": None,
    "Reference": None,
    "Number of Positions": "NOMBRE_DE_POSTES_A_POURVOIR",
    "Closing Date": "DATE_D_EXPIRATION_DE_L_OFFRE",
    "Diploma": "DIPLOME",
    "Job Type_y": None,
    "Experience": None,
    "Education Level": "NIVEAU_D_ETUDES",
    "Gender": None,
    "Job Description_y": None}
    def renommer_colonnes(df, equivalences):
        colonnes_renommees = {ancien_nom: nouvel_nom for ancien_nom, nouvel_nom in equivalences.items() if nouvel_nom is not None}
        df_renomme = df.rename(columns=colonnes_renommees)
        return df_renomme
    agenceemploi_jeunes_df = renommer_colonnes(agenceemploi_jeunes_df, equivalences)
    
    return agenceemploi_jeunes_df
