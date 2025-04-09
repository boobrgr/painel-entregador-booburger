# painel_entregador.py
import streamlit as st
import json
import os
import time

DATA_FILE = "pedidos.json"
USUARIOS_FILE = "usuarios.json"

st.set_page_config(page_title="App do Entregador - Boo Burger", layout="wide")
st.title("📦 App do Entregador")

# Função auxiliar para carregar JSON
def load_json(file, default):
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    return default

# Login do entregador
cpf = st.text_input("Digite seu CPF para login")
usuarios = load_json(USUARIOS_FILE, [])
nome_entregador = next((u["nome"] for u in usuarios if u["cpf"] == cpf), None)

if nome_entregador:
    st.success(f"Entregador logado: {nome_entregador}")
    pedidos = load_json(DATA_FILE, [])

    pedidos_entregador = [
        p for p in pedidos
        if p.get("entregador") == nome_entregador and p.get("status") in ["pronto", "despachado"]
    ]

    if pedidos_entregador:
        for pedido in pedidos_entregador:
            tempo = int(time.time() - pedido["hora_criacao"])
            restante = pedido.get("prazo_entrega_min", 30) * 60 - tempo
            restante_min = max(0, int(restante // 60))

            with st.container():
                st.markdown(f"""
                    <div style='background-color:#f0f0f0; border-radius:10px; padding:15px; margin-bottom:10px;'>
                        <strong>Pedido #{pedido['id']}</strong><br>
                        Bairro: {pedido['bairro']}<br>
                        Telefone: {pedido['telefone']}<br>
                        Código Ifood: {pedido['codigo_ifood']}<br>
                        Tempo restante: <strong>{restante_min} min</strong>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Nenhum pedido pronto ou despachado disponível para você ainda.")

else:
    st.warning("Informe um CPF válido para visualizar os pedidos.")
