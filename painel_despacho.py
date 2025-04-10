# Este painel requer a biblioteca Streamlit. Para instalar:
# pip install streamlit

try:
    import streamlit as st
    import time
    from datetime import datetime
except ModuleNotFoundError:
    print("Erro: O módulo 'streamlit' não está instalado. Use 'pip install streamlit'.")
else:

    st.set_page_config(page_title="Painel de Despacho - Boo Burger", layout="wide")

    st.markdown("""
    <style>
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
        .entregador-button {
            padding: 10px 16px;
            margin: 0 5px;
            border: none;
            border-radius: 12px;
            background-color: #eee;
            font-weight: bold;
            cursor: pointer;
        }
        .entregador-selecionado {
            background-color: #28a745 !important;
            color: white !important;
        }
        .card {
            background: white;
            border-radius: 20px;
            padding: 14px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            position: relative;
        }
        .card-esmaecido {
            opacity: 0.4;
        }
        .tempo-circulo {
            width: 65px;
            height: 65px;
            border-radius: 50%;
            border: 6px solid #444;
            background: #fff;
            margin: auto;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 15px;
        }
        .botoes-status button {
            padding: 6px 10px;
            border-radius: 8px;
            border: none;
            font-weight: bold;
            cursor: pointer;
        }
        .botao-pronto {
            background: #28a745;
            color: white;
        }
        .botao-saiu {
            background: #ffc107;
            color: black;
        }
        .remover {
            position: absolute;
            right: 12px;
            top: 10px;
            color: red;
            font-weight: bold;
            cursor: pointer;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='top-bar'>
        Boo Burger - Painel de Despacho
    </div>
    """, unsafe_allow_html=True)

    entregadores_default = ["Edimilson", "Lucas", "Mãozinha", "Montanha", "Nino", "Davi Medeiros"]

    if "fila_entregadores" not in st.session_state:
        st.session_state.fila_entregadores = []

    st.write("## Entregadores")
    cols = st.columns(len(entregadores_default))
    for i, (nome, col) in enumerate(zip(entregadores_default, cols)):
        if nome not in st.session_state.fila_entregadores:
            if col.button(nome):
                st.session_state.fila_entregadores.append(nome)
        else:
            col.markdown(f"<button class='entregador-button entregador-selecionado'>{nome} ({st.session_state.fila_entregadores.index(nome)+1}º)</button>", unsafe_allow_html=True)

    if "pedidos" not in st.session_state:
        st.session_state.pedidos = [
            {"id": 2050, "cliente": "Luiza Abreu", "bairro": "CENTRO", "itens": ["🍔 Byron x1", "🍟 Batata x2"], "codigo_ifood": "9873", "hora_criacao": time.time() - 180, "prazo_entrega_min": 35, "status": "em_preparo"},
            {"id": 2051, "cliente": "Irineu", "bairro": "CENTRO", "itens": ["🍔 Boo x1", "🥐 Croissant x1"], "codigo_ifood": "6543", "hora_criacao": time.time() - 240, "prazo_entrega_min": 35, "status": "em_preparo"},
            {"id": 2052, "cliente": "Rebeca", "bairro": "MUSSURUNGA", "itens": ["🍔 Dubbo x1", "🍟 Batata x1"], "codigo_ifood": "4321", "hora_criacao": time.time() - 300, "prazo_entrega_min": 30, "status": "em_preparo"},
            {"id": 2053, "cliente": "Larissa", "bairro": "ITAPUÃ", "itens": ["🍔 Dubbo x1", "🥤 Suco x1"], "codigo_ifood": "1234", "hora_criacao": time.time() - 150, "prazo_entrega_min": 30, "status": "em_preparo"}
        ]

    pedidos = sorted(st.session_state.pedidos, key=lambda p: (p['status'] != 'em_preparo', p['hora_criacao']))
    cols = st.columns(4)
    for i, pedido in enumerate(pedidos):
        col = cols[i % 4]
        restante = max(0, int(pedido['prazo_entrega_min'] - (time.time() - pedido['hora_criacao']) // 60))
        classe = "card"
        if pedido['status'] != "em_preparo":
            classe += " card-esmaecido"

        with col:
            st.markdown(f"""
            <div class='{classe}'>
                <div class='remover'>❌</div>
                <div><strong>Pedido:</strong> {pedido['id']}</div>
                <div><strong>Ifood:</strong> #{pedido['codigo_ifood']}</div>
                <div><strong>Cliente:</strong> {pedido['cliente']}</div>
                <div><strong>Bairro:</strong> {pedido['bairro']}</div>
                <div style='margin-top:10px;'>
                    {'<br>'.join(pedido['itens'])}
                </div>
                <div class='tempo-circulo' style='border-color: {'#dc3545' if pedido['status']=='em_preparo' else ('#28a745' if pedido['status']=='pronto' else '#ffc107')}'>
                    <div>{restante}</div>
                    <div style='font-size:10px;'>min</div>
                </div>
            """, unsafe_allow_html=True)

            if st.button('✅ Pronto', key=f"pronto_{pedido['id']}"):
                pedido['status'] = 'pronto'
            if st.button('🚚 Saiu', key=f"saiu_{pedido['id']}"):
                pedido['status'] = 'despachado'
            if st.button(f"Remover {pedido['id']}", key=f"rm_{pedido['id']}"):
                st.session_state.pedidos = [p for p in st.session_state.pedidos if p['id'] != pedido['id']]
                st.stop()

            st.markdown(f"""
                <div style='font-size:11px;text-align:center;margin-top:8px;'>
                    Início: {datetime.fromtimestamp(pedido['hora_criacao']).strftime('%H:%M')}<br>
                    Previsão: {datetime.fromtimestamp(pedido['hora_criacao'] + pedido['prazo_entrega_min'] * 60).strftime('%H:%M')}
                </div>
            </div>
            """, unsafe_allow_html=True)
