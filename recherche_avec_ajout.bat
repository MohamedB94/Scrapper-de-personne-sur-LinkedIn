@echo off
:: Configuration pour l'affichage correct des caractères accentués
chcp 65001 > nul
:: Définir les variables d'environnement pour Python et l'encodage
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

echo ================================================
echo RECHERCHE AVEC AJOUT AU FICHIER EXISTANT
echo ================================================
echo.
echo Ce script va rechercher des profils et les ajouter
echo au fichier Excel existant (Resultats_Profils.xlsx)
echo sans supprimer les données précédentes.
echo.

:: Vérifier si le fichier de résultats existe
if exist "Resultats_Profils.xlsx" (
    echo ✓ Fichier de résultats existant trouvé
    echo   Le nouveau contenu sera ajouté à ce fichier
) else (
    echo ℹ  Aucun fichier de résultats existant
    echo   Un nouveau fichier sera créé
)

echo.
set /p job_title="Entrez l'intitulé de poste à rechercher: "

if "%job_title%"=="" (
    echo ❌ Aucun intitulé de poste saisi
    pause
    exit /b 1
)

set /p num_results="Nombre de profils à rechercher (défaut: 5): "
if "%num_results%"=="" set num_results=5

echo.
echo 🔍 Recherche en cours pour: %job_title%
echo 📊 Nombre de résultats: %num_results%
echo.

:: Lancer la recherche en utilisant le fichier existant comme base
if exist "Resultats_Profils.xlsx" (
    python profile_scraper.py --input "Resultats_Profils.xlsx" --output "Resultats_Profils.xlsx" --job "%job_title%" --count %num_results%
) else (
    python profile_scraper.py --output "Resultats_Profils.xlsx" --job "%job_title%" --count %num_results%
)

echo.
echo ================================================
echo RECHERCHE TERMINÉE
echo ================================================
echo.
if exist "Resultats_Profils.xlsx" (
    echo ✅ Résultats sauvegardés dans: Resultats_Profils.xlsx
    echo.
    set /p open_file="Voulez-vous ouvrir le fichier? (o/n): "
    if /i "!open_file!"=="o" (
        start excel "Resultats_Profils.xlsx"
    )
) else (
    echo ❌ Erreur: Aucun fichier de résultats créé
)

echo.
pause
