#!/bin/bash
# Script para executar a aplicação Streamlit
# Garante que o diretório raiz está no Python path

cd "$(dirname "$0")"
export PYTHONPATH="$(pwd):$PYTHONPATH"
streamlit run src/app.py

