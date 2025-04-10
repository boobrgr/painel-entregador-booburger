
import streamlit as st

st.set_page_config(page_title="Painel Boo Burger", layout="wide")

st.markdown("""
    <style>
        .entregadores {
            display: flex;
            overflow-x: auto;
            padding: 10px 0;
        }
        .entregador {
            min-width: 100px;
            height: 40px;
            margin-right: 10px;
            background-color: #444;
            color: white;
            border: none;
            border-radius: 5px;
            text-align: center;
            line-height: 40px;
            flex-shrink: 0;
        }
        .pedido {
            background-color: #fff;
            border-left: 10px solid #3498db;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center;'>Painel de Despacho - Boo Burger</h2>", unsafe_allow_html=True)

# Entregadores
st.markdown("""
<div class="entregadores">
    <div class="entregador">Lucas</div>
    <div class="entregador">Marcos</div>
    <div class="entregador">Jaqueline</div>
    <div class="entregador">Felipe</div>
    <div class="entregador">iFood</div>
</div>
""", unsafe_allow_html=True)

# Pedidos
pedidos = [
    {"nome": "JoÃ£o", "desc": "X-Burger + Fritas", "status": "Em preparo", "tempo": "12min", "cor": "#f39c12"},
    {"nome": "Maria", "desc": "Veggie + Suco", "status": "Aguardando Entregador", "tempo": "18min", "cor": "#e74c3c"},
    {"nome": "Pedro", "desc": "Duplo Boo + Refri", "status": "Saiu para entrega", "tempo": "5min", "cor": "#2ecc71"},
]

for pedido in pedidos:
    st.markdown(f"""
    <div class="pedido" style="border-left-color: {pedido['cor']}">
        <h4>{pedido['nome']}</h4>
        <p>Pedido: {pedido['desc']}</p>
        <p>Status: {pedido['status']}</p>
        <p>Tempo: {pedido['tempo']}</p>
    </div>
    """, unsafe_allow_html=True)
