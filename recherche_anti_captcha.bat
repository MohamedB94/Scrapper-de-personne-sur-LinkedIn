@echo off
:: Configuration pour l'affichage correct des caractères accentués
chcp 65001 > nul
:: Définir les variables d'environnement pour Python et l'encodage
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

echo ================================================
echo RECHERCHE ANTI-CAPTCHA (MODE LENT)
echo ================================================
echo.
echo Ce script utilise des délais plus longs et des
echo techniques spéciales pour éviter les CAPTCHAs.
echo.
echo ⚠️  IMPORTANT: Ce mode est plus lent mais plus fiable
echo     Comptez 2-3 minutes par recherche.
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

echo.
echo ⏱️  CONFIGURATION ANTI-CAPTCHA:
echo    • Délais de frappe humains: ✓
echo    • User-Agent réaliste: ✓
echo    • Navigation progressive: ✓
echo    • Détection de CAPTCHA: ✓
echo    • Fallback simulation: ✓
echo.

set /p num_results="Nombre de profils (max 3 recommandé): "
if "%num_results%"=="" set num_results=3
if %num_results% gtr 5 (
    echo ⚠️  Plus de 5 profils augmente le risque de CAPTCHA
    set /p confirm="Continuer quand même? (o/n): "
    if /i not "!confirm!"=="o" exit /b 1
)

echo.
echo 🔍 Recherche en cours pour: %job_title%
echo 📊 Nombre de résultats: %num_results%
echo ⏳ Mode: Anti-CAPTCHA (lent mais fiable)
echo.
echo 💡 Si un CAPTCHA apparaît, le script basculera automatiquement
echo    en mode simulation pour continuer le travail.
echo.

:: Lancer la recherche en mode anti-CAPTCHA
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
    echo 💡 CONSEILS POUR ÉVITER LES CAPTCHAS:
    echo    • Attendez 5-10 minutes entre les recherches
    echo    • Limitez-vous à 3-5 profils par recherche
    echo    • Variez les intitulés de postes
    echo    • Fermez et rouvrez le navigateur régulièrement
    echo.
    set /p open_file="Voulez-vous ouvrir le fichier de résultats? (o/n): "
    if /i "!open_file!"=="o" (
        start excel "Resultats_Profils.xlsx"
    )
) else (
    echo ❌ Erreur: Aucun fichier de résultats créé
    echo 💡 Essayez le mode simulation en cas de problème persistant
)

echo.
pause
