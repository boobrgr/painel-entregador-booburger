# painel_despacho.py
import streamlit as st
import json
import os
import time
import random
import uuid

st.set_page_config(page_title="Painel de Despacho - Boo Burger", layout="wide")

# Dados de teste para pedidos
pedidos = [
    {
        "id": 3001,
        "bairro": "Vilas do Atlântico",
        "zona": 4,
        "status": "em_preparo",
        "entregador": None,
        "hora_criacao": time.time() - 300,
        "prazo_entrega_min": 30,
        "telefone": "(71) 9 9999-0001",
        "consumer_id": "2050",
        "codigo_ifood": "9871",
        "itens": "🍔 Byron x1\n🍟 Batata x1",
        "cliente": "Irineu"
    },
    {
        "id": 3002,
        "bairro": "Vilas do AtlÂntico",
        "zona": 4,
        "status": "em_preparo",
        "entregador": None,
        "hora_criacao": time.time() - 600,
        "prazo_entrega_min": 30,
        "telefone": "(71) 9 9999-0002",
        "consumer_id": "2051",
        "codigo_ifood": "9872",
        "itens": "🍔 Boo x1\n🍟 Batata x2",
        "cliente": "Rebeca"
    },
    {
        "id": 3003,
        "bairro": "Itapuã",
        "zona": 6,
        "status": "em_preparo",
        "entregador": None,
        "hora_criacao": time.time() - 200,
        "prazo_entrega_min": 30,
        "telefone": "(71) 9 9999-0003",
        "consumer_id": "2052",
        "codigo_ifood": "9873",
        "itens": "🍔 Bacon King x1\n🥤 Refri x1",
        "cliente": "Larissa"
    }
]
