@echo off
:: Configuration pour l'affichage correct des caractères accentués
chcp 65001 > nul

:menu
cls
echo ================================================
echo    MENU PRINCIPAL - SCRAPER DE PROFILS
echo ================================================
echo.
echo Choisissez une action:
echo.
echo 1. 🚀 Rechercher des profils (rapide)
echo 2. 🐌 Recherche anti-CAPTCHA (lent mais fiable)
echo 3. ✏️  Ajouter des profils manuellement
echo 4. ⚙️  Installer les dépendances
echo 5. ❓ Aide et documentation
echo 0. 🚪 Quitter
echo.
set /p choice="Votre choix (0-5): "

if "%choice%"=="1" goto recherche
if "%choice%"=="2" goto recherche_anticaptcha
if "%choice%"=="3" goto ajout_manuel
if "%choice%"=="4" goto installation
if "%choice%"=="5" goto aide
if "%choice%"=="0" goto quitter

echo ❌ Choix invalide. Veuillez choisir entre 0 et 5.
pause
goto menu

:recherche
echo.
echo 🔍 Lancement de la recherche de profils (mode rapide)...
echo.
set /p job_title="Intitulé de poste à rechercher: "
set /p count="Nombre de profils à extraire (défaut: 5): "
if "%count%"=="" set count=5
python profile_scraper_2024.py --job "%job_title%" --count %count% --output "Resultats_Profils.xlsx"
pause
goto menu

:recherche_anticaptcha
echo.
echo 🐌 Lancement de la recherche anti-CAPTCHA (mode lent)...
echo.
set /p job_title="Intitulé de poste à rechercher: "
set /p count="Nombre de profils à extraire (défaut: 5): "
if "%count%"=="" set count=5
python profile_scraper_2024.py --job "%job_title%" --count %count% --output "Resultats_Profils.xlsx" --slow
pause
goto menu

:ajout_manuel
echo.
echo ✏️ Ajout manuel d'un profil professionnel
echo.
set /p job_title="Intitulé de poste: "
set /p firstname="Prénom: "
set /p lastname="Nom: "
set /p company="Entreprise: "
set /p linkedin="URL LinkedIn (optionnel): "
set /p notes="Notes (optionnel): "

echo.
echo Ajout du profil: %firstname% %lastname% (%company%)...
echo.

python -c "import pandas as pd; from datetime import datetime; data = pd.DataFrame({'Intitulé de poste': ['%job_title%'], 'Prénom': ['%firstname%'], 'Nom': ['%lastname%'], 'Entreprise': ['%company%'], 'LinkedIn': ['%linkedin%'], 'Date d''ajout': [datetime.now().strftime('%%Y-%%m-%%d %%H:%%M:%%S')], 'Notes': ['%notes%']}); try: old_data = pd.read_excel('Resultats_Profils.xlsx'); data = pd.concat([old_data, data], ignore_index=True); except: pass; data.to_excel('Resultats_Profils.xlsx', index=False); print('✓ Profil ajouté avec succès')"

pause
goto menu

:installation
echo.
echo ⚙️ Installation des dépendances...
echo.
call install_dependencies.bat
pause
goto menu

:aide
cls
echo ================================================
echo               AIDE ET DOCUMENTATION
echo ================================================
echo.
echo 📖 DOCUMENTATION:
echo.
echo • README.md - Documentation complète du projet
echo.
echo 🎯 UTILISATION RAPIDE:
echo.
echo 1. Commencez par "Installer les dépendances" (option 4)
echo 2. Utilisez "Rechercher des profils" (option 1) pour mode rapide
echo 3. Utilisez "Recherche anti-CAPTCHA" (option 2) si vous rencontrez des CAPTCHAs
echo 4. Utilisez "Ajouter des profils manuellement" (option 3) pour saisie directe
echo.
echo 📊 FICHIER DE RÉSULTATS:
echo • Tous les profils sont sauvés dans "Resultats_Profils.xlsx"
echo • Structure: Intitulé, Prénom, Nom, Entreprise, LinkedIn, Date, Notes
echo • Le fichier s'enrichit à chaque recherche sans perte de données
echo.
echo 🧩 STRUCTURE DU PROJET:
echo • profile_scraper_2024.py - Script principal d'extraction
echo • Resultats_Profils.xlsx - Fichier de résultats
echo • Roles_Data.xlsx - Liste de rôles pour recherche multiple (optionnel)
echo • requirements.txt - Liste des dépendances Python
echo.
echo 📋 OPTIONS DE RECHERCHE:
echo • Mode rapide: Extraction standard des profils
echo • Mode anti-CAPTCHA: Délais plus longs pour éviter les détections
echo • Ajout manuel: Saisie directe des informations de profil
echo.
pause
goto menu
echo 🔍 ANTI-CAPTCHA:
echo • Le mode anti-CAPTCHA (option 2) est plus lent mais évite les blocages
echo • Il utilise des délais humains et bascule en simulation si nécessaire
echo • Recommandé si vous voyez des CAPTCHAs avec le mode rapide
echo.
pause
goto menu

:quitter
echo.
echo 👋 Merci d'avoir utilisé le scraper de profils!
echo.
pause
exit
