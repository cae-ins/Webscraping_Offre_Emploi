import time
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import os
#Importation du module d'envoi de mail
from script_scrapping_agenceemploi import agence_emploi_jeunes # type: ignore
from send_mail_offre import send_mail_success_offre, send_mail_error_offre
from script_scrapping_Novojob import scrap_novojob
from script_scrapping_Educarriere import emploi_educarriere
from script_scrapping_Alerte_emploi import alerteemploi
from script_scrapping_Emploi_ci import emploi_ci
from script_scrapping_Projobivoire import projobivoire
from script_scrapping_Mondiale_df import mondiale_ci
from script_scrapping_Rmo_jobcenter_df import rmo_jobcenter
from script_scrapping_Talent_ci import talent_ci
from script_scrapping_Yop_l_frii import extract_job_information, extract_job_info_from_urls, yop_l_frii
from script_fonction_doublon import preprocess_text, doublon

from selenium import webdriver
#from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By

##-----------------------------------------------------------------------------------------------------------
##-----------------------------------------------------------------------------------------------------------
# NOVOJOB

try:

# Appel de la fonction principale
#Exportation de la donnée Finale

    # Appel de la fonction principale
#Exportation de la donnée Finale
    df_novojob = scrap_novojob()
    chemin_fichier_df_novojob = os.path.join('C:/Users/Dell/Documents/UB/IPC/CODE_IPC/COLLECTE_JOURNALIERE_offre_emploi','Data_Scrapping_df_novojob_'+datetime.now().strftime('%d%m%Y')+'.xlsx')
    df_novojob.to_excel(chemin_fichier_df_novojob, index=False)
    

    send_mail_success_offre(["abdoulayebakayoko265@gmail.com", "doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci","moussakr@gmail.com"])
    #send_sms(f"le fichier {'Data_Scrapping_offre_'+datetime.now().strftime('%d%m%Y')+'.xlsx'} a été deposé avec succès.")

except Exception as e:

    print("Il y a une erreur dans le code principal:", e)

    send_mail_error_offre(["doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci"])
    #send_sms(f"Il y a une erreur dans le code principal", e )

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------   

# Educarriere
try:

# Appel de la fonction principale
#Exportation de la donnée Finale

    df_educarriere = emploi_educarriere()
    chemin_fichier_df_educarriere = os.path.join('C:/Users/Dell/Documents/UB/IPC/CODE_IPC/COLLECTE_JOURNALIERE_offre_emploi','Data_Scrapping_df_educarriere_'+datetime.now().strftime('%d%m%Y')+'.xlsx')
    df_educarriere.to_excel(chemin_fichier_df_educarriere, index=False)


    send_mail_success_offre(["abdoulayebakayoko265@gmail.com", "doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci","moussakr@gmail.com"])
    #send_sms(f"le fichier {'Data_Scrapping_offre_'+datetime.now().strftime('%d%m%Y')+'.xlsx'} a été deposé avec succès.")

except Exception as e:

    print("Il y a une erreur dans le code principal:", e)

    send_mail_error_offre(["doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci"])
    #send_sms(f"Il y a une erreur dans le code principal", e )
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Alerte_emploi
equivalences = {
'Job Title': 'INTITULE_DU_POSTE',
'Date Posted': 'DATE_DE_DEBUT_DE_L_OFFRE',
'Description': 'Description',
'URL': 'URL',
'Post URL': 'Post URL',
    }
    # Fonction pour renommer les colonnes du DataFrame en conservant les colonnes sans équivalence
def renommer_colonnes(df, equivalences):
    colonnes_renommees = {ancien_nom: nouvel_nom for ancien_nom, nouvel_nom in equivalences.items() if nouvel_nom is not None}
    df_renomme = df.rename(columns=colonnes_renommees)
    return df_renomme
    
