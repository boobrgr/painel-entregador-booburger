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
            body {
                background-color: #000;
            }
            .top-bar {
                background-color: #000;
                color: white;
                text-align: center;
                padding: 10px 0;
                font-size: 24px;
                font-weight: bold;
                letter-spacing: 1px;
                margin-bottom: 20px;
            }
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
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class='top-bar'>
            <img src='https://i.imgur.com/Qr6l0wK.png' width='40' style='vertical-align: middle; margin-right:10px;'>
            Boo Burger - Painel de Despacho
        </div>
    """, unsafe_allow_html=True)

    entregadores_default = ["Edimilson", "Lucas", "Mãozinha", "Montanha", "Nino", "Davi Medeiros"]

    if "fila_entregadores" not in st.session_state:
        st.session_state.fila_entregadores = []

    st.markdown("<div style='display:flex;justify-content:center;gap:10px;margin-bottom:20px;'>", unsafe_allow_html=True)
    for i, nome in enumerate(entregadores_default):
        selecionado = nome in st.session_state.fila_entregadores
        posicao = st.session_state.fila_entregadores.index(nome)+1 if selecionado else ""
        cor = "#28a745" if selecionado else "#eee"
        texto = f"{nome} ({posicao}º)" if selecionado else nome
        if st.button(texto, key=f"entregador_btn_{i}"):
            if not selecionado:
                st.session_state.fila_entregadores.append(nome)
        st.markdown(f"<style>#entregador_btn_{i}{{background-color:{cor};color:{'white' if selecionado else 'black'};border-radius:12px;}}</style>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

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

    def tempo_restante(pedido):
        tempo = int(time.time() - pedido['hora_criacao'])
        restante = pedido['prazo_entrega_min'] * 60 - tempo
        return max(0, int(restante // 60))

    card_colunas = st.columns(4)

    pedidos.sort(key=lambda p: (p['status'] != 'em_preparo', p['hora_criacao']))
    for i, pedido in enumerate(pedidos):
        restante = tempo_restante(pedido)
        status_cor = '#dc3545' if pedido['status'] == 'em_preparo' else ('#28a745' if pedido['status'] == 'pronto' else '#ffc107')
        with card_colunas[i % 4]:
            st.markdown(f"""
                <div style='background:#fff;border-radius:20px;padding:14px;margin-bottom:20px;box-shadow:0 2px 8px rgba(0,0,0,0.15); opacity:0.4;' if pedido['status'] != 'em_preparo' else "<div style='background:#fff;border-radius:20px;padding:14px;margin-bottom:20px;box-shadow:0 2px 8px rgba(0,0,0,0.15);'">
                    <div style='display:flex;justify-content:space-between;'>
                        <div><strong>Pedido:</strong> {pedido['id']}</div>
                        {'<span style=\'color:red;font-weight:bold;cursor:pointer;\'>❌</span>' if not st.button(f'Remover {pedido["id"]}', key=f'remove_{pedido["id"]}') else pedidos.pop(i)}
                    </div>
                    <div style='margin-top:4px;'>
                        <strong>Ifood:</strong> #{pedido['codigo_ifood']}<br>
                        <strong>Cliente:</strong> {pedido['cliente']}<br>
                        <strong>Bairro:</strong> {pedido['bairro']}
                    </div>
                    <div style='margin:10px 0;font-size:15px;'>{pedido['itens'].replace(chr(10), '<br>')}</div>
                    <div style='width:65px;height:65px;border-radius:50%;border:6px solid {status_cor};background:#fff;margin:auto;display:flex;flex-direction:column;align-items:center;justify-content:center;font-weight:bold;font-size:15px;'>
                        <div>{restante}</div><div style='font-size:10px;'>min</div>
                    </div>
                    <div style='display:flex;justify-content:center;gap:8px;margin-top:10px;'>
                        {st.button('✅ Pronto', key=f'pronto_{pedido["id"]}') and pedido.update({'status': 'pronto'}) or ''}
                        {st.button('🚚 Saiu', key=f'despachado_{pedido["id"]}') and pedido.update({'status': 'despachado'}) or ''}
                    </div>
                    <div style='font-size:11px;text-align:center;margin-top:8px;'>
                        Início: {datetime.fromtimestamp(pedido['hora_criacao']).strftime('%H:%M')}<br>
                        Previsão: {datetime.fromtimestamp(pedido['hora_criacao'] + pedido['prazo_entrega_min']*60).strftime('%H:%M')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
