@echo off
chcp 65001 >nul

:: 🎮 ATLAS CONSOLE - Atalho para Windows
:: Studio Agent Integration System
:: Versão: 2.0.0

:: Verificar se PowerShell está disponível
where powershell >nul 2>&1
if %ERRORLEVEL% equ 0 (
    :: Executar com PowerShell
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0ATLAS_CONSOLE.ps1"
) else (
    :: Tentar com cmd
    echo ❌ PowerShell não encontrado!
    echo.
    echo Tente um destes métodos:
    echo.
    echo 1. Instale o PowerShell:
    echo    https://aka.ms/PSWindows
    echo.
    echo 2. Execute diretamente:
    echo    powershell -File "%~dp0ATLAS_CONSOLE.ps1"
    echo.
    echo 3. Use o console Linux:
    echo    bash ATLAS_CONSOLE_QUICK.sh
    echo.
    pause
)
