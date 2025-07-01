# LinkedIn Profile Scraper

## Description

Ce projet permet d'extraire des profils LinkedIn à partir de recherches Google, en se basant sur des intitulés de postes. Il extrait les noms, prénoms et entreprises des profils trouvés, puis les enregistre dans un fichier Excel.

## Fonctionnalités

- Recherche de profils LinkedIn par intitulé de poste
- Extraction fiable des noms, prénoms et entreprises
- Validation des données pour éviter les valeurs génériques
- Export des résultats au format Excel
- Protection contre les CAPTCHA de Google

## Prérequis

- Python 3.6 ou supérieur
- Google Chrome installé
- Les bibliothèques Python suivantes :
  - pandas
  - selenium
  - webdriver-manager
  - openpyxl
  - argparse
  - requests

## Fichiers du projet

- `profile_scraper_2024.py` - Script principal pour l'extraction de profils
- `Resultats_Profils.xlsx` - Fichier de résultats (créé automatiquement)
- `Roles_Data.xlsx` - Fichier contenant des rôles à rechercher (optionnel)
- `requirements.txt` - Liste des dépendances Python
- `menu.bat` - Menu interactif pour faciliter l'utilisation
- `install_dependencies.bat` - Script d'installation des dépendances

## Installation

```bash
# Installer les dépendances requises
pip install selenium pandas openpyxl
```

## Utilisation

### Recherche simple

```bash
python profile_scraper_2024.py --job "data engineer" --count 10 --output "Resultats_Profils.xlsx"
```

### Options disponibles

- `--job` ou `-j` : Intitulé du poste à rechercher
- `--count` ou `-c` : Nombre de résultats à extraire (défaut: 5)
- `--output` ou `-o` : Fichier Excel de sortie (défaut: "Resultats_Profils.xlsx")
- `--input` ou `-i` : Fichier Excel existant à enrichir (optionnel)
- `--slow` : Mode lent avec délais supplémentaires pour éviter les CAPTCHA

### Modes de recherche

#### Mode rapide (par défaut)

```bash
python profile_scraper_2024.py --job "data engineer" --count 10
```

#### Mode anti-CAPTCHA (lent mais plus fiable)

```bash
python profile_scraper_2024.py --job "data engineer" --count 10 --slow
```

Ce mode utilise des délais plus longs entre les actions pour éviter d'être détecté comme un robot.

## Exemple de résultats

Le script génère un fichier Excel avec les colonnes suivantes:

- Intitulé de poste
- Prénom
- Nom
- Entreprise
- LinkedIn (URL du profil)
- Date d'ajout
- Notes

## Performance

- Le scraper utilise une approche multistratégie pour s'adapter aux changements de structure de Google
- Les techniques anti-détection minimisent les risques de rencontrer des CAPTCHA
- Les patterns d'extraction sont optimisés pour reconnaître divers formats de profils LinkedIn

## Résolution de problèmes

- Si vous rencontrez des CAPTCHA, essayez d'exécuter le script moins fréquemment
- Pour améliorer la qualité des résultats, ajustez le nombre de profils recherchés
- En cas de problème d'extraction, vérifiez que Chrome est bien installé et à jour

## Notes importantes

- Ce script respecte les conditions d'utilisation de Google et LinkedIn en limitant la fréquence des requêtes
- L'extraction est basée uniquement sur les informations publiquement accessibles via Google
- Le scraper est configuré pour éviter la détection automatique et minimiser l'impact sur les serveurs

## Exemple d'exécution réussie

```
🔍 Recherche Google pour: data engineer
📄 Chargement de Google...
✓ Consentement cookies accepté
🔤 Recherche tapée: site:linkedin.com/in/ data engineer
📊 Analyse des résultats...
✓ 20 liens LinkedIn trouvés
  📄 Analyse du profil 1...
    ✓ Profil extrait: Jean-Baptiste Braun chez KLM
  📄 Analyse du profil 2...
    ✓ Profil extrait: Sandro Gazzo chez eXalt
  📄 Analyse du profil 3...
    ✓ Profil extrait: Alexis Da Costa chez Devoteam A Cloud
```