try:

    alerte_emploi_df = alerteemploi()
    alerte_emploi_df=renommer_colonnes(alerte_emploi_df, equivalences)
    alerte_emploi_df.reset_index(drop=True, inplace=True)
    chemin_fichier_alerte_emploi_df = os.path.join('C:/Users/Dell/Documents/UB/IPC/CODE_IPC/COLLECTE_JOURNALIERE_offre_emploi','Data_Scrapping_emploi_df_'+datetime.now().strftime('%d%m%Y')+'.xlsx')
    alerte_emploi_df.to_excel(chemin_fichier_alerte_emploi_df, index=False)

    send_mail_success_offre(["abdoulayebakayoko265@gmail.com", "doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci","moussakr@gmail.com"])
    #send_sms(f"le fichier {'Data_Scrapping_offre_'+datetime.now().strftime('%d%m%Y')+'.xlsx'} a été deposé avec succès.")

except Exception as e:

    print("Il y a une erreur dans le code principal:", e)

    send_mail_error_offre(["doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci"])
    #send_sms(f"Il y a une erreur dans le code principal", e )  
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
# Appel de la fonction pour obtenir le DataFrame
#emploi_ci
try:

    emploi_df=emploi_ci()
    emploi_df.reset_index(drop=True, inplace=True)
    chemin_fichier_emploi_df = os.path.join('C:/Users/Dell/Documents/UB/IPC/CODE_IPC/COLLECTE_JOURNALIERE_offre_emploi','Data_Scrapping_emploi_df_'+datetime.now().strftime('%d%m%Y')+'.xlsx')
    emploi_df.to_excel(chemin_fichier_emploi_df, index=False)

    send_mail_success_offre(["abdoulayebakayoko265@gmail.com", "doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci","moussakr@gmail.com"])
    #send_sms(f"le fichier {'Data_Scrapping_offre_'+datetime.now().strftime('%d%m%Y')+'.xlsx'} a été deposé avec succès.")

except Exception as e:

    print("Il y a une erreur dans le code principal:", e)

    send_mail_error_offre(["doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci"])
    #send_sms(f"Il y a une erreur dans le code principal", e )

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
# Appeler la fonction projobivoire pour obtenir le DataFrame des offres d'emploi
try:

# Appel de la fonction principale
#Exportation de la donnée Finale
    df_projobivoire = projobivoire()
    chemin_fichier_df_projobivoire = os.path.join('C:/Users/Dell/Documents/UB/IPC/CODE_IPC/COLLECTE_JOURNALIERE_offre_emploi','Data_Scrapping_df_projobivoire_'+datetime.now().strftime('%d%m%Y')+'.xlsx')
    df_projobivoire.to_excel(chemin_fichier_df_projobivoire, index=False)

    send_mail_success_offre(["abdoulayebakayoko265@gmail.com", "doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci","moussakr@gmail.com"])
    #send_sms(f"le fichier {'Data_Scrapping_offre_'+datetime.now().strftime('%d%m%Y')+'.xlsx'} a été deposé avec succès.")

except Exception as e:

    print("Il y a une erreur dans le code principal:", e)

    send_mail_error_offre(["doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci"])
    #send_sms(f"Il y a une erreur dans le code principal", e )

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
# Appel de la fonction principale
try:

# Appel de la fonction principale
#Exportation de la donnée Finale
    mondiale_df=mondiale_ci()
    chemin_fichier_mondiale_df = os.path.join('C:/Users/Dell/Documents/UB/IPC/CODE_IPC/COLLECTE_JOURNALIERE_offre_emploi','Data_Scrapping_mondiale_df_'+datetime.now().strftime('%d%m%Y')+'.xlsx')
    mondiale_df.to_excel(chemin_fichier_mondiale_df, index=False)


    send_mail_success_offre(["abdoulayebakayoko265@gmail.com", "doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci","moussakr@gmail.com"])
    #send_sms(f"le fichier {'Data_Scrapping_offre_'+datetime.now().strftime('%d%m%Y')+'.xlsx'} a été deposé avec succès.")

