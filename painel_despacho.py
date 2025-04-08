# painel_despacho.py
import streamlit as st
import json
import os
import time
import uuid
import random

st.set_page_config(page_title="Painel de Despacho - Boo Burger", layout="wide")
st.title("🍔 Painel de Despacho - Boo Burger")

DATA_FILE = "pedidos.json"
ENTREGADORES_FILE = "entregadores.json"

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

def get_zona(bairro):
    return 1  # Simulado para exibição

# Carrega ou inicializa os dados
entregadores = load_json(ENTREGADORES_FILE, ["Edimilson", "Lucas", "Mãozinha", "Montanha", "Nino"])
pedidos = load_json(DATA_FILE, [])

# Gera pedidos simulados caso esteja vazio
if not pedidos:
    for i in range(5):
        bairro = f"Bairro {i+1}"
        id_full = str(uuid.uuid4())
        pedidos.append({
            "id": i + 1,
            "bairro": bairro,
            "zona": get_zona(bairro),
            "status": "em_preparo",
            "entregador": None,
            "hora_criacao": time.time(),
            "prazo_entrega_min": 30,
            "telefone": f"(71) 9{random.randint(8000,9999)}-{random.randint(1000,9999)}",
            "consumer_id": id_full,
            "codigo_ifood": id_full[-8:]
        })
    save_json(DATA_FILE, pedidos)

# Seleção de entregador
if "entregador_selecionado" not in st.session_state:
    st.session_state.entregador_selecionado = entregadores[0]

entregador = st.selectbox("Entregador ativo", entregadores, index=entregadores.index(st.session_state.entregador_selecionado))
st.session_state.entregador_selecionado = entregador
st.markdown(f"🚚 Entregador selecionado: **{entregador}**")

st.sidebar.subheader("📊 Status dos Pedidos")
st.sidebar.write(f"✅ Prontos: {sum(p['status'] == 'pronto' for p in pedidos)}")
st.sidebar.write(f"📤 Despachados: {sum(p['status'] == 'despachado' for p in pedidos)}")

aba1, aba2, aba3 = st.tabs(["🔴 Em Preparo", "🟢 Prontos", "📤 Despachados"])
abas = {"em_preparo": aba1, "pronto": aba2, "despachado": aba3}

for status, aba in abas.items():
    with aba:
        for pedido in pedidos:
            if pedido["status"] != status:
                continue
            tempo = tempo_espera(pedido)
            prazo_seg = pedido.get("prazo_entrega_min", 30) * 60
            restante = max(0, prazo_seg - tempo)
            progresso = max(0, min(100, 100 - (tempo / prazo_seg * 100)))
            cor = "#28a745" if progresso > 60 else ("#ffc107" if progresso > 30 else "#dc3545")
            cor_fundo = "#e6f4ea" if progresso > 60 else ("#fff8e1" if progresso > 30 else "#fdecea")

            with st.container():
                st.markdown(f"""
                <div style='background-color:{cor_fundo}; border-radius: 16px; padding:16px; margin-bottom: 12px; border: 1px solid #ddd;'>
                    <strong>Pedido #{pedido['id']} - {pedido['bairro']}</strong><br>
                    <span>⏱️ <strong>{restante // 60} min restantes</strong></span><br>
                    📞 <code>{pedido['telefone']}</code><br>
                    🧾 Código Ifood: <code>{pedido['codigo_ifood']}</code><br>
                    <a href="https://confirmacao-entrega-propria.ifood.com.br/numero-pedido" target="_blank">🔗 Confirmar no Ifood</a>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns([1, 1])
                if status == "em_preparo":
                    with col1:
                        if st.button("✅ Marcar Pronto", key=f"pronto_{pedido['id']}"):
                            pedido["status"] = "pronto"
                            save_json(DATA_FILE, pedidos)
                            st.rerun()
                elif status == "pronto":
                    with col2:
                        if st.button("📤 Despachar", key=f"despachar_{pedido['id']}"):
                            pedido["status"] = "despachado"
                            pedido["entregador"] = st.session_state.entregador_selecionado
                            save_json(DATA_FILE, pedidos)
                            st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)

# 🔔 Alerta sonoro se tiver pedido urgente
urgente = any(
    p["status"] != "despachado" and 
    (100 - (tempo_espera(p) / (p.get("prazo_entrega_min", 30) * 60)) * 100) < 30 
    for p in pedidos
)
if urgente:
    st.markdown("""
        <audio autoplay>
          <source src="https://www.soundjay.com/buttons/sounds/beep-07.mp3" type="audio/mpeg">
        </audio>
    """, unsafe_allow_html=True)

save_json(DATA_FILE, pedidos)
