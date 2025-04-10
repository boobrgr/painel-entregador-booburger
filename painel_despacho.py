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

    st.image("https://i.imgur.com/Qr6l0wK.png", width=80)
    st.markdown("<h2 style='margin-top: -10px;'>Painel de Pedidos - <span style='color:#f97316;'>Boo Burger</span></h2>", unsafe_allow_html=True)

    if "fila_entregadores" not in st.session_state:
        st.session_state.fila_entregadores = []

    st.subheader("Entregadores")
    cols = st.columns(len(entregadores_default))
    for i, (entregador, col) in enumerate(zip(entregadores_default, cols), start=1):
        if entregador in st.session_state.fila_entregadores:
            pos = st.session_state.fila_entregadores.index(entregador) + 1
            col.markdown(f"""
                <div style='background-color:#28a745;padding:10px 12px;border-radius:12px;color:white;font-weight:bold;text-align:center;'>
                    {entregador}<br><span style='font-size:12px'>({pos}º)</span>
                </div>
            """, unsafe_allow_html=True)
        else:
            if col.button(entregador, key=f"entregador_{i}"):
                st.session_state.fila_entregadores.append(entregador)
                st.experimental_rerun()

    st.markdown("<hr>", unsafe_allow_html=True)

    # Pedidos de exemplo com base na imagem enviada
    pedidos = [
        {
            "id": 2050,
            "cliente": "Luiza Abreu",
            "bairro": "CENTRO",
            "itens": "🍔 Byron x1\n🍟 Batata x2",
            "codigo_ifood": "9873",
            "hora_criacao": time.time() - 180,
            "prazo_entrega_min": 35,
            "status": "em_preparo",
            "zona": 5
        },
        {
            "id": 2051,
            "cliente": "Irineu",
            "bairro": "CENTRO",
            "itens": "🍔 Boo x1\n🥐 Croissant x1",
            "codigo_ifood": "6543",
            "hora_criacao": time.time() - 240,
            "prazo_entrega_min": 35,
            "status": "em_preparo",
            "zona": 5
        },
        {
            "id": 2052,
            "cliente": "Rebeca",
            "bairro": "MUSSURUNGA",
            "itens": "🍔 Dubbo x1\n🍟 Batata x1",
            "codigo_ifood": "4321",
            "hora_criacao": time.time() - 300,
            "prazo_entrega_min": 30,
            "status": "em_preparo",
            "zona": 6
        },
        {
            "id": 2053,
            "cliente": "Larissa",
            "bairro": "ITAPUÃ",
            "itens": "🍔 Dubbo x1\n🥤 Suco x1",
            "codigo_ifood": "1234",
            "hora_criacao": time.time() - 150,
            "prazo_entrega_min": 30,
            "status": "em_preparo",
            "zona": 6
        }
    ]

    cor_zona = {
        5: "#d1f4ff",
        6: "#fff1ba"
    }

    def tempo_restante(pedido):
        tempo = int(time.time() - pedido['hora_criacao'])
        restante = pedido['prazo_entrega_min'] * 60 - tempo
        return max(0, int(restante // 60))

    st.markdown("<h4>Pedidos :</h4>", unsafe_allow_html=True)

    card_colunas = st.columns(4)
    for i, pedido in enumerate(pedidos):
        cor = cor_zona.get(pedido['zona'], '#ffffff')
        restante = tempo_restante(pedido)
        with card_colunas[i % 4]:
            st.markdown(f"""
                <div style='background-color:{cor}; border-radius:16px; padding:16px; margin-bottom:20px; box-shadow:0 2px 6px rgba(0,0,0,0.1);'>
                    <strong>Pedido:</strong> {pedido['id']}<br>
                    <strong>Ifood:</strong> #{pedido['codigo_ifood']}<br>
                    <strong>Cliente:</strong> {pedido['cliente']}<br>
                    <strong>Bairro:</strong> {pedido['bairro']}<br>
                    <div style='margin: 6px 0; font-size:15px;'>{pedido['itens'].replace(chr(10), '<br>')}</div>

                    <div style='width:60px;height:60px;border-radius:50%;border:8px solid #444;background:#fff;margin:auto;display:flex;align-items:center;justify-content:center;font-weight:bold;font-size:16px;'>
                        {restante}<br><span style='font-size:10px;'>min</span>
                    </div>

                    <div style='display:flex;justify-content:center;gap:8px;margin-top:8px;'>
                        <button style='background:#28a745;border:none;color:#fff;padding:6px 10px;border-radius:8px;'>Pronto</button>
                        <button style='background:#ffc107;border:none;color:#000;padding:6px 10px;border-radius:8px;'>Saiu para Entrega</button>
                    </div>

                    <div style='font-size:11px; text-align:center; margin-top:8px;'>
                        Início: {datetime.fromtimestamp(pedido['hora_criacao']).strftime('%H:%M')}<br>
                        Previsão: {datetime.fromtimestamp(pedido['hora_criacao'] + pedido['prazo_entrega_min']*60).strftime('%H:%M')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
