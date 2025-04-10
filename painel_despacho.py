<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Painel de Despacho - Boo Burger</title>
  <style>
    body {
      margin: 0;
      font-family: Arial, sans-serif;
      background-color: #f3f3f3;
    }

    header {
      padding: 10px;
      background-color: #000;
      color: white;
      text-align: center;
      font-size: 20px;
    }

    .entregadores {
      display: flex;
      overflow-x: auto;
      background-color: #222;
      padding: 10px;
    }

    .entregador {
      min-width: 100px;
      height: 40px;
      margin-right: 10px;
      background-color: #444;
      color: white;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      flex-shrink: 0;
    }

    .entregador.ativo {
      background-color: #27ae60;
    }

    .painel-pedidos {
      display: flex;
      flex-direction: column;
      gap: 15px;
      padding: 15px;
    }

    .pedido {
      background-color: #fff;
      border-left: 10px solid #3498db;
      border-radius: 5px;
      padding: 10px;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .pedido h3 {
      margin: 0 0 5px;
    }

    .pedido p {
      margin: 2px 0;
    }

    @media (max-width: 600px) {
      .pedido {
        font-size: 14px;
      }
    }
  </style>
</head>
<body>

  <header>Painel de Despacho - Boo Burger</header>

  <div class="entregadores">
    <button class="entregador ativo">Lucas</button>
    <button class="entregador">Marcos</button>
    <button class="entregador">Jaqueline</button>
    <button class="entregador">Felipe</button>
    <button class="entregador">iFood</button>
  </div>

  <div class="painel-pedidos">
    <div class="pedido" style="border-left-color: #f39c12;">
      <h3>#1023 - João</h3>
      <p>Pedido: X-Burger + Fritas</p>
      <p>Status: Em preparo</p>
      <p>Tempo: 12min</p>
    </div>

    <div class="pedido" style="border-left-color: #e74c3c;">
      <h3>#1024 - Maria</h3>
      <p>Pedido: Veggie + Suco</p>
      <p>Status: Aguardando Entregador</p>
      <p>Tempo: 18min</p>
    </div>

    <div class="pedido" style="border-left-color: #2ecc71;">
      <h3>#1025 - Pedro</h3>
      <p>Pedido: Duplo Boo + Refrigerante</p>
      <p>Status: Saiu para entrega</p>
      <p>Tempo: 5min</p>
    </div>
  </div>

</body>
</html>
