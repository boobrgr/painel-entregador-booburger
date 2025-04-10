import streamlit as st
import time
from datetime import datetime

st.set_page_config(page_title="Painel de Pedidos - Boo Burger", layout="wide")

st.markdown("""
<style>
    .top-bar {
        color: black;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        padding: 10px;
        margin-bottom: 30px;
    }
    .entregadores {
        display: flex;
        justify-content: center;
        gap: 16px;
        margin-bottom: 30px;
    }
    .entregador {
        text-align: center;
        background-color: #eee;
        border-radius: 12px;
        padding: 10px;
        width: 90px;
        font-weight: bold;
    }
    .entregador.selecionado {
        background-color: #28a745;
        color: white;
    }
    .pedido-card {
        background: white;
        border-radius: 20px;
        padding: 20px;
        margin-bottom: 30px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    .itens {
        margin: 15px 0;
        line-height: 1.6;
    }
    .tempo-circulo {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        border: 6px solid #444;
        background: #fff;
        margin: 10px auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 16px;
    }
    .botoes-status {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-top: 10px;
    }
    .botoes-status button {
        padding: 6px 12px;
        border-radius: 8px;
        border: none;
        font-weight: bold;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='top-bar'>Painel de Pedidos - Boo Burger</div>", unsafe_allow_html=True)

entregadores_default = ["Edimilson", "Lucas", "Mãozinha", "Montanha", "Nino", "Davi"]

if "fila_entregadores" not in st.session_state:
    st.session_state.fila_entregadores = []

st.markdown("<div class='entregadores'>", unsafe_allow_html=True)
for nome in entregadores_default:
    selecionado = nome in st.session_state.fila_entregadores
    posicao = st.session_state.fila_entregadores.index(nome)+1 if selecionado else ""
    classe = "entregador selecionado" if selecionado else "entregador"
    if st.button(nome, key=f"entregador_{nome}"):
        if not selecionado:
            st.session_state.fila_entregadores.append(nome)
    st.markdown(f"<div class='{classe}'>{f'{posicao}º<br>' if posicao else ''}{nome}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Exemplo de pedidos
if "pedidos" not in st.session_state:
    st.session_state.pedidos = [
        {"id": 2050, "cliente": "Luiza Abreu", "bairro": "Centro", "itens": ["2x 🍔 Dubbo", "1x 🥤 Coca-Cola-Litro"], "codigo_ifood": "9873", "hora_criacao": time.time() - 300, "prazo_entrega_min": 35, "status": "em_preparo"},
        {"id": 2051, "cliente": "Irineu", "bairro": "Centro", "itens": ["1x 🍔 Boo", "1x 🥐 Croissant"], "codigo_ifood": "6543", "hora_criacao": time.time() - 240, "prazo_entrega_min": 30, "status": "em_preparo"},
        {"id": 2052, "cliente": "Larissa", "bairro": "Itinga", "itens": ["1x 🍟 Batata", "1x 🥤 Suco de Laranja"], "codigo_ifood": "4312", "hora_criacao": time.time() - 100, "prazo_entrega_min": 25, "status": "em_preparo"}
    ]

colunas = st.columns(3)
for i, pedido in enumerate(st.session_state.pedidos):
    restante = max(0, int(pedido['prazo_entrega_min'] - (time.time() - pedido['hora_criacao']) // 60))
    with colunas[i % 3]:
        st.markdown("<div class='pedido-card'>", unsafe_allow_html=True)
        st.markdown(f"**Cliente:** {pedido['cliente']}  ", unsafe_allow_html=True)
        st.markdown(f"**Bairro:** {pedido['bairro']}  ", unsafe_allow_html=True)
        st.markdown(f"**Pedido iFood:** #{pedido['codigo_ifood']}  ", unsafe_allow_html=True)
        st.markdown("<div class='itens'>", unsafe_allow_html=True)
        for item in pedido['itens']:
            st.markdown(f"- {item}", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='tempo-circulo'><div>{restante}</div><div style='font-size:10px;'>min</div></div>", unsafe_allow_html=True)

        st.markdown("<div class='botoes-status'>", unsafe_allow_html=True)
        if st.button(f"✅ Pronto {pedido['id']}"):
            pedido['status'] = 'pronto'
        if st.button(f"🚚 Saiu {pedido['id']}"):
            pedido['status'] = 'despachado'
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(f"<div style='text-align:center;font-size:12px;margin-top:8px;'>Início: {datetime.fromtimestamp(pedido['hora_criacao']).strftime('%H:%M')}<br>Previsão: {datetime.fromtimestamp(pedido['hora_criacao'] + pedido['prazo_entrega_min'] * 60).strftime('%H:%M')}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
