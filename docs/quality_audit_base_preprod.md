# 📊 RÉSULTATS DE L'AUDIT DE QUALITÉ DES DONNÉES

---

## Table : **auth_group**

| Colonne | Type | Lignes | NULL (%) | Vide (%) | Distincts | Cardinalité (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| id | integer | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| name | character varying | 0 | 0.00% | 0.00% | 0 | **0.00%** |

---

## Table : **auth_group_permissions**

| Colonne | Type | Lignes | NULL (%) | Vide (%) | Distincts | Cardinalité (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| id | bigint | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| group_id | integer | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| permission_id | integer | 0 | 0.00% | 0.00% | 0 | **0.00%** |

---

## Table : **auth_permission**

| Colonne | Type | Lignes | NULL (%) | Vide (%) | Distincts | Cardinalité (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| id | integer | 44 | 0.00% | 0.00% | 44 | **100.00%** |
| name | character varying | 44 | 0.00% | 0.00% | 44 | **100.00%** |
| content_type_id | integer | 44 | 0.00% | 0.00% | 11 | **25.00%** |
| codename | character varying | 44 | 0.00% | 0.00% | 44 | **100.00%** |

---

## Table : **auth_user**

| Colonne | Type | Lignes | NULL (%) | Vide (%) | Distincts | Cardinalité (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| id | integer | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| password | character varying | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| last_login | timestamp with time zone | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| is_superuser | boolean | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| username | character varying | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| first_name | character varying | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| last_name | character varying | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| email | character varying | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| is_staff | boolean | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| is_active | boolean | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| date_joined | timestamp with time zone | 0 | 0.00% | 0.00% | 0 | **0.00%** |

---

## Table : **auth_user_groups**

| Colonne | Type | Lignes | NULL (%) | Vide (%) | Distincts | Cardinalité (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| id | bigint | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| user_id | integer | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| group_id | integer | 0 | 0.00% | 0.00% | 0 | **0.00%** |

---

## Table : **auth_user_user_permissions**

| Colonne | Type | Lignes | NULL (%) | Vide (%) | Distincts | Cardinalité (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| id | bigint | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| user_id | integer | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| permission_id | integer | 0 | 0.00% | 0.00% | 0 | **0.00%** |

---

## Table : **df_educarriere_offres**

| Colonne | Type | Lignes | NULL (%) | Vide (%) | Distincts | Cardinalité (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| INTITULE_DU_POSTE | text | 930 | 0.00% | 0.00% | 31 | **3.33%** |
| Job_Link | text | 930 | 0.00% | 0.00% | 31 | **3.33%** |
| Image_URL | text | 930 | 0.00% | 0.00% | 1 | **0.11%** |
| Code | text | 930 | 0.00% | 0.00% | 31 | **3.33%** |
| Date_DEdition | text | 930 | 0.00% | 0.00% | 2 | **0.22%** |
| Date_limite | text | 930 | 0.00% | 0.00% | 11 | **1.18%** |
| URL | text | 930 | 0.00% | 0.00% | 30 | **3.23%** |
| Image URL | text | 930 | 0.00% | 0.00% | 9 | **0.97%** |
| SPECIALITE | text | 930 | 0.00% | 0.00% | 25 | **2.69%** |
| DIPLOME | text | 930 | 0.00% | 0.00% | 16 | **1.72%** |
| Annee_Experience | text | 930 | 0.00% | 3.23% | 11 | **1.18%** |
| LIEU_DU_POSTE_DE_TRAVAIL | text | 930 | 0.00% | 0.00% | 18 | **1.94%** |
| DATE_DE_DEBUT_DE_L_OFFRE | text | 930 | 0.00% | 0.00% | 2 | **0.22%** |
| DATE_D_EXPIRATION_DE_L_OFFRE | text | 930 | 0.00% | 0.00% | 11 | **1.18%** |
| DESCRIPTION_DU_POSTE | text | 930 | 0.00% | 0.00% | 23 | **2.47%** |
| Profil_Poste | text | 930 | 0.00% | 0.00% | 23 | **2.47%** |
| Dossiers de candidature | text | 930 | 0.00% | 0.00% | 23 | **2.47%** |

---

## Table : **df_novojob**

| Colonne | Type | Lignes | NULL (%) | Vide (%) | Distincts | Cardinalité (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| INTITULE_DU_POSTE | text | 6 | 0.00% | 0.00% | 5 | **83.33%** |
| Entreprise | text | 6 | 0.00% | 0.00% | 2 | **33.33%** |
| PAYS_DU_POSTE_DE_TRAVAIL | text | 6 | 0.00% | 0.00% | 1 | **16.67%** |
| DATE_DE_DEBUT_DE_L_OFFRE | text | 6 | 0.00% | 0.00% | 3 | **50.00%** |
| Niveau_Experience | text | 6 | 0.00% | 0.00% | 1 | **16.67%** |
| Annee_Experience | text | 6 | 0.00% | 0.00% | 2 | **33.33%** |
| URL | text | 6 | 0.00% | 0.00% | 2 | **33.33%** |
| SITE_WEB_DE_L_ENTREPRISE | text | 6 | 0.00% | 0.00% | 5 | **83.33%** |
| LIEU_DU_POSTE_DE_TRAVAIL | text | 6 | 0.00% | 0.00% | 2 | **33.33%** |
| DATE_D_EXPIRATION_DE_L_OFFRE | text | 6 | 0.00% | 0.00% | 3 | **50.00%** |
| SPECIALITE | text | 6 | 0.00% | 0.00% | 2 | **33.33%** |
| BRANCHE_D_ACTIVITE | text | 6 | 0.00% | 0.00% | 2 | **33.33%** |
| DIPLOME | text | 6 | 0.00% | 0.00% | 3 | **50.00%** |
| NOMBRE_DE_POSTES_A_POURVOIR | text | 6 | 0.00% | 0.00% | 1 | **16.67%** |
| TYPE_DE_CONTRAT_DU_POSTE | text | 6 | 0.00% | 0.00% | 1 | **16.67%** |
| DESCRIPTION_DU_POSTE | text | 6 | 0.00% | 0.00% | 5 | **83.33%** |
| VILLE_DU_POSTE_DE_TRAVAIL | text | 6 | 0.00% | 0.00% | 2 | **33.33%** |

---

## Table : **df_novojob_offres**

| Colonne | Type | Lignes | NULL (%) | Vide (%) | Distincts | Cardinalité (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| INTITULE_DU_POSTE | text | 271 | 0.00% | 0.00% | 38 | **14.02%** |
| Entreprise | text | 271 | 0.00% | 0.00% | 22 | **8.12%** |
| PAYS_DU_POSTE_DE_TRAVAIL | text | 271 | 0.00% | 64.21% | 2 | **0.74%** |
| DATE_DE_DEBUT_DE_L_OFFRE | text | 271 | 0.00% | 0.00% | 15 | **5.54%** |
| Niveau_Experience | text | 271 | 0.00% | 0.00% | 5 | **1.85%** |
| Annee_Experience | text | 271 | 0.00% | 0.00% | 4 | **1.48%** |
| URL | text | 271 | 0.00% | 0.00% | 25 | **9.23%** |
| SITE_WEB_DE_L_ENTREPRISE | text | 271 | 0.00% | 0.00% | 38 | **14.02%** |
| LIEU_DU_POSTE_DE_TRAVAIL | text | 271 | 0.00% | 0.00% | 2 | **0.74%** |
| DATE_D_EXPIRATION_DE_L_OFFRE | text | 271 | 0.00% | 0.00% | 18 | **6.64%** |
| SPECIALITE | text | 271 | 0.00% | 0.00% | 9 | **3.32%** |
| BRANCHE_D_ACTIVITE | text | 271 | 0.00% | 0.00% | 5 | **1.85%** |
| DIPLOME | text | 271 | 0.00% | 0.00% | 13 | **4.80%** |
| NOMBRE_DE_POSTES_A_POURVOIR | text | 271 | 0.00% | 0.00% | 6 | **2.21%** |
| TYPE_DE_CONTRAT_DU_POSTE | text | 271 | 0.00% | 0.00% | 7 | **2.58%** |
| DESCRIPTION_DU_POSTE | text | 271 | 0.00% | 0.00% | 38 | **14.02%** |
| RAISON_SOCIALE_DE_L_ENTREPRISE | text | 271 | 0.00% | 0.00% | 2 | **0.74%** |
| VILLE_DU_POSTE_DE_TRAVAIL | text | 271 | 0.00% | 0.00% | 2 | **0.74%** |

---

## Table : **df_projobivoire_offres**

| Colonne | Type | Lignes | NULL (%) | Vide (%) | Distincts | Cardinalité (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| SPECIALITE | text | 5457 | 0.00% | 100.00% | 1 | **0.02%** |
| TYPE_DE_CONTRAT_DU_POSTE | text | 5457 | 0.00% | 0.22% | 12 | **0.22%** |
| DATE_DE_DEBUT_DE_L_OFFRE | text | 5457 | 0.00% | 0.00% | 284 | **5.20%** |
| DATE_D_EXPIRATION_DE_L_OFFRE | text | 5457 | 0.00% | 0.00% | 229 | **4.20%** |
| INTITULE_DU_POSTE | text | 5457 | 0.00% | 2.25% | 117 | **2.14%** |
| URL | text | 5457 | 0.00% | 0.00% | 4355 | **79.81%** |
| SITE_WEB_DE_L_ENTREPRISE | text | 5457 | 0.00% | 0.00% | 546 | **10.01%** |

---

## Table : **df_talent_ci_offres**

| Colonne | Type | Lignes | NULL (%) | Vide (%) | Distincts | Cardinalité (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| INTITULE_DU_POSTE | text | 80 | 0.00% | 0.00% | 74 | **92.50%** |
| RAISON_SOCIALE_DE_L_ENTREPRISE | text | 80 | 0.00% | 100.00% | 1 | **1.25%** |
| LIEU_DU_POSTE_DE_TRAVAIL | text | 80 | 0.00% | 100.00% | 1 | **1.25%** |
| DESCRIPTION_DU_POSTE | text | 80 | 0.00% | 100.00% | 1 | **1.25%** |
| DERNIERE_MISE_A_JOUR | text | 80 | 0.00% | 100.00% | 1 | **1.25%** |
| SITE_WEB_DE_L_ENTREPRISE | text | 80 | 0.00% | 0.00% | 4 | **5.00%** |

---

## Table : **django_admin_log**

| Colonne | Type | Lignes | NULL (%) | Vide (%) | Distincts | Cardinalité (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| id | integer | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| action_time | timestamp with time zone | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| object_id | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| object_repr | character varying | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| action_flag | smallint | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| change_message | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| content_type_id | integer | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| user_id | integer | 0 | 0.00% | 0.00% | 0 | **0.00%** |

---

## Table : **django_content_type**

| Colonne | Type | Lignes | NULL (%) | Vide (%) | Distincts | Cardinalité (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| id | integer | 11 | 0.00% | 0.00% | 11 | **100.00%** |
| app_label | character varying | 11 | 0.00% | 0.00% | 5 | **45.45%** |
| model | character varying | 11 | 0.00% | 0.00% | 11 | **100.00%** |

---

## Table : **django_migrations**

| Colonne | Type | Lignes | NULL (%) | Vide (%) | Distincts | Cardinalité (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| id | bigint | 24 | 0.00% | 0.00% | 24 | **100.00%** |
| app | character varying | 24 | 0.00% | 0.00% | 5 | **20.83%** |
| name | character varying | 24 | 0.00% | 0.00% | 20 | **83.33%** |
| applied | timestamp with time zone | 24 | 0.00% | 0.00% | 24 | **100.00%** |

---

## Table : **django_session**

| Colonne | Type | Lignes | NULL (%) | Vide (%) | Distincts | Cardinalité (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| session_key | character varying | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| session_data | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| expire_date | timestamp with time zone | 0 | 0.00% | 0.00% | 0 | **0.00%** |

---

## Table : **educarriere_offres**

| Colonne | Type | Lignes | NULL (%) | Vide (%) | Distincts | Cardinalité (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| BRANCHE_D_ACTIVITE | text | 470 | 0.00% | 0.00% | 30 | **6.38%** |
| TYPE_DE_CONTRAT_DU_POSTE | text | 470 | 0.00% | 0.00% | 4 | **0.85%** |
| SPECIALITE | text | 470 | 0.00% | 0.00% | 29 | **6.17%** |
| DIPLOME | text | 470 | 0.00% | 0.00% | 14 | **2.98%** |
| EXPERIENCE_PROFESSIONNELLE | text | 470 | 25.53% | 0.00% | 6 | **1.28%** |
| LIEU_DU_POSTE_DE_TRAVAIL | text | 470 | 0.00% | 0.00% | 13 | **2.77%** |
| SITE_WEB_DE_L_ENTREPRISE | text | 470 | 0.00% | 0.00% | 30 | **6.38%** |
| DATE_DE_DEBUT_DE_L_OFFRE | text | 470 | 0.00% | 0.00% | 3 | **0.64%** |
| DATE_D_EXPIRATION_DE_L_OFFRE | text | 470 | 0.00% | 0.00% | 10 | **2.13%** |
| Description | text | 470 | 0.00% | 0.00% | 31 | **6.60%** |
| INTITULE_DU_POSTE | text | 470 | 0.00% | 0.00% | 371 | **78.94%** |
| Sous_titre | text | 470 | 0.00% | 0.00% | 406 | **86.38%** |
| Code | text | 470 | 0.00% | 0.00% | 417 | **88.72%** |
| Date_DEdition | text | 470 | 0.00% | 0.00% | 57 | **12.13%** |
| Date_limite | text | 470 | 0.00% | 0.00% | 52 | **11.06%** |
| PAYS_DU_POSTE_DE_TRAVAIL | text | 470 | 0.00% | 0.00% | 93 | **19.79%** |
| URL | text | 470 | 0.00% | 0.00% | 28 | **5.96%** |
| Unite_EXPERIENCE_PROFESSIONNELLE | text | 470 | 0.00% | 0.00% | 2 | **0.43%** |

---

## Table : **emploi_ci_offres**

| Colonne | Type | Lignes | NULL (%) | Vide (%) | Distincts | Cardinalité (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| INTITULE_DU_POSTE | text | 625 | 0.00% | 0.00% | 25 | **4.00%** |
| Entreprise | text | 625 | 0.00% | 0.00% | 21 | **3.36%** |
| DATE_DE_DEBUT_DE_L_OFFRE | text | 625 | 0.00% | 0.00% | 3 | **0.48%** |
| DESCRIPTION_DU_POSTE | text | 625 | 0.00% | 0.00% | 25 | **4.00%** |
| LIEU_DU_POSTE_DE_TRAVAIL | text | 625 | 0.00% | 0.00% | 6 | **0.96%** |
| DIPLOME | text | 625 | 0.00% | 0.00% | 12 | **1.92%** |
| Annee_Experience | text | 625 | 0.00% | 0.00% | 9 | **1.44%** |
| TYPE_DE_CONTRAT_DU_POSTE | text | 625 | 0.00% | 0.00% | 9 | **1.44%** |
| SOUS_POSTE | text | 625 | 0.00% | 12.00% | 23 | **3.68%** |
| URL | text | 625 | 0.00% | 0.00% | 1 | **0.16%** |
| Offre_Link | text | 625 | 0.00% | 0.00% | 25 | **4.00%** |

---

## Table : **emploi_df_offres**

| Colonne | Type | Lignes | NULL (%) | Vide (%) | Distincts | Cardinalité (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Poste | text | 271 | 0.00% | 0.00% | 249 | **91.88%** |
| Ville | text | 271 | 0.00% | 0.00% | 47 | **17.34%** |
| Offre_Link | text | 271 | 0.00% | 0.00% | 271 | **100.00%** |
| Entreprise | text | 271 | 0.00% | 0.00% | 145 | **53.51%** |
| Description | text | 271 | 0.00% | 0.00% | 270 | **99.63%** |
| Niveau_Études | text | 271 | 0.00% | 0.00% | 1 | **0.37%** |
| Niveau_Expérience | text | 271 | 0.00% | 0.00% | 13 | **4.80%** |
| Contrat | text | 271 | 0.00% | 0.00% | 32 | **11.81%** |
| Région | text | 271 | 0.00% | 0.00% | 18 | **6.64%** |
| Compétences | text | 271 | 0.00% | 0.00% | 224 | **82.66%** |
| Date_Publication | text | 271 | 0.00% | 0.00% | 22 | **8.12%** |

---

## Table : **emploi_offres**

| Colonne | Type | Lignes | NULL (%) | Vide (%) | Distincts | Cardinalité (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| titre | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| date_publication | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| LIEU_DU_POSTE_DE_TRAVAIL | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| description | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| type_contrat | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| URL | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| site_id | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Reference | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| nombre_postes | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| date_expiration | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| niveau_etudes | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| experience_requise | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| formation | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Gender | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Unite_Annee_Experience | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| recruteur_id | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Job Title1 | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Author1 | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Date Posted1 | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Description1 | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Nous Recherchons | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Département | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Supérieur hiérarchique | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Supervise | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Travail % | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Poste Basé à | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| type_mobilite | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Contrat | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Début de contrat | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Job_Link | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Image_URL | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| offre_id | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Date_DEdition | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Date_limite | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Image URL | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| SPECIALITE | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| competences | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Dossiers de candidature | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| entreprise_id | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| PAYS_DU_POSTE_DE_TRAVAIL | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Niveau_Experience | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| BRANCHE_D_ACTIVITE | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| RAISON_SOCIALE_DE_L_ENTREPRISE | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| lieu_id | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| date_mise_a_jour | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Poste | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Ville | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Offre_Link | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Description | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Niveau_Études | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Niveau_Expérience | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Région | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| mots_cles | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Date_Publication | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| DATE_DE_PUBLICATION | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| DETAILS_URL | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Description_Profil | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| salaire_min | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| FILIALE | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| SECTEUR | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| statut_offre | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| fonction | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| POSTE | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| SOUS_POSTE | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| url_offre | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Job Image | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| NOMBRE_DE_POSTE_DE_TRAVAIL | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| Titre du Poste | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| annee_min | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| annee_max | text | 0 | 0.00% | 0.00% | 0 | **0.00%** |

---

## Table : **entreprise_emploi**

| Colonne | Type | Lignes | NULL (%) | Vide (%) | Distincts | Cardinalité (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| offre_id | text | 58225 | 98.53% | 0.00% | 46 | **0.08%** |
| titre | text | 58225 | 0.68% | 0.00% | 13410 | **23.03%** |
| description | text | 58225 | 91.48% | 0.00% | 683 | **1.17%** |
| date_publication | text | 58225 | 0.60% | 0.00% | 1751 | **3.01%** |
| date_mise_a_jour | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| date_expiration | text | 58225 | 40.02% | 0.00% | 1297 | **2.23%** |
| salaire_min | text | 58225 | 99.97% | 0.00% | 3 | **0.01%** |
| salaire_max | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| devise_salaire | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| type_contrat | text | 58225 | 39.39% | 0.00% | 860 | **1.48%** |
| experience_requise | text | 58225 | 53.69% | 0.00% | 579 | **0.99%** |
| categorie | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| fonction | text | 58225 | 99.97% | 0.00% | 18 | **0.03%** |
| url_offre | text | 58225 | 18.18% | 0.00% | 47621 | **81.79%** |
| url_application | text | 58225 | 98.56% | 0.00% | 26 | **0.04%** |
| mots_cles | text | 58225 | 99.58% | 0.00% | 223 | **0.38%** |
| competences | text | 58225 | 98.56% | 0.00% | 26 | **0.04%** |
| niveau_etudes | text | 58225 | 94.71% | 0.00% | 11 | **0.02%** |
| formation | text | 58225 | 92.93% | 0.00% | 47 | **0.08%** |
| type_emploi | text | 58225 | 99.97% | 0.00% | 18 | **0.03%** |
| nombre_postes | text | 58225 | 71.10% | 0.00% | 92 | **0.16%** |
| langue_offre | text | 58225 | 99.97% | 0.00% | 8 | **0.01%** |
| statut_offre | text | 58225 | 99.97% | 0.00% | 18 | **0.03%** |
| vues | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| candidatures | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| type_mobilite | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| niveau_teletravail | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| avantages | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| bonus | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| description_avantages | text | 58225 | 99.97% | 0.00% | 1 | **0.00%** |
| info_diversite | text | 58225 | 99.97% | 0.00% | 2 | **0.00%** |
| video_url | text | 58225 | 98.56% | 0.00% | 6 | **0.01%** |
| label_offre | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| tags | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| infos_environnement_travail | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| certification | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| conditions_travail | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| politique_teletravail | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| process_recrutement | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| commentaires | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| entreprise_id | text | 58225 | 99.02% | 0.00% | 166 | **0.29%** |
| lieu_id | text | 58225 | 19.90% | 0.00% | 4009 | **6.89%** |
| site_id | text | 58225 | 83.80% | 0.00% | 1402 | **2.41%** |
| recruteur_id | text | 58225 | 99.09% | 0.00% | 2 | **0.00%** |

---

## Table : **entreprises**

| Colonne | Type | Lignes | NULL (%) | Vide (%) | Distincts | Cardinalité (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| entreprise_id | integer | 8 | 0.00% | 0.00% | 8 | **100.00%** |
| nom_entreprise | character varying | 8 | 0.00% | 0.00% | 8 | **100.00%** |
| description_entreprise | text | 8 | 100.00% | 0.00% | 0 | **0.00%** |
| secteur_entreprise | character varying | 8 | 0.00% | 0.00% | 4 | **50.00%** |
| taille_entreprise | character varying | 8 | 100.00% | 0.00% | 0 | **0.00%** |
| site_web | character varying | 8 | 0.00% | 0.00% | 8 | **100.00%** |
| type_entreprise | character varying | 8 | 0.00% | 0.00% | 3 | **37.50%** |
| categorie_entreprise | character varying | 8 | 0.00% | 0.00% | 3 | **37.50%** |

---

## Table : **lieux**

| Colonne | Type | Lignes | NULL (%) | Vide (%) | Distincts | Cardinalité (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| lieu_id | integer | 3 | 0.00% | 0.00% | 3 | **100.00%** |
| ville | character varying | 3 | 0.00% | 0.00% | 3 | **100.00%** |
| code_postal | character varying | 3 | 100.00% | 0.00% | 0 | **0.00%** |
| region | character varying | 3 | 100.00% | 0.00% | 0 | **0.00%** |
| pays | character varying | 3 | 0.00% | 33.33% | 2 | **66.67%** |

---

## Table : **mondiale_df_offres**

| Colonne | Type | Lignes | NULL (%) | Vide (%) | Distincts | Cardinalité (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| INTITULE_DU_POSTE | text | 112 | 0.00% | 0.00% | 20 | **17.86%** |
| LIEU_DU_POSTE_DE_TRAVAIL | text | 112 | 0.00% | 0.00% | 18 | **16.07%** |
| DATE_DE_PUBLICATION | text | 112 | 0.00% | 0.00% | 5 | **4.46%** |
| DATE_D_EXPIRATION_DE_L_OFFRE | text | 112 | 0.00% | 0.00% | 10 | **8.93%** |

---

## Table : **novojob_offres**

| Colonne | Type | Lignes | NULL (%) | Vide (%) | Distincts | Cardinalité (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| INTITULE_DU_POSTE | text | 267 | 0.00% | 0.00% | 44 | **16.48%** |
| Entreprise | text | 267 | 0.00% | 0.00% | 16 | **5.99%** |
| PAYS_DU_POSTE_DE_TRAVAIL | text | 267 | 0.00% | 8.61% | 2 | **0.75%** |
| DATE_DE_DEBUT_DE_L_OFFRE | text | 267 | 0.00% | 0.00% | 23 | **8.61%** |
| Niveau_Experience | text | 267 | 0.00% | 0.00% | 5 | **1.87%** |
| Annee_Experience | text | 267 | 0.00% | 0.00% | 4 | **1.50%** |
| URL | text | 267 | 0.00% | 0.00% | 20 | **7.49%** |
| SITE_WEB_DE_L_ENTREPRISE | text | 267 | 0.00% | 0.00% | 45 | **16.85%** |
| LIEU_DU_POSTE_DE_TRAVAIL | text | 267 | 0.00% | 0.00% | 3 | **1.12%** |
| DATE_D_EXPIRATION_DE_L_OFFRE | text | 267 | 0.00% | 0.00% | 25 | **9.36%** |
| SPECIALITE | text | 267 | 0.00% | 0.00% | 10 | **3.75%** |
| BRANCHE_D_ACTIVITE | text | 267 | 0.00% | 0.00% | 6 | **2.25%** |
| DIPLOME | text | 267 | 0.00% | 0.00% | 16 | **5.99%** |
| NOMBRE_DE_POSTES_A_POURVOIR | text | 267 | 0.00% | 0.00% | 9 | **3.37%** |
| TYPE_DE_CONTRAT_DU_POSTE | text | 267 | 0.00% | 0.00% | 6 | **2.25%** |
| DESCRIPTION_DU_POSTE | text | 267 | 0.00% | 0.00% | 45 | **16.85%** |
| RAISON_SOCIALE_DE_L_ENTREPRISE | text | 267 | 0.00% | 0.00% | 2 | **0.75%** |
| VILLE_DU_POSTE_DE_TRAVAIL | text | 267 | 0.00% | 0.00% | 3 | **1.12%** |

---

## Table : **offre_emploi**

| Colonne | Type | Lignes | NULL (%) | Vide (%) | Distincts | Cardinalité (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| offre_id | text | 58225 | 98.53% | 0.00% | 46 | **0.08%** |
| titre | text | 58225 | 0.68% | 0.00% | 13410 | **23.03%** |
| description | text | 58225 | 91.48% | 0.00% | 683 | **1.17%** |
| date_publication | text | 58225 | 1.16% | 0.00% | 1344 | **2.31%** |
| date_mise_a_jour | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| date_expiration | text | 58225 | 1.16% | 0.00% | 1344 | **2.31%** |
| salaire_min | text | 58225 | 99.97% | 0.00% | 3 | **0.01%** |
| salaire_max | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| devise_salaire | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| type_contrat | text | 58225 | 39.39% | 0.00% | 860 | **1.48%** |
| experience_requise | text | 58225 | 53.69% | 0.00% | 579 | **0.99%** |
| categorie | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| fonction | text | 58225 | 99.97% | 0.00% | 18 | **0.03%** |
| url_offre | text | 58225 | 18.18% | 0.00% | 47621 | **81.79%** |
| url_application | text | 58225 | 98.56% | 0.00% | 26 | **0.04%** |
| mots_cles | text | 58225 | 99.58% | 0.00% | 223 | **0.38%** |
| competences | text | 58225 | 98.56% | 0.00% | 26 | **0.04%** |
| niveau_etudes | text | 58225 | 94.71% | 0.00% | 11 | **0.02%** |
| formation | text | 58225 | 92.93% | 0.00% | 47 | **0.08%** |
| type_emploi | text | 58225 | 99.97% | 0.00% | 18 | **0.03%** |
| nombre_postes | text | 58225 | 71.10% | 0.00% | 92 | **0.16%** |
| langue_offre | text | 58225 | 99.97% | 0.00% | 8 | **0.01%** |
| statut_offre | text | 58225 | 99.97% | 0.00% | 18 | **0.03%** |
| vues | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| candidatures | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| type_mobilite | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| niveau_teletravail | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| avantages | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| bonus | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| description_avantages | text | 58225 | 99.97% | 0.00% | 1 | **0.00%** |
| info_diversite | text | 58225 | 99.97% | 0.00% | 2 | **0.00%** |
| video_url | text | 58225 | 98.56% | 0.00% | 6 | **0.01%** |
| label_offre | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| tags | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| infos_environnement_travail | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| certification | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| conditions_travail | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| politique_teletravail | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| process_recrutement | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| commentaires | text | 58225 | 100.00% | 0.00% | 0 | **0.00%** |
| entreprise_id | text | 58225 | 99.02% | 0.00% | 166 | **0.29%** |
| lieu_id | text | 58225 | 19.90% | 0.00% | 4009 | **6.89%** |
| site_id | text | 58225 | 83.80% | 0.00% | 1402 | **2.41%** |
| recruteur_id | text | 58225 | 99.09% | 0.00% | 2 | **0.00%** |

---

## Table : **offres_emploi**

| Colonne | Type | Lignes | NULL (%) | Vide (%) | Distincts | Cardinalité (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| offre_id | integer | 100 | 0.00% | 0.00% | 100 | **100.00%** |
| titre | character varying | 100 | 0.00% | 0.00% | 10 | **10.00%** |
| description | text | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| date_publication | timestamp without time zone | 100 | 0.00% | 0.00% | 8 | **8.00%** |
| date_mise_a_jour | timestamp without time zone | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| date_expiration | timestamp without time zone | 100 | 0.00% | 0.00% | 9 | **9.00%** |
| salaire_min | numeric | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| salaire_max | numeric | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| devise_salaire | character varying | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| type_contrat | character varying | 100 | 0.00% | 0.00% | 3 | **3.00%** |
| experience_requise | character varying | 100 | 0.00% | 0.00% | 7 | **7.00%** |
| categorie | character varying | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| fonction | character varying | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| url_offre | character varying | 100 | 0.00% | 0.00% | 23 | **23.00%** |
| url_application | character varying | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| mots_cles | text | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| competences | text | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| niveau_etudes | character varying | 100 | 0.00% | 0.00% | 6 | **6.00%** |
| formation | character varying | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| type_emploi | character varying | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| nombre_postes | integer | 100 | 0.00% | 0.00% | 3 | **3.00%** |
| langue_offre | character varying | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| statut_offre | character varying | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| vues | integer | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| candidatures | integer | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| type_mobilite | character varying | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| niveau_teletravail | character varying | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| avantages | text | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| bonus | text | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| description_avantages | text | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| info_diversite | text | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| video_url | character varying | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| label_offre | character varying | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| tags | text | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| infos_environnement_travail | text | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| certification | character varying | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| conditions_travail | text | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| politique_teletravail | text | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| process_recrutement | text | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| commentaires | text | 100 | 100.00% | 0.00% | 0 | **0.00%** |
| entreprise_id | integer | 100 | 0.00% | 0.00% | 8 | **8.00%** |
| lieu_id | integer | 100 | 0.00% | 0.00% | 3 | **3.00%** |
| site_id | integer | 100 | 0.00% | 0.00% | 10 | **10.00%** |
| recruteur_id | integer | 100 | 100.00% | 0.00% | 0 | **0.00%** |

---

## Table : **recruteurs**

| Colonne | Type | Lignes | NULL (%) | Vide (%) | Distincts | Cardinalité (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| recruteur_id | integer | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| nom_recruteur | character varying | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| poste_recruteur | character varying | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| email_recruteur | character varying | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| telephone_recruteur | character varying | 0 | 0.00% | 0.00% | 0 | **0.00%** |
| date_dernier_contact | timestamp without time zone | 0 | 0.00% | 0.00% | 0 | **0.00%** |

---

## Table : **rmo_jobcenter_df_offres**

| Colonne | Type | Lignes | NULL (%) | Vide (%) | Distincts | Cardinalité (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| DETAILS_URL | text | 18 | 0.00% | 0.00% | 18 | **100.00%** |
| Description_Profil | text | 18 | 0.00% | 0.00% | 2 | **11.11%** |
| Entreprise | text | 18 | 0.00% | 0.00% | 4 | **22.22%** |
| Code | text | 18 | 0.00% | 0.00% | 18 | **100.00%** |
| BRANCHE_D_ACTIVITE | text | 18 | 0.00% | 0.00% | 8 | **44.44%** |
| LIEU_DU_POSTE_DE_TRAVAIL | text | 18 | 0.00% | 0.00% | 5 | **27.78%** |
| Rémunération | text | 18 | 0.00% | 0.00% | 3 | **16.67%** |
| NOMBRE_DE_POSTES_A_POURVOIR | text | 18 | 0.00% | 0.00% | 2 | **11.11%** |
| DIPLOME | text | 18 | 0.00% | 0.00% | 4 | **22.22%** |
| Annee_Experience | text | 18 | 0.00% | 0.00% | 3 | **16.67%** |
| VILLE_DU_POSTE_DE_TRAVAIL | text | 18 | 0.00% | 0.00% | 5 | **27.78%** |
| PAYS_DU_POSTE_DE_TRAVAIL | text | 18 | 0.00% | 0.00% | 5 | **27.78%** |
| DATE_DE_DEBUT_DE_L_OFFRE | text | 18 | 0.00% | 0.00% | 9 | **50.00%** |
| FILIALE | text | 18 | 0.00% | 100.00% | 1 | **5.56%** |
| INTITULE_DU_POSTE | text | 18 | 0.00% | 0.00% | 18 | **100.00%** |
| SECTEUR | text | 18 | 0.00% | 0.00% | 8 | **44.44%** |
| REFERENCE_STATUT | text | 18 | 0.00% | 0.00% | 18 | **100.00%** |
| URL | text | 18 | 0.00% | 0.00% | 1 | **5.56%** |
| FONCTION | text | 18 | 0.00% | 0.00% | 18 | **100.00%** |
| DESCRIPTION_DU_POSTE | text | 18 | 0.00% | 0.00% | 18 | **100.00%** |
| POSTE | text | 18 | 0.00% | 0.00% | 18 | **100.00%** |
| TYPE_DE_CONTRAT_DU_POSTE | text | 18 | 0.00% | 0.00% | 4 | **22.22%** |
| SOUS | | | | | | |