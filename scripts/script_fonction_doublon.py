import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
from transformers import CamembertModel, CamembertTokenizer
import torch

#syntax d'install de la version stable du package tranformers 

def preprocess_text(text):
    if isinstance(text, str):  # Vérifier si le texte est une chaîne de caractères
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
    elif isinstance(text, float):  # Si c'est une valeur float, remplacer par une chaîne vide
        text = ''
    return text

def traitement_combinaison_final(df_final):
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
    return df_final

df_final = traitement_combinaison_final(df_final)

def extract_embeddings(text):
    # Tokenize the text
    tokens = tokenizer.encode(text, add_special_tokens=True)
    
    # Convert tokens to tensor
    input_ids = torch.tensor([tokens]).to(device)
    
    # Get the embeddings
    with torch.no_grad():
        outputs = model(input_ids)
        embeddings = outputs.last_hidden_state.squeeze(0)
    
    return embeddings

def doublon_embeddings_camembert(df_final):
    #Vérification de la disponibilité du GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    #Chargement du modèle camembert et du tokenizer
    model_name = 'camembert-base'
    model = CamembertModel.from_pretrained(model_name).to(device)
    tokenizer = CamembertTokenizer.from_pretrained(model_name)
    
    encoding_values = tokenizer(df_final['Combined_text'])

    threshold = 0.9

    # Calcul de similarité
    similarities = cosine_similarity(encoding_values, encoding_values)

    # Identification des doublons
    duplicates = set()
    for i in range(len(similarities)):
        for j in range(i+1, len(similarities)):
            if similarities[i,j] > threshold:
                duplicates.add(j)

    # Suppression des doublons
    df_final = df_final.drop(index=duplicates).reset_index(drop=True)

# Suppression des doublons
    df_final = df_final.drop(index=duplicates).reset_index(drop=True)

    # Retourner le DataFrame final
    return df_final



def doublon_tfidf(df_final):
    # Prétraitement des données
    # Remplacer les valeurs manquantes par une chaîne vide dans les colonnes utilisées
    

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