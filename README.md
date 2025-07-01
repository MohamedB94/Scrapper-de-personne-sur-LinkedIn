# Fichier README.md

# Scraper de Profils Professionnels

Ce script permet de rechercher des profils professionnels à partir d'intitulés de postes spécifiques.
Il extrait les noms, prénoms, entreprises et profils LinkedIn pour permettre un contact direct
via LinkedIn.

**🔗 NOUVELLE PHILOSOPHIE : Contact professionnel exclusivement via LinkedIn**

## Prérequis

- Python 3.6 ou supérieur
- Les bibliothèques Python suivantes :
  - pandas
  - selenium
  - webdriver-manager
  - openpyxl (pour le support Excel)

## Installation Rapide

1. Utilisez le menu principal : `menu.bat`
2. Choisissez "Installer les dépendances" (option 4)

Ou manuellement :

```
pip install pandas selenium webdriver-manager openpyxl
```

Chrome doit être installé sur votre système (le script utilise ChromeDriver)

## Utilisation

### Via le Menu Principal (Recommandé)

Exécutez `menu.bat` pour accéder au menu interactif avec toutes les options.

### En ligne de commande

#### Rechercher des profils pour un intitulé de poste spécifique

```
python profile_scraper.py --job "Directeur Marketing" --count 10 --output resultats.xlsx
```

#### Lire les intitulés de postes à partir d'un fichier Excel existant

```
python profile_scraper.py --input Roles_Data.xlsx --output resultats_enrichis.xlsx --count 5
```

### Arguments

- `--input` ou `-i` : Fichier Excel contenant les données existantes
- `--output` ou `-o` : Fichier Excel de sortie (par défaut: "Resultats_Profils.xlsx")
- `--job` ou `-j` : Intitulé de poste à rechercher
- `--count` ou `-c` : Nombre de résultats à récupérer par intitulé de poste (par défaut: 5)

## Structure du fichier Excel

Le script génère un fichier Excel avec les colonnes suivantes :

- **Intitulé de poste** : Le poste recherché
- **Prénom** : Prénom de la personne
- **Nom** : Nom de famille de la personne
- **Entreprise** : Société où travaille la personne
- **LinkedIn** : URL du profil LinkedIn (pour contact direct)
- **Date d'ajout** : Date et heure d'ajout du profil
- **Notes** : Champ libre pour vos annotations

## Migration depuis l'ancienne version

✅ **MIGRATION TERMINÉE** - Si vous aviez d'anciens fichiers Excel avec emails, ils ont été automatiquement mis à jour.

## Remarques importantes

- **🚫 PLUS D'EMAILS** : Ce script ne génère plus d'adresses email
- **🔗 Contact via LinkedIn** : Approche plus professionnelle et éthique
- **⚡ Mode Anti-CAPTCHA** : Utilise des délais humains pour éviter les blocages
- **💾 Sauvegarde automatique** : Les données s'accumulent sans perte
- **🎯 Version simplifiée** : Interface épurée pour usage professionnel

## Avertissement et Éthique

L'utilisation de ce script pour collecter des données personnelles peut être soumise à des restrictions légales selon votre pays. Assurez-vous de respecter le RGPD en Europe ou d'autres lois similaires dans votre juridiction.

**Contact via LinkedIn uniquement** : Cette approche respecte mieux la vie privée et les préférences de contact professionnel des personnes.

Ce script est fourni à des fins éducatives et professionnelles uniquement.
