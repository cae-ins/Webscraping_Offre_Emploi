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
from script_scrapping_Yop_l_frii import yop_l_frii
from script_fonction_doublon import preprocess_text, doublon

from selenium import webdriver
#from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import os
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, types

##-----------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 

from urllib.parse import quote_plus

# Copie du DataFrame source


def nettoyer_et_inserer(df, table_name):
    """
    Nettoie les colonnes texte du DataFrame et insère les données dans PostgreSQL.

    Args:
        df (pd.DataFrame): Le DataFrame à nettoyer et insérer.
        table_name (str): Le nom de la table cible (sans suffixe '_offres').
    """
    # 1. Nettoyage des champs texte
    try:
        for col in df.select_dtypes(include='object').columns:
            df[col] = df[col].astype(str).apply(
                lambda x: x.encode('latin1', errors='replace').decode('utf-8', errors='replace')
            )
        print("✅ Encodage des colonnes texte nettoyé avec succès.")
    except Exception as e:
        print("❌ Erreur lors du nettoyage des chaînes :", e)
        raise

    # 2. Connexion PostgreSQL + Insertion
    try:
        # Paramètres de connexion
        user = 'mngerscrpdb'
        password = quote_plus('P@ssw0rd')  # Encodage sécurisé du mot de passe
        host = '192.168.1.248'
        port = '5432'
        database = 'scrappinjob_db'

        # Création du moteur SQLAlchemy
        engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')

        # Mapping des types pour insertion
        dtype_mapping = {col: types.Text() for col in df.columns}

        # Insertion dans la base de données
        df.to_sql(
            name=f"{table_name}_offres",
            con=engine,
            if_exists='replace',
            index=False,
            dtype=dtype_mapping,
            method='multi'
        )
        print(f"✅ Insertion réussie dans PostgreSQL : table {table_name}_offres")
    except Exception as e:
        print("❌ Erreur de connexion ou d'insertion dans PostgreSQL :", e)
        raise

# Exécution de la fonction avec le DataFrame et le nom de table


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------  
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
    # 2. Nettoyage de tous les champs texte (force l'encodage/décodage sûr)
    nettoyer_et_inserer(df_novojob, "df_novojob")
    

    send_mail_success_offre(["abdoulayebakayoko265@gmail.com", "doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci","moussakr@gmail.com"])
    #send_sms(f"le fichier {'Data_Scrapping_offre_'+datetime.now().strftime('%d%m%Y')+'.xlsx'} a été deposé avec succès.")

except Exception as e:

    print("Il y a une erreur dans le code principal:", e)

    send_mail_error_offre(["doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci"])
    #send_sms(f"Il y a une erreur dans le code principal", e )
# totaux


#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------   

# Educarriere
try:

# Appel de la fonction principale
#Exportation de la donnée Finale

    df_educarriere = emploi_educarriere()
    chemin_fichier_df_educarriere = os.path.join('C:/Users/Dell/Documents/UB/IPC/CODE_IPC/COLLECTE_JOURNALIERE_offre_emploi','Data_Scrapping_df_educarriere_'+datetime.now().strftime('%d%m%Y')+'.xlsx')
    df_educarriere.to_excel(chemin_fichier_df_educarriere, index=False)
    # 2. Nettoyage de tous les champs texte (force l'encodage/décodage sûr)
    nettoyer_et_inserer(df_educarriere, "df_educarriere")


    send_mail_success_offre(["abdoulayebakayoko265@gmail.com", "doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci","moussakr@gmail.com"])
    #send_sms(f"le fichier {'Data_Scrapping_offre_'+datetime.now().strftime('%d%m%Y')+'.xlsx'} a été deposé avec succès.")

except Exception as e:

    print("Il y a une erreur dans le code principal:", e)

    send_mail_error_offre(["doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci"])
    #send_sms(f"Il y a une erreur dans le code principal", e )
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
try:

    alerte_emploi_df = alerteemploi()
    alerte_emploi_df.reset_index(drop=True, inplace=True)
    chemin_fichier_alerte_emploi_df = os.path.join('C:/Users/Dell/Documents/UB/IPC/CODE_IPC/COLLECTE_JOURNALIERE_offre_emploi','Data_Scrapping_alerteemploi_df_'+datetime.now().strftime('%d%m%Y')+'.xlsx')
    alerte_emploi_df.to_excel(chemin_fichier_alerte_emploi_df, index=False)
    # 2. Nettoyage de tous les champs texte (force l'encodage/décodage sûr)
    nettoyer_et_inserer(alerte_emploi_df, "alerte_emploi_df")

    send_mail_success_offre(["abdoulayebakayoko265@gmail.com", "doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci","moussakr@gmail.com"])
    #send_sms(f"le fichier {'Data_Scrapping_offre_'+datetime.now().strftime('%d%m%Y')+'.xlsx'} a été deposé avec succès.")

except Exception as e:

    print("Il y a une erreur dans le code principal:", e)

    send_mail_error_offre(["doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci"])
    #send_sms(f"Il y a une erreur dans le code principal", e )  
