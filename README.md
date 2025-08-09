# Crypto Tracker Dashboard

[![Python](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🚀 Visão Geral

**Crypto Tracker Dashboard** é uma aplicação moderna para coleta, armazenamento e visualização histórica de dados de criptomoedas em tempo real. Utiliza a API pública da CoinGecko para coletar preços, volumes, market caps e variações percentuais de moedas como Bitcoin, Ethereum, Cardano, Solana e Dogecoin, armazenando os dados de forma eficiente em arquivos Parquet.

Os dados coletados são apresentados em um dashboard interativo, desenvolvido em [Dash](https://dash.plotly.com/), que permite análise gráfica, filtragem por período e comparação das principais métricas.

---

## 🔥 Features

- Coleta automática e periódica dos dados das principais criptomoedas (Bitcoin, Ethereum, Cardano, Solana, Dogecoin).
- Armazenamento incremental e eficiente em arquivos Parquet para análise histórica.
- Dashboard responsivo e interativo com filtros de período e seleção de moedas.
- Visualização dos preços em USD e BRL, volumes e variações percentuais (1h, 24h, 7d, 30d).
- Implantação facilitada com Docker e Docker Compose para ambiente isolado e reproduzível.

---

## 🛠 Tecnologias

- **Python 3.12** — linguagem principal.
- **Requests** — para consumo da API CoinGecko.
- **Pandas** — manipulação e armazenamento de dados.
- **Parquet** — formato eficiente para armazenamento histórico.
- **Dash by Plotly** — framework para construção do dashboard web.
- **Docker & Docker Compose** — containerização e orquestração.

---

## 📦 Estrutura do Projeto

```
crypto_tracker/
│
├── app/
│   ├── main.py          # Script de coleta e armazenamento dos dados
│   ├── dashboard.py     # Dashboard web para visualização dos dados
│   └── requirements.txt # Dependências Python
│
├── data/
│   └── historical/      # Dados históricos (arquivos .parquet)
│
├── Dockerfile           # Imagem base para coletor e dashboard
├── docker-compose.yml   # Configuração dos serviços Docker
└── README.md            # Documentação do projeto
```

---

## ⚙️ Como Rodar

### Pré-requisitos

- Docker instalado ([Guia oficial](https://docs.docker.com/get-docker/))
- Docker Compose instalado ([Guia oficial](https://docs.docker.com/compose/install/))

### Passo a passo

1. Clone este repositório:

```bash
git clone https://github.com/seu-usuario/crypto-tracker.git
cd crypto-tracker
```

2. Build e start dos containers:

```bash
docker-compose up --build
```

3. Acesse o dashboard no navegador:

```
http://localhost:8050
```

---

## 📊 Como funciona

- O serviço **coletor** (`main.py`) roda continuamente, coletando dados da API CoinGecko a cada 60 segundos, salvando e atualizando os arquivos Parquet em `data/historical/`.
- O serviço **dashboard** (`dashboard.py`) lê esses arquivos e exibe gráficos interativos que podem ser filtrados por moeda e período.

---

## 🔧 Desenvolvimento Local

Caso queira rodar localmente sem Docker:

1. Crie um ambiente virtual e instale as dependências:

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate    # Windows

pip install -r app/requirements.txt
```

2. Rode o coletor:

```bash
python app/main.py
```

3. Em outra aba do terminal, rode o dashboard:

```bash
python app/dashboard.py
```

---

## 📈 Ideias para melhorias futuras

- Integração com banco de dados SQL para consultas mais rápidas.
- Adição de alertas via e-mail ou notificações para variações críticas.
- Inclusão de mais criptomoedas e fontes de dados.
- Implementação de autenticação no dashboard.
- Exportação dos dados filtrados em CSV, Excel ou PDF.

---

## 📄 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor, abra uma issue ou envie um pull request.

---