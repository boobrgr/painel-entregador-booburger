# painel_entregador.py
import streamlit as st
import json
import os
import time

st.set_page_config(page_title="Painel do Entregador - Boo Burger", layout="wide")
st.title("📦 Painel do Entregador - Boo Burger")

DATA_FILE = "pedidos.json"
ENTREGADORES_FILE = "entregadores.json"

# Funções utilitárias
def load_json(file, default):
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    return default

def tempo_restante(pedido):
    prazo_segundos = pedido.get("prazo_entrega_min", 30) * 60
    restante = prazo_segundos - (time.time() - pedido["hora_criacao"])
    return max(0, int(restante))

# Carrega dados
pedidos = load_json(DATA_FILE, [])
entregadores = load_json(ENTREGADORES_FILE, [])

# Seleção de entregador com sessão
if "entregador_logado" not in st.session_state:
    st.subheader("🔐 Selecione seu nome")
    st.session_state.entregador_logado = st.selectbox("Entregador", entregadores)
    st.stop()

# Mostra entregador logado
entregador = st.session_state.entregador_logado
st.success(f"🧍 Entregador: {entregador}")
if st.button("Trocar entregador"):
    del st.session_state.entregador_logado
    st.experimental_rerun()

# Filtra pedidos despachados para este entregador
meus_pedidos = [p for p in pedidos if p.get("status") == "despachado" and p.get("entregador") == entregador]

if not meus_pedidos:
    st.info("Nenhum pedido atribuído a você no momento.")
else:
    for pedido in meus_pedidos:
        restante = tempo_restante(pedido)
        progresso = max(0, min(100, 100 - (restante / (pedido.get("prazo_entrega_min", 30) * 60)) * 100))
        cor = "#28a745" if progresso > 60 else ("#ffc107" if progresso > 30 else "#dc3545")

        with st.container():
            st.markdown(f"""
                <div style='background-color:#f9f9f9; border-left: 8px solid {cor}; border-radius:12px; padding:16px; margin-bottom:12px;'>
                    <strong>Pedido #{pedido['id']} - {pedido['bairro']}</strong><br>
                    ⏱️ Tempo restante: <strong>{restante // 60} min</strong><br>
                    📞 Telefone: <code>{pedido['telefone']}</code><br>
                    🧾 Código Ifood: <code>{pedido['codigo_ifood']}</code><br>
                    <a href="https://confirmacao-entrega-propria.ifood.com.br/numero-pedido" target="_blank">🔗 Confirmar no Ifood</a>
                </div>
            """, unsafe_allow_html=True)
