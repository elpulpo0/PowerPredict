# PowerPredict
Prédiction de la consommation d'énergie d'un bâtiment

## Description
**PowerPredict** est une application web permettant de visualiser et de prédire la consommation énergétique de bâtiments. Elle combine un backend pour distribue une API et un frontend interactif pour offrir une interface utilisateur.

---

## Architecture de l'application

PowerPredict est structurée en deux parties principales :

1. **Backend :**
   - Écrit en Python.
   - Fournit des endpoints pour récupérer et traiter les données de consommation énergétique.

2. **Frontend :**
   - Développé avec Streamlit.
   - Offre une interface utilisateur pour saisir des paramètres, afficher des graphiques et visualiser les prédictions.

### Schéma de l'architecture :

`[Frontend (Streamlit)] <---> [Backend (FastAPI)] <---> [Base de données (SQLite)]`

---

## Choix techniques

1. **Langage principal :**
   - Python

2. **Frontend :**
   - Streamlit

3. **Backend :**
   - FastAPI

4. **Base de données :**
   - SQLite

5. **Tests :**
   - Pytest

---

## API utilisée

L'application interagit avec l'es 'API suivante :
- **PowerPredict API (API interne)** : Fournit les données de consommation d'énergie selon les filtres appliqués.

### Exemple d'appel à l'API :
```bash
GET https://powerpredict.onrender.com/data?region=guadeloupe&zone_climatique=GUA
```

---

## Instructions d'installation et d'utilisation

### Créer un environement virtuel

```python -m venv __venv```

### Activer l'environement virtuel

- mac/linux:
`source __venv/bin/activate.fish`
- windows:
`__venv/Scripts/activate` or `__venv/Scripts/activate.ps1` 
- bash(windows):
`source __venv/Scripts/activate`

### Installer les dépendances

```bash
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
```

### Lancer le backend seul

```bash
cd _backend
uvicorn App:app --reload
```

### Lancer le frontend seul

```bash
cd _frontend
streamlit run main.py
```

### Lancer le backend et le frontend en //

```bash
bash start.bash
```

### Lancer les tests

```bash
pytest
```

### Exemple pour lancer uniquement test_energy_consumption.py :

```bash
pytest _backend/tests/test_energy_consumption.py
```

---

## Fonctionnalités principales

1. Visualisation des données de consommation d'énergie en fonction de la région et de la zone climatique.
2. Filtrage dynamique basé sur des critères (ex. : année, région, zone climatique).
3. Prédictions énergétiques basées sur des modèles intégrés ou API externes.

---

# Structure du projet PowerPredict

| Arborescence       | Description                                         |
|--------------------|-----------------------------------------------------|
| 📂 PowerPredict 
| ├── 📂 _backend        | Code source du backend                              |
| │   ├── api            | Fichiers relatifs aux endpoints API                 |
| │   ├── tests          | Tests unitaires                                     |
| │   ├── database       | Fichiers concernant la création de la base de données |
| │   └── models         | Fichiers relatifs à l'entraînement des modèles      |
| ├── 📂 _frontend       | Code source du frontend (Streamlit)                 |
| │   ├── main           | Point d'entrée de l'application Streamlit           |
| │   └── fonctions      | Fonctions pour l'interface                          |
| ├── requirements       | Dépendances Python                                  |
| ├── start              | Script de démarrage (backend + frontend)            |
| ├── README             | Documentation de l'application                     |
