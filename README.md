# 🚕 NYC Yellow Taxi – ELT Pipeline sur GCP (BigQuery, GCS, Airflow, SQL & Analytics)

## 📌 Présentation du projet
Ce projet met en œuvre un **pipeline ELT complet sur Google Cloud Platform (GCP)** à partir des données publiques des **NYC Yellow Taxi Trips**.

L’objectif est de couvrir **l’ensemble du cycle de vie de la donnée** :
- ingestion automatisée
- stockage cloud
- chargement analytique
- transformations SQL
- orchestration avec Airflow (Cloud Composer)
- analyse exploratoire
- visualisation
- préparation à des usages Machine Learning

Ce projet peut servir de **référence reproductible** pour construire un pipeline ELT moderne sur GCP.

---

## 🏗️ Architecture globale
```
Source (NYC Taxi Parquet)
|
v
Google Cloud Storage (GCS)
|
v
BigQuery (RAW)
|
v
BigQuery (TRANSFORMED)
|
v
Vues analytiques (SQL)
|
v
Notebooks Python BigQuery
|
v
(BigQuery ML - extension future)
```

---

## 🧱 Stack technologique
- **Google Cloud Storage (GCS)** : stockage des fichiers bruts
- **BigQuery** : entrepôt de données analytique
- **Cloud Composer (Airflow 2)** : orchestration ELT
- **Python** : ingestion, automatisation
- **SQL BigQuery** : transformations, vues analytiques
- **BigQuery Notebooks (Python)** : analyse et visualisation

---

## 1️⃣ Extraction des données (Extract)

### 🎯 Source
Les données proviennent du site officiel NYC Taxi (format Parquet) :
- Yellow Taxi Trips (mensuels)

### 📄 Script principal
`download_taxi_data.py`

### 🔧 Fonctionnement
- Télécharge les fichiers Parquet depuis la source officielle
- Vérifie si le fichier existe déjà dans GCS (idempotence)
- Upload direct vers GCS
- Génère des logs stockés dans GCS

### ▶️ Exécution (manuelle)
```bash
python download_taxi_data.py
```

## 2️⃣ Stockage des données (GCS)

📦 Bucket
```
gs://<PROJECT_ID>-data-bucket/
```

📂 Structure
```
dataset/
 └── trips/           # fichiers parquet taxi
from-git/
 ├── download_taxi_data.py
 ├── load_raw_trips_data.py
 ├── transform_trips_data.py
 └── logs/
```

## 3️⃣ Chargement BigQuery (Load)

📄 Script
```
load_raw_trips_data.py
```
🎯 **Objectif**

Charger les fichiers Parquet depuis GCS vers BigQuery sans doublons.

🔧 **Fonctionnement**

- Liste les fichiers Parquet présents dans GCS

- Compare avec les fichiers déjà chargés (champ source_file)

- Charge chaque fichier dans une table temporaire

- Insère les données dans la table finale RAW

- Supprime la table temporaire

📊 Table cible
```
raw_yellowtrips.trips
```

## 4️⃣ Création des datasets BigQuery

📄 Script
```
create_datasets.py
```
📁 Datasets créés

- raw_yellowtrips → données brutes

- transformed_data → données nettoyées

- views_fordashboard → vues analytiques

▶️ Exécution
```
python create_datasets.py
```

## 5️⃣ Transformation des données (Transform)

📄 Script
```
transform_trips_data.py
```
🎯 **Objectif**

Nettoyer et filtrer les données pour un usage analytique.

🔧 Règles appliquées

- passenger_count > 0

- trip_distance > 0

- total_amount > 0

- exclusion des paiements invalides

📊 Table cible
```
transformed_data.cleaned_and_filtered
```

## 6️⃣ Orchestration ELT avec Airflow (Cloud Composer)

📄 DAG
```
elt_dag_pipeline.py
```
🧩 **Étapes du pipeline**

* Téléchargement des données → GCS

* Chargement BigQuery RAW

* Transformation BigQuery

🔁 **Exécution**

- Déployé dans le bucket dags/ de Cloud Composer

- Déclenché manuellement ou via scheduling

- Gestion des retries et des logs

🟢 **Résultat**

Pipeline entièrement automatisé et stable dans Cloud Composer.

## 7️⃣ Création de vues analytiques (SQL)

🎯 **Objectif**

Préparer des objets directement exploitables pour :

- dashboards

- notebooks

- analyses métiers

🧠 **Exemples de vues créées**

📈 Demande dans le temps
```
views_fordashboard.demand_over_time
```
- analyse journalière, hebdomadaire, mensuelle

- saisonnalité et tendances

⏰ Heures de pointe par zone
```
views_fordashboard.peak_hours_by_zone
```
- jointure avec la table de référence des zones

- analyse horaire par borough et zone

## 8️⃣ Analyse & visualisation avec BigQuery Notebooks

📓 **Contenu**

- Connexion native BigQuery → DataFrame

- Analyse exploratoire

- Visualisations (tendances, distributions, comparaisons)

- Préparation de features analytiques

🎯 **Avantages**

- Pas de data export

- Scalabilité BigQuery

- Workflow Data Analyst / Data Scientist intégré

## 9️⃣ Ouverture vers le Machine Learning (BigQuery ML)

🔮 **Perspectives**

Le projet est prêt pour :

- enrichissement externe (météo, jours fériés)

- création de features SQL

- modèles BigQuery ML (régression / classification)

**Exemples** :

- prédiction du nombre de courses journalières

- prédiction du montant total des trajets

# 🚀 Conclusion

Ce projet démontre la mise en place complète d’un pipeline ELT cloud-native, de l’ingestion jusqu’à l’analyse avancée, en utilisant les outils standards de l’écosystème GCP.

Il constitue une base solide et réutilisable pour tout projet Data Engineering / Analytics sur Google Cloud.

# 👤 Auteur

Mamadou DIEDHIOU

Data Analyst / Chargé d'études statistiques/ Data Engineer