#-------
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------    
# Appel de la fonction pour obtenir le DataFrame
#emploi_ci
try:

    emploi_df =emploi_ci()
    emploi_df.reset_index(drop=True, inplace=True)
    chemin_fichier_emploi_df = os.path.join('C:/Users/Dell/Documents/UB/IPC/CODE_IPC/COLLECTE_JOURNALIERE_offre_emploi','Data_Scrapping_emploi_df_'+datetime.now().strftime('%d%m%Y')+'.xlsx')
    emploi_df.to_excel(chemin_fichier_emploi_df, index=False)
    # 2. Nettoyage de tous les champs texte (force l'encodage/décodage sûr)
    nettoyer_et_inserer(emploi_df, "emploi_df")

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
    # 2. Nettoyage de tous les champs texte (force l'encodage/décodage sûr)
    nettoyer_et_inserer(df_projobivoire, "df_projobivoire") 
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

    # 2. Nettoyage de tous les champs texte (force l'encodage/décodage sûr)
    nettoyer_et_inserer(mondiale_df, "mondiale_df") 
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
    
    rmo_jobcenter_df=rmo_jobcenter()
    chemin_fichier_rmo_jobcenter_df = os.path.join('C:/Users/Dell/Documents/UB/IPC/CODE_IPC/COLLECTE_JOURNALIERE_offre_emploi','Data_Scrapping_rmo_jobcenter_df_'+datetime.now().strftime('%d%m%Y')+'.xlsx')
    rmo_jobcenter_df.to_excel(chemin_fichier_rmo_jobcenter_df, index=False)
    # 2. Nettoyage de tous les champs texte (force l'encodage/décodage sûr)
    nettoyer_et_inserer(rmo_jobcenter_df, "rmo_jobcenter_df") 

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
    # 2. Nettoyage de tous les champs texte (force l'encodage/décodage sûr)
    nettoyer_et_inserer(df_talent_ci, "df_talent_ci")

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
    # 2. Nettoyage de tous les champs texte (force l'encodage/décodage sûr)
    nettoyer_et_inserer(agenceemploi_jeunes_df, "agenceemploi_jeunes_df")


    send_mail_success_offre(["abdoulayebakayoko265@gmail.com", "doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci","moussakr@gmail.com"])
    #send_sms(f"le fichier {'Data_Scrapping_offre_'+datetime.now().strftime('%d%m%Y')+'.xlsx'} a été deposé avec succès.")

except Exception as e:

    print("Il y a une erreur dans le code principal:", e)

    send_mail_error_offre(["doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci"])
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------   




try:

# Appel de la fonction principale
#Exportation de la donnée Finale
    yop_l_frii_total= yop_l_frii()
     # Affichage du DataFrame résultant
    chemin_fichier_yop_l_frii_total = os.path.join('C:/Users/Dell/Documents/UB/IPC/CODE_IPC/COLLECTE_JOURNALIERE_offre_emploi','Data_Scrapping_yop_l_frii_total_'+datetime.now().strftime('%d%m%Y')+'.xlsx')
    yop_l_frii_total.to_excel(chemin_fichier_yop_l_frii_total, index=False)
    # 2. Nettoyage de tous les champs texte (force l'encodage/décodage sûr)
    nettoyer_et_inserer(yop_l_frii_total, "yop_l_frii_total")


    send_mail_success_offre(["abdoulayebakayoko265@gmail.com", "doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci","moussakr@gmail.com"])
    #send_sms(f"le fichier {'Data_Scrapping_offre_'+datetime.now().strftime('%d%m%Y')+'.xlsx'} a été deposé avec succès.")

except Exception as e:

    print("Il y a une erreur dans le code principal:", e)

    send_mail_error_offre(["doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci"])
    #send_sms(f"Il y a une erreur dans le code principal", e )


#----------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------       
dfs = [df_novojob, df_educarriere, df_projobivoire, emploi_df, alerte_emploi_df, mondiale_df, rmo_jobcenter_df, df_talent_ci, yop_l_frii_total, agenceemploi_jeunes_df]
try:
    # Concaténation des DataFrames existants
    
    df_final = pd.concat([df for df in dfs if not df.empty], ignore_index=True)

    # Exportation de la donnée Finale
    chemin_fichier_collecte = os.path.join('C:/Users/Dell/Documents/UB/IPC/CODE_IPC/COLLECTE_JOURNALIERE_offre_emploi', 'Data_Scrapping_offre_' + datetime.now().strftime('%d%m%Y') + '.xlsx')
    df_final.to_excel(chemin_fichier_collecte, index=False)

    # Envoyer un email de succès
    send_mail_success_offre(["abdoulayebakayoko265@gmail.com", "doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci", "moussakr@gmail.com"])
    # Envoyer un SMS
    #send_sms(f"le fichier {'Data_Scrapping_offre_'+datetime.now().strftime('%d%m%Y')+'.xlsx'} a été deposé avec succès.")

except Exception as e:
    print("Il y a une erreur dans le code principal:", e)

    try:
        # Si une erreur se produit, concaténez les DataFrames qui existent
        dfs = [df for df in dfs if not df.empty]
        df_final = pd.concat(dfs, ignore_index=True)
        chemin_fichier_collecte = os.path.join('C:/Users/Dell/Documents/UB/IPC/CODE_IPC/COLLECTE_JOURNALIERE_offre_emploi', 'Data_Scrapping_offre_' + datetime.now().strftime('%d%m%Y') + '.xlsx')
        df_final.to_excel(chemin_fichier_collecte, index=False)

        # Envoyer un email d'erreur
        send_mail_error_offre(["doumbiaabdoulaye0525@gmail.com"], ["j.migone@stat.plan.gouv.ci"])
        # Envoyer un SMS
        #send_sms(f"Il y a une erreur dans le code principal: {e}")

    except Exception as concat_error:
        print("Erreur lors de la concaténation des DataFrames:", concat_error)

#------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------
# 2. Nettoyage de tous les champs texte (force l'encodage/décodage sûr)
nettoyer_et_inserer(df_final, "Data_Scrapping_offre_brute")
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
# 2. Nettoyage de tous les champs texte (force l'encodage/décodage sûr)
nettoyer_et_inserer(doublon, "Data_Scrapping_offre")