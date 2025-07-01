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
call recherche_avec_ajout.bat
pause
goto menu

:recherche_anticaptcha
echo.
echo 🐌 Lancement de la recherche anti-CAPTCHA (mode lent)...
echo.
call recherche_anti_captcha.bat
pause
goto menu

:ajout_manuel
echo.
echo ✏️ Lancement de l'ajout manuel de profils...
echo.
call ajouter_profils.bat
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
echo 📖 GUIDES DISPONIBLES:
echo.
echo • README.md - Documentation complète
echo • STRUCTURE_PROJET.md - Structure des fichiers
echo.
echo 🎯 UTILISATION RAPIDE:
echo.
echo 1. Commencez par "Installer les dépendances" (option 4)
echo 2. Utilisez "Recherche anti-CAPTCHA" (option 2) si vous avez des CAPTCHAs
echo 3. Sinon utilisez "Rechercher des profils" (option 1) pour plus rapide
echo 4. Ou "Ajouter des profils manuellement" (option 3) pour saisie manuelle
echo.
echo 📊 FICHIER DE RÉSULTATS:
echo • Tous les profils sont sauvés dans "Resultats_Profils.xlsx"
echo • Structure: Intitulé, Prénom, Nom, Entreprise, LinkedIn, Date, Notes
echo • ❌ PLUS D'EMAILS - Contact direct via LinkedIn uniquement
echo • Le fichier s'enrichit à chaque recherche sans perte de données
echo.
echo 🔗 NOUVELLE PHILOSOPHIE:
echo • Plus de génération ou enrichissement d'emails
echo • Contact professionnel direct via LinkedIn
echo • Plus éthique et conforme aux attentes actuelles
echo • Données LinkedIn réelles extraites des profils
echo.
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
