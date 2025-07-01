@echo off
:: Configuration pour l'affichage correct des caractères accentués
chcp 65001 > nul
echo Vérification de l'installation de Python...

python --version > nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé ou n'est pas dans le PATH.
    echo Veuillez installer Python 3.6 ou supérieur depuis https://www.python.org/downloads/
    echo et vous assurer qu'il est ajouté au PATH système.
    pause
    exit /b 1
)

echo Installation des dépendances Python pour le scraper de profils...
pip install -r requirements.txt
echo Installation terminée!
pause