except Exception as e:

    print("Il y a une erreur dans le code principal:", e)

    send_mail_error_offre(["doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci"])
    #send_sms(f"Il y a une erreur dans le code principal", e )  

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
# Liste des URLs des pages d'offres d'emploi
urls_rmo = [
    "https://rmo-jobcenter.com/fr/nos-offres-emploi.html",
    # Ajoutez d'autres URLs au besoin
]

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


try:

# Appel de la fonction principale
#Exportation de la donnée Finale


    rmo_jobcenter_df = pd.merge(data,rmo_jobcenter_df, on='DETAILS_URL')
    rmo_jobcenter_df = rmo_jobcenter_df.drop_duplicates()
    rmo_jobcenter_df.reset_index(drop=True, inplace=True)
    chemin_fichier_rmo_jobcenter_df = os.path.join('C:/Users/Dell/Documents/UB/IPC/CODE_IPC/COLLECTE_JOURNALIERE_offre_emploi','Data_Scrapping_rmo_jobcenter_df_'+datetime.now().strftime('%d%m%Y')+'.xlsx')
    rmo_jobcenter_df.to_excel(chemin_fichier_rmo_jobcenter_df, index=False)

    

    send_mail_success_offre(["abdoulayebakayoko265@gmail.com", "doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci","moussakr@gmail.com"])
    #send_sms(f"le fichier {'Data_Scrapping_offre_'+datetime.now().strftime('%d%m%Y')+'.xlsx'} a été deposé avec succès.")

except Exception as e:

    print("Il y a une erreur dans le code principal:", e)

    send_mail_error_offre(["doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci"])
    #send_sms(f"Il y a une erreur dans le code principal", e )
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
# Talent_ci
try:

# Appel de la fonction principale
#Exportation de la donnée Finale
    df_talent_ci = talent_ci()
    chemin_fichier_df_talent_ci = os.path.join('C:/Users/Dell/Documents/UB/IPC/CODE_IPC/COLLECTE_JOURNALIERE_offre_emploi','Data_Scrapping_df_talent_ci_'+datetime.now().strftime('%d%m%Y')+'.xlsx')
    df_talent_ci.to_excel(chemin_fichier_df_talent_ci, index=False)

    send_mail_success_offre(["abdoulayebakayoko265@gmail.com", "doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci","moussakr@gmail.com"])
    #send_sms(f"le fichier {'Data_Scrapping_offre_'+datetime.now().strftime('%d%m%Y')+'.xlsx'} a été deposé avec succès.")

except Exception as e:

    print("Il y a une erreur dans le code principal:", e)

    send_mail_error_offre(["doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci"])
    #send_sms(f"Il y a une erreur dans le code principal", e )

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------   

# Agence_emploi_jeunes
try:

# Appel de la fonction principale
#Exportation de la donnée Finale
    agenceemploi_jeunes_df = agence_emploi_jeunes()

    
    chemin_fichier_agenceemploi_jeunes_df = os.path.join('C:/Users/Dell/Documents/UB/IPC/CODE_IPC/COLLECTE_JOURNALIERE_offre_emploi','Data_Scrapping_agenceemploi_jeunes_df_'+datetime.now().strftime('%d%m%Y')+'.xlsx')
    agenceemploi_jeunes_df.to_excel(chemin_fichier_agenceemploi_jeunes_df, index=False)


    send_mail_success_offre(["abdoulayebakayoko265@gmail.com", "doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci","moussakr@gmail.com"])
    #send_sms(f"le fichier {'Data_Scrapping_offre_'+datetime.now().strftime('%d%m%Y')+'.xlsx'} a été deposé avec succès.")

except Exception as e:

    print("Il y a une erreur dans le code principal:", e)

    send_mail_error_offre(["doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci"])
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
# Yop_l_frii  
# Appel de la fonction principale
yop_l_frii= yop_l_frii()
yop_l_frii['INTITULE_DU_POSTE'] = yop_l_frii['INTITULE_DU_POSTE'].str.replace(r'[()]', '')

# Utilisation de str.extract() pour extraire les parties de la chaîne
yop_l_frii['DATE_DE_DEBUT_DE_L_OFFRE'] = yop_l_frii['INTITULE_DU_POSTE'].str.extract(r'(\d+\s\w+\s\d+)$')



