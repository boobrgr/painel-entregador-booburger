# painel_despacho.py
import random
import json
import os
import time
from datetime import datetime
import uuid

try:
    import streamlit as st
    st.set_page_config(page_title="Painel de Despacho - Boo Burger", layout="wide")
    STREAMLIT_AVAILABLE = True
except ModuleNotFoundError:
    STREAMLIT_AVAILABLE = False
    print("\n[ERRO] O módulo 'streamlit' não está instalado. Para rodar esse painel, instale com: pip install streamlit\n")

if STREAMLIT_AVAILABLE:
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

    entregadores_default = ["Edimilson", "Lucas", "Mãozinha", "Montanha", "Nino", "Davi Medeiros"]

    zonas = {
        1: ["ALPHAVILLE ABRANTES", "ABRANTES", "CATU DE ABRANTES"],
        2: ["PORTÃO  (FINAL)", "PORTÃO  (ENTRADA)", "ENCONTRO DAS ÁGUAS"],
        3: ["FOZ DO JOANES", "PRAIA DE BURAQUINHO", "BURAQUINHO", "MIRAGEM", "GRANJAS REUNIDAS"],
        4: ["LOTEAMENTO MIRAGEM", "VILAS DO ATLÂNTICO", "FAZENDA PITANGUEIRAS", "BOSQUE DO QUIOSQUE", "MORADA DO SOL"],
        5: ["JARDIM AEROPORTO", "PARQUE JOCKEY CLUBE", "ARACUI", "CENTRO", "VILA PRAIANA", "SANTOS DUMONT", "IPITANGA"],
        6: ["PIATÃ", "ITAPUÃ", "MUSSURUNGA", "TERMINAL DO AEROPORTO", "STELLA MARIS", "SÃO CRISTÓVÃO",
            "PRAIA DO FLAMENGO (depois da Pipa)", "PRAIA DO FLAMENGO (até a Pipa)", "PATAMARES"],
        7: ["JARDIM DAS MARGARIDAS", "ITINGA", "JARDIM PEROLA NEGRA", "JARDIM METRÓPOLE", "PARQUE SANTA RITA",
            "JARDIM TROPICAL", "JARDIM TARUMÃ", "QUINTAS DO PICUAIA", "JARDIM CIDADE NOVA", "JARDIM CENTENÁRIO",
            "POUSO ALEGRE", "PARQUE SANTA JÚLIA", "VILA DE SENNA", "SÃO SALVADOR"],
        8: ["JARDIM IPITANGA", "DIAMANTE", "ÁGUAS FINAS", "VIDA NOVA", "JARDIM MEU IDEAL",
            "JARDIM CARAPINA", "RECREIO DE IPITANGA", "CAJI"]
    }

    DATA_FILE = "pedidos.json"
    ENTREGADORES_FILE = "entregadores.json"

    st.title("🛵 Painel de Despacho - Boo Burger")

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

    pedidos = load_json(DATA_FILE, [])
    entregadores = load_json(ENTREGADORES_FILE, entregadores_default)

    if "fila_entregadores" not in st.session_state:
        st.session_state.fila_entregadores = []

    st.subheader("Entregadores")
    st.markdown("### 🟩 Clique para definir a ordem da fila de entregadores")

    cols = st.columns(len(entregadores))
    for i, (entregador, col) in enumerate(zip(entregadores, cols)):
        if entregador in st.session_state.fila_entregadores:
            pos = st.session_state.fila_entregadores.index(entregador) + 1
            col.markdown(f"**{entregador} ({pos}º)**")
        else:
            if col.button(entregador):
                st.session_state.fila_entregadores.append(entregador)

    novo_nome = st.text_input("+ Novo Entregador", key="novo_entregador")
    if novo_nome and st.button("Adicionar"):
        entregadores.append(novo_nome)
        st.session_state.fila_entregadores.append(novo_nome)
        save_json(ENTREGADORES_FILE, entregadores)

    prontos = sum(p["status"] == "pronto" for p in pedidos)
    despachados = sum(p["status"] == "despachado" for p in pedidos)
    st.sidebar.markdown(f"✅ **Pedidos Prontos:** {prontos}")
    st.sidebar.markdown(f"📤 **Pedidos Despachados:** {despachados}")
