@echo off
REM Script de démarrage rapide pour développeurs
REM Outil de Maintenance Système v2.1

cls
echo.
echo ========================================
echo  DEMARRAGE RAPIDE
echo  Outil de Maintenance Systeme v2.1
echo ========================================
echo.

REM Vérifier si l'environnement virtuel existe
if not exist "venv\Scripts\activate.bat" (
    echo [1/3] Creation de l'environnement virtuel...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERREUR: Impossible de creer l'environnement virtuel
        echo Verifiez que Python est installe
        pause
        exit /b 1
    )
    echo ✓ Environnement virtuel cree
) else (
    echo [1/3] Environnement virtuel deja present
)

echo.
echo [2/3] Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

echo.
echo [3/3] Installation des dependances...
pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo ERREUR: Impossible d'installer les dependances
    pause
    exit /b 1
)
echo ✓ Dependances installees

echo.
echo ========================================
echo  PRET!
echo ========================================
echo.
echo Commandes disponibles:
echo   - Lancer l'application:     python src\OutilMaintenance.py
echo   - Creer l'executable:       cd build_tools ; python build.py
echo   - Desactiver venv:          deactivate
echo.
echo Environnement virtuel active.
echo.

cmd /k
