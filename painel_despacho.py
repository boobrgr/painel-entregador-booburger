<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>Painel de Pedidos - Boo Burger</title>
  <style>
    body {
      margin: 0;
      font-family: 'Segoe UI', sans-serif;
      background-color: #f3f3f3;
    }

    header {
      background-color: #222;
      color: white;
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 15px;
      font-size: 24px;
    }

    header img {
      height: 50px;
    }

    .entregadores {
      background: #eee;
      padding: 15px;
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }

    .entregador-btn {
      background-color: #4CAF50;
      border: none;
      padding: 10px 20px;
      color: white;
      font-weight: bold;
      border-radius: 20px;
      cursor: pointer;
      min-width: 100px;
      transition: transform 0.2s;
    }

    .entregador-btn:hover {
      transform: scale(1.05);
    }

    .fila-indice {
      display: block;
      font-size: 10px;
      margin-top: 2px;
    }

    .painel {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 20px;
      padding: 20px;
    }

    .pedido {
      border-radius: 14px;
      padding: 16px;
      background: white;
      box-shadow: 0 4px 8px rgba(0,0,0,0.08);
      display: flex;
      flex-direction: column;
      position: relative;
    }

    .topo {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .cronometro-container {
      position: relative;
      width: 80px;
      height: 80px;
      flex-shrink: 0;
    }

    .cronometro-svg {
      width: 100%;
      height: 100%;
      overflow: visible;
      transform: rotate(-90deg);
    }

    .cronometro-circle-bg {
      fill: white;
      stroke: #ccc;
      stroke-width: 8;
    }

    .cronometro-circle {
      fill: white;
      stroke-width: 8;
      stroke-linecap: round;
      transform-origin: center;
      transition: stroke 0.3s, stroke-dashoffset 0.3s linear;
    }

    .cronometro-text {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      font-weight: bold;
      font-size: 16px;
      text-align: center;
      pointer-events: none;
    }

    .cronometro-text-inner {
      display: inline-block;
      color: white;
    }

    .piscar {
      animation: piscar 1s infinite;
      transform-origin: center;
    }

    @keyframes piscar {
      0% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.6; transform: scale(1.2); }
      100% { opacity: 1; transform: scale(1); }
    }

    .descricao-itens div {
      margin-bottom: 4px;
    }

    .badge {
      padding: 5px 10px;
      font-size: 12px;
      font-weight: bold;
      border-radius: 10px;
      display: inline-block;
      margin-right: 8px;
    }

    .badge.pronto { background-color: #4CAF50; color: white; }
    .badge.entrega { background-color: #f1c40f; color: #000; }

    .info-extra {
      margin-top: 8px;
      font-size: 13px;
      color: #555;
    }
  .entregador-btn.selecionado {
  background-color: #4CAF50;
  color: white;
}
.btn-status {
  padding: 6px 12px;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  margin-right: 8px;
  cursor: pointer;
  opacity: 0.4;
  transition: 0.2s;
}

.btn-status.pronto.ativo {
  background-color: #4CAF50;
  color: white;
  opacity: 1;
}

.btn-status.entrega.ativo {
  background-color: #f1c40f;
  color: #000;
  opacity: 1;
}
</style>
</head>
<body>

<header>
  <img src="https://i.imgur.com/qHXy5vO.png" alt="Logo Boo Burger">
  Painel de Pedidos - Boo Burger
</header>

<div class="entregadores" id="entregadores">
  <!-- Entregadores dinâmicos aqui -->
</div>

<div class="painel" id="painel-pedidos"></div>

<script>
  const entregadores = [
    { nome: "Edimilson" },
    { nome: "Lucas" },
    { nome: "Jhonatan" },
    { nome: "Montanha" },
    { nome: "Nino" }
  ];
let filaSelecionados = [];
  const pedidos = [
    { cliente: "João B.", bairro: "Itapuã", numero: "2050", numero_ifood: "#9899", descricao: ["🍔 2x Dubbo", "🥤 1x Coca-Cola-Litro"], status: "Saiu para Entrega", inicio: "19:05", previsao: "20:05", tempo: 25 },
    { cliente: "Victor L.", bairro: "Centro", numero: "2051", numero_ifood: "#6533", descricao: ["🍔 5x Byron", "*sem cebola", "🍟 3x Batata", "🥤 3x Coca-Cola-Litro"], status: "Saiu para Entrega", inicio: "19:06", previsao: "19:36", tempo: 15 },
    { cliente: "Davi Medeiros", bairro: "Centro", numero: "2053", numero_ifood: "#9638", descricao: ["🍔 2x Dubbo", "🥤 1x Coca-Cola-Litro"], status: "Saiu para Entrega", inicio: "19:12", previsao: "19:42", tempo: 12 },
    { cliente: "João Dantas", bairro: "Abrantes", numero: "2050", numero_ifood: "#9899", descricao: ["🍔 2x Dubbo", "🥤 1x Coca-Cola-Litro"], status: "Saiu para Entrega", inicio: "19:05", previsao: "19:35", tempo: 35 },
    { cliente: "Fernando Liborio", bairro: "Centro", numero: "2051", numero_ifood: "#6533", descricao: ["🍔 2x Dubbo", "🥤 1x Coca-Cola-Litro"], status: "Saiu para Entrega", inicio: "19:05", previsao: "19:35", tempo: 25 }
  ];

  const coresPorBairro = {
    "Centro": "#9be6ff",
    "Itapuã": "#e0e0e0",
    "Abrantes": "#fff1a8"
  };

  function renderEntregadores() {
  const area = document.getElementById("entregadores");
  area.innerHTML = "";
  entregadores.forEach((e) => {
    const btn = document.createElement("button");
    btn.className = "entregador-btn";

    const indexNaFila = filaSelecionados.indexOf(e.nome);
    if (indexNaFila !== -1) {
      btn.classList.add("selecionado");
      btn.innerHTML = `${e.nome}<span class="fila-indice">${indexNaFila + 1}º</span>`;
    } else {
      btn.innerHTML = `${e.nome}`;
    }

    btn.onclick = () => {
      const i = filaSelecionados.indexOf(e.nome);
      if (i === -1) {
        filaSelecionados.push(e.nome);
      } else {
        filaSelecionados.splice(i, 1);
      }
      renderEntregadores();
    };

    area.appendChild(btn);
  });
}


  function createCircularTimer(container, tempoMinutos) {
    const circle = container.querySelector(".cronometro-circle");
    const text = container.querySelector(".cronometro-text-inner");
    const radius = 26;
    const circumference = 2 * Math.PI * radius;
    let seconds = tempoMinutos * 60;

    circle.style.strokeDasharray = circumference;

    const interval = setInterval(() => {
      const percent = seconds / (tempoMinutos * 60);
      const offset = circumference * (1 - percent);
      const min = Math.floor(seconds / 60);
      circle.style.strokeDashoffset = offset;
      text.innerText = `${min}min`;

     const bgCircle = container.querySelector(".cronometro-circle-bg");

if (seconds <= 900) {
  circle.classList.add("piscar");
  text.classList.add("piscar");
  bgCircle.classList.add("piscar");
  circle.style.stroke = "#ff0033";
  text.style.color = "#ff0033";
} else {
  circle.classList.remove("piscar");
  text.classList.remove("piscar");
  bgCircle.classList.remove("piscar");
  circle.style.stroke = "#2ecc71";
  text.style.color = "#2ecc71";
}

      seconds--;
      if (seconds < 0) clearInterval(interval);
    }, 1000);
  }

  function renderPedidos() {
    const painel = document.getElementById("painel-pedidos");
    painel.innerHTML = "";
    pedidos.forEach(p => {
      const card = document.createElement("div");
      card.className = "pedido";
      card.style.backgroundColor = coresPorBairro[p.bairro] || "#fff";

      const topo = document.createElement("div");
      topo.className = "topo";

      const info = document.createElement("div");
      info.innerHTML = `
        <div><strong>Pedido:</strong> ${p.numero} &nbsp; <strong>Ifood:</strong> ${p.numero_ifood}</div>
        <div><strong>Cliente:</strong> ${p.cliente}</div>
        <div><strong>Bairro:</strong> ${p.bairro}</div>
      `;

      const cronometro = document.createElement("div");
      cronometro.className = "cronometro-container";
      cronometro.innerHTML = `
        <svg class="cronometro-svg" viewBox="0 0 60 60">
          <circle class="cronometro-circle-bg" cx="30" cy="30" r="26"/>
          <circle class="cronometro-circle" cx="30" cy="30" r="26"/>
        </svg>
        <div class="cronometro-text"><span class="cronometro-text-inner">0m</span></div>
      `;

      topo.appendChild(info);
      topo.appendChild(cronometro);
      card.appendChild(topo);

      const itens = document.createElement("div");
      itens.className = "descricao-itens";
      itens.innerHTML = p.descricao.map(i => `<div>${i}</div>`).join("");
      card.appendChild(itens);

const statusArea = document.createElement("div");
statusArea.style.marginTop = "10px";

const btnPronto = document.createElement("button");
btnPronto.className = "btn-status pronto";
btnPronto.innerText = "Pronto";
btnPronto.onclick = () => {
  p.status = "Pronto";
  renderPedidos();
};

const btnEntrega = document.createElement("button");
btnEntrega.className = "btn-status entrega";
btnEntrega.innerText = "Saiu para Entrega";
btnEntrega.onclick = () => {
  const entregador = filaSelecionados.shift();
  if (entregador) {
    p.status = "Saiu para Entrega";
    p.entregador = entregador;
    renderEntregadores();
    renderPedidos();
  } else {
    alert("Nenhum entregador selecionado!");
  }
};

if (p.status === "Pronto") btnPronto.classList.add("ativo");
if (p.status === "Saiu para Entrega") {
  btnEntrega.classList.add("ativo");
  const entregadorInfo = document.createElement("div");
  entregadorInfo.className = "info-extra";
  entregadorInfo.innerText = `Entregador: ${p.entregador || '---'}`;
  card.appendChild(entregadorInfo);
}

statusArea.appendChild(btnPronto);
statusArea.appendChild(btnEntrega);
card.appendChild(statusArea);


      const horarios = document.createElement("div");
      horarios.className = "info-extra";
      horarios.innerText = `Início: ${p.inicio} | Previsão: ${p.previsao}`;
      card.appendChild(horarios);

      painel.appendChild(card);
      createCircularTimer(cronometro, p.tempo);
    });
  }

  renderEntregadores();
  renderPedidos();
</script>
</body>
</html>
