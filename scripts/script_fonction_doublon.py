import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string

def preprocess_text(text):
    if isinstance(text, str):  # Vérifier si le texte est une chaîne de caractères
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
    elif isinstance(text, float):  # Si c'est une valeur float, remplacer par une chaîne vide
        text = ''
    return text

def doublon(df_final):
    # Prétraitement des données
    # Remplacer les valeurs manquantes par une chaîne vide dans les colonnes utilisées
    df_final['INTITULE_DU_POSTE_clean'] = df_final['INTITULE_DU_POSTE'].fillna('')
    df_final['Description_clean'] = df_final['Description'].fillna('')
    df_final['Entreprise_clean'] = df_final['Entreprise'].fillna('')
    df_final['DIPLOME_clean'] = df_final["DIPLOME"].fillna('')
    df_final['TYPE_DE_CONTRAT_DU_POSTE_clean'] = df_final["TYPE_DE_CONTRAT_DU_POSTE"].fillna('')

    # Prétraitement des données
    df_final['Description_clean'] = df_final['Description_clean'].apply(preprocess_text)
    df_final['INTITULE_DU_POSTE_clean'] = df_final['INTITULE_DU_POSTE_clean'].apply(preprocess_text)
    df_final['Entreprise_clean'] = df_final['Entreprise_clean'].apply(preprocess_text)
    df_final['DIPLOME_clean'] = df_final["DIPLOME_clean"].apply(preprocess_text)   
    df_final['TYPE_DE_CONTRAT_DU_POSTE_clean'] = df_final["TYPE_DE_CONTRAT_DU_POSTE_clean"].apply(preprocess_text)

    # Concaténer toutes les variables pour créer un texte combiné
    df_final['Combined_text'] = df_final['INTITULE_DU_POSTE_clean'] + ' ' + df_final['Description_clean'] + ' ' + df_final['Entreprise_clean'] + ' ' + df_final['DIPLOME_clean'] + ' ' + df_final['TYPE_DE_CONTRAT_DU_POSTE_clean']

    # Vectorisation des données
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(df_final['Combined_text'])

    # Calcul de similarité
    similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Seuil de similarité
    threshold = 0.9

    # Identification des doublons
    duplicates = set()
    for i in range(len(similarities)):
        for j in range(i+1, len(similarities)):
            if similarities[i,j] > threshold:
                duplicates.add(j)

    # Suppression des doublons
    df_final = df_final.drop(index=duplicates).reset_index(drop=True)

    # Retourner le DataFrame final
    return df_final