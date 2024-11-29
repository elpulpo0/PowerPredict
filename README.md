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

## Lancer le backend et le frontend en //

```bash
bash start.bash
```

## Lancer les tests

```bash
pytest
```

Exemple pour lancer uniquement test_energy_consumption.py :

```bash
pytest _backend/tests/test_energy_consumption.py
```

