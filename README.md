# PowerPredict
Prédiction de la consommation d'énergie d'un bâtiment

## Créer un environement virtuel

```python -m venv __venv```

## Activer l'environement virtuel

- mac/linux:
`source __venv/bin/activate.fish`
- windows:
`__venv/Scripts/activate` or `__venv/Scripts/activate.ps1` 
- bash(windows):
`source __venv/Scripts/activate`

## Installer les dépendances

```bash
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
```

## Désactiver l'environnement virtuel

`deactivate`

## Lancer le backend

```bash
cd _backend
uvicorn App:app --reload
```

## Lancer les tests

exemple pour test_energy_consumption.py :

```bash
cd /path/to/PowerPredict
pytest tests/test_energy_consumption.py
```