# Remplacer la partie extraite par une chaîne vide pour obtenir INTITULE_DU_POSTE
yop_l_frii['INTITULE_DU_POSTE'] = yop_l_frii['INTITULE_DU_POSTE'].str.replace(r'(\d+\s\w+\s\d+)$', '')
yop_l_frii['NOMBRE_DE_POSTE_DE_TRAVAIL'] = yop_l_frii['INTITULE_DU_POSTE'].str.extract(r'(\d+)\s*postes')

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

try:

# Appel de la fonction principale
#Exportation de la donnée Finale
    yop_l_frii_total = pd.merge(yop_l_frii,df, on='URL_DU_POSTE')
    yop_l_frii_total = yop_l_frii_total.drop_duplicates()
    yop_l_frii_total.reset_index(drop=True, inplace=True)
    yop_l_frii_total  # Affichage du DataFrame résultant
    chemin_fichier_yop_l_frii_total = os.path.join('C:/Users/Dell/Documents/UB/IPC/CODE_IPC/COLLECTE_JOURNALIERE_offre_emploi','Data_Scrapping_yop_l_frii_total_'+datetime.now().strftime('%d%m%Y')+'.xlsx')
    yop_l_frii_total.to_excel(chemin_fichier_yop_l_frii_total, index=False)


    send_mail_success_offre(["abdoulayebakayoko265@gmail.com", "doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci","moussakr@gmail.com"])
    #send_sms(f"le fichier {'Data_Scrapping_offre_'+datetime.now().strftime('%d%m%Y')+'.xlsx'} a été deposé avec succès.")

except Exception as e:

    print("Il y a une erreur dans le code principal:", e)

    send_mail_error_offre(["doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci"])
    #send_sms(f"Il y a une erreur dans le code principal", e )

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------  
# totaux
try:

# Appel de la fonction principale
#Exportation de la donnée Finale


    df_final = pd.concat([df_novojob, df_educarriere,df_projobivoire,emploi_df,alerte_emploi_df,mondiale_df,rmo_jobcenter_df,df_talent_ci,yop_l_frii_total,agenceemploi_jeunes_df], axis=0, ignore_index=True)
    chemin_fichier_collecte = os.path.join('C:/Users/Dell/Documents/UB/IPC/CODE_IPC/COLLECTE_JOURNALIERE_offre_emploi','Data_Scrapping_offre_'+datetime.now().strftime('%d%m%Y')+'.xlsx')
    df_final.to_excel(chemin_fichier_collecte, index=False)
    

    send_mail_success_offre(["abdoulayebakayoko265@gmail.com", "doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci","moussakr@gmail.com"])
    #send_sms(f"le fichier {'Data_Scrapping_offre_'+datetime.now().strftime('%d%m%Y')+'.xlsx'} a été deposé avec succès.")

except Exception as e:

    print("Il y a une erreur dans le code principal:", e)

    send_mail_error_offre(["doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci"])
    #send_sms(f"Il y a une erreur dans le code principal", e )
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------       

try:

# Appel de la fonction principale
#Exportation de la donnée Finale
 
    doublon = doublon(df_final)
    chemin_fichier_collecte1 = os.path.join('C:/Users/Dell/Documents/UB/IPC/CODE_IPC/COLLECTE_JOURNALIERE_offre_emploi','Data_Scrapping_doublon_'+datetime.now().strftime('%d%m%Y')+'.xlsx')
    doublon.to_excel(chemin_fichier_collecte1, index=False)

    send_mail_success_offre(["abdoulayebakayoko265@gmail.com", "doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci","moussakr@gmail.com"])
    #send_sms(f"le fichier {'Data_Scrapping_offre_'+datetime.now().strftime('%d%m%Y')+'.xlsx'} a été deposé avec succès.")

except Exception as e:

    print("Il y a une erreur dans le code principal:", e)

    send_mail_error_offre(["doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci"])
    #send_sms(f"Il y a une erreur dans le code principal", e )
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------       