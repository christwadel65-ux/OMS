@echo off
REM Script de build rapide pour Outil de Maintenance Système
REM Auteur: c.Lecomte

cd ..

echo ========================================
echo  BUILD - Outil Maintenance v2.1
echo ========================================
echo.

echo [1/2] Compilation avec PyInstaller...
python build_tools\build.py
if %errorlevel% neq 0 (
    echo.
    echo ERREUR: La compilation a echoue.
    pause
    exit /b 1
)

echo.
echo.
echo ========================================
echo  BUILD TERMINE!
echo ========================================
echo.
echo L'executable se trouve dans: dist\OutilMaintenance\
echo.
echo Prochaine etape:
echo   - Testez l'executable
echo   - Compilez build_tools\setup.iss avec Inno Setup
echo.
pause
