# painel_despacho.py
# (código completo corrigido com identação correta e estrutura limpa)

# Dados de teste para pedidos
import time
pedidos_teste = [
    {
        "id": 3001,
        "bairro": "Vilas do Atlântico",
        "zona": 4,
        "status": "em_preparo",
        "entregador": None,
        "hora_criacao": time.time() - 300,
        "prazo_entrega_min": 30,
        "telefone": "(71) 9 9999-0001",
        
        "itens": "🍔 Byron x1\n🍟 Batata x1",
        "cliente": "Irineu",
        "consumer_id": "2050",
        "codigo_ifood": "9871"
    },
    {
        "id": 3002,
        "bairro": "Vilas do Atlântico",
        "zona": 4,
        "status": "em_preparo",
        "entregador": None,
        "hora_criacao": time.time() - 600,
        "prazo_entrega_min": 30,
        "telefone": "(71) 9 9999-0002",
        
        "itens": """🍔 Boo x1
🍟 Batata x2""",
        "cliente": "Rebeca",
        "consumer_id": "2051",
        "codigo_ifood": "9872"
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
        
        "itens": """🍔 Bacon King x1
🥤 Refri x1""",
        "cliente": "Larissa",
        "consumer_id": "2052",
        "codigo_ifood": "9873"
    }
]

