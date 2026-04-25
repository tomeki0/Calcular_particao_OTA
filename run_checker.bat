@echo off
setlocal

:: =========================================
:: OTA Super Partition Checker Launcher
:: =========================================

set SCRIPT_DIR=%~dp0
set SCRIPT=ota_super_partition_checker.py

:: ---- CHECK PYTHON ----
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado no sistema.
    echo.
    echo Instale o Python 3.x e marque "Add to PATH".
    echo https://www.python.org/downloads/
    echo.

    :: tenta fallback manual
    if exist "C:\Program Files\Python312\python.exe" (
        set PYTHON_EXE="C:\Program Files\Python312\python.exe"
        echo [INFO] Usando Python manual: %PYTHON_EXE%
    ) else (
        echo [ERRO] Nenhuma versao de Python encontrada.
        pause
        exit /b
    )
) else (
    set PYTHON_EXE=python
)

:: ---- CHECK ADB ----
where adb >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [ERRO] ADB nao encontrado.
    echo.
    echo Instale Android Platform Tools e adicione ao PATH:
    echo https://developer.android.com/tools/releases/platform-tools
    echo.
    pause
    exit /b
)

:: ---- CHECK SCRIPT ----
if not exist "%SCRIPT_DIR%%SCRIPT%" (
    echo.
    echo [ERRO] Script nao encontrado:
    echo %SCRIPT_DIR%%SCRIPT%
    echo.
    pause
    exit /b
)

:: ---- EXECUCAO ----
echo.
echo [INFO] SETUP PASS - Executando ferramenta...
echo.

%PYTHON_EXE% "%SCRIPT_DIR%%SCRIPT%"

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Falha na execucao do script.
    pause
    exit /b
)

echo.
echo =========================================
echo Finalizado com sucesso
echo =========================================

pause