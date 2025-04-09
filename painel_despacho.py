import streamlit as st
import json
import os
import time
import random
import uuid

st.set_page_config(page_title="Painel de Despacho - Boo Burger", layout="wide")

st.markdown("""
    <style>
        .entregador {
            display: inline-block;
            padding: 10px 20px;
            margin: 5px;
            border-radius: 12px;
            border: 1px solid #ccc;
            background-color: #eee;
            color: #000;
            font-weight: bold;
            cursor: pointer;
        }
        .entregador.selecionado {
            background-color: #28a745 !important;
            color: white;
        }
        .botao-vermelho button {
            background-color: #dc3545 !important;
            color: white;
        }
        .botao-verde button {
            background-color: #28a745 !important;
            color: white;
        }
        .botao-amarelo button {
            background-color: #ffc107 !important;
            color: black;
        }
    </style>
""", unsafe_allow_html=True)

# Defaults
entregadores_default = ["Edimilson", "Lucas", "Mãozinha", "Montanha", "Nino", "Davi Medeiros"]

zonas = {
    1: ["ALPHAVILLE ABRANTES", "ABRANTES", "CATU DE ABRANTES"],
    2: ["PORTÃO  (FINAL)", "PORTÃO  (ENTRADA)", "ENCONTRO DAS ÁGUAS"],
    3: ["FOZ DO JOANES", "PRAIA DE BURAQUINHO", "BURAQUINHO", "MIRAGEM", "GRANJAS REUNIDAS"],
    4: ["LOTEAMENTO MIRAGEM", "VILAS DO ATLÂNTICO", "FAZENDA PITANGUEIRAS", "BOSQUE DO QUIOSQUE", "MORADA DO SOL"],
    5: ["JARDIM AEROPORTO", "PARQUE JOCKEY CLUBE", "ARACUI", "CENTRO", "VILA PRAIANA", "SANTOS DUMONT", "IPITANGA"],
    6: ["PIATÃ", "ITAPUÃ", "MUSSURUNGA", "TERMINAL DO AEROPORTO", "STELLA MARIS", "SÃO CRISTÓVÃO", "PRAIA DO FLAMENGO (depois da Pipa)", "PRAIA DO FLAMENGO (até a Pipa)", "PATAMARES"],
    7: ["JARDIM DAS MARGARIDAS", "ITINGA", "JARDIM PEROLA NEGRA", "JARDIM METRÓPOLE", "PARQUE SANTA RITA", "JARDIM TROPICAL", "JARDIM TARUMÃ", "QUINTAS DO PICUAIA", "JARDIM CIDADE NOVA", "JARDIM CENTENÁRIO", "POUSO ALEGRE", "PARQUE SANTA JÚLIA", "VILA DE SENNA", "SÃO SALVADOR"],
    8: ["JARDIM IPITANGA", "DIAMANTE", "ÁGUAS FINAS", "VIDA NOVA", "JARDIM MEU IDEAL", "JARDIM CARAPINA", "RECREIO DE IPITANGA", "CAJI"]
}

DATA_FILE = "pedidos.json"
ENTREGADORES_FILE = "entregadores.json"

def get_zona(bairro):
    nome = bairro.strip().upper()
    for zona, bairros in zonas.items():
        if nome in bairros:
            return zona
    return None

def load_json(file, default):
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    return default

def save_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def tempo_espera(pedido):
    return int(time.time() - pedido["hora_criacao"])
