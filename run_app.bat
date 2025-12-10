@echo off
REM Script para executar a aplicação Streamlit
REM Garante que o diretório raiz está no Python path

cd /d "%~dp0"
set PYTHONPATH=%CD%;%PYTHONPATH%
streamlit run src/app.py

