# Sistema de Triangulação de Motos - IoT Prototype (Sprint 3)

## 📋 Descrição do Projeto

Protótipo funcional de um sistema de gerenciamento inteligente de motos, utilizando simuladores Python para sensores RFID e atuadores, com integração em tempo real via HTTP. O sistema permite monitoramento de motos em diferentes pontos de um pátio, persistência de dados e visualização em dashboard local.

## 🎯 Problema Resolvido

**Desafio**: Localização precisa e monitoramento em tempo real de motos em pátios da Mottu.
**Solução**: Sistema de triangulação usando múltiplos sensores RFID simulados que coletam dados de intensidade de sinal e enviam para uma API Python, permitindo rastreamento de até 3 dispositivos IoT simultaneamente.

## 🛠 Tecnologias Utilizadas

### Simulação de Hardware:

*   Sensores RFID (simulados via Python)
*   Atuadores simulados (LEDs virtuais ou mensagens de status)
*   3 dispositivos IoT simulados

### Software e Protocolos:

*   Python 3.13
*   Flask / Flask-SocketIO (API e comunicação em tempo real)
*   SQLite (persistência de dados)
*   HTTP/REST API
*   JSON (formato de dados)
*   Dashboard em Flask + HTML/JS

### Links:

*   Pitch = https://www.youtube.com/watch?si=OhGFE0eqJH3WFoXn&v=tFLwiapUUiE&feature=youtu.be
*   Demostração = 

## 🔧 Como Rodar o Projeto

### Clonar o repositório e criar ambiente virtual:

```bash
git clone <URL_DO_REPO>
cd IOT
python -m venv venv
vvenv\\Scripts\\activate   # Windows
pip install -r requirements.txt
```

### Rodar a API:

```bash
python api.py
```

A API ficará escutando em `http://localhost:5007/api`.

### Rodar os dispositivos simulados (3 sensores/atuadores):

```bash
cd devices
python leitura.py --api-base http://localhost:5007/api --devices 3 --interval 3
```

Cada dispositivo envia leituras de RFID periodicamente para a API.

### Rodar o dashboard para visualização:

```bash
cd ../dashboard
python dashboard_server.py
```

Dashboard acessível em `http://localhost:5008`.
Mostra leituras recentes e status dos dispositivos em tempo real.

## 📊 Dados Enviados para API

Formato JSON:

```json
{
  "rfid": "ECAAAAAAAAAAAAAAAAAAAAAAMOTTU20293",
  "device_id": 1,
  "potencia_sinal": 13
}
```

## 🔄 Funcionamento do Sistema

### Fluxo de operação:

*   Sensores simulados detectam motos (IDs RFID) e geram potência do sinal aleatória.
*   Dados são enviados via HTTP POST para a API.
*   API armazena os dados no banco SQLite.
*   Dashboard consome API via REST + WebSocket e exibe telemetria em tempo real.

### Testes Funcionais Simulados:

*   Motos desaparecendo ou trocando de posição.
*   Comunicação de até 3 dispositivos IoT simultaneamente.

## 🏗 Arquitetura do Sistema

`[Dispositivos IoT Simulados] → [API Flask] → [SQLite] → [Dashboard Flask/JS]`

## 📡 Protocolos de Comunicação

### Requisição HTTP

`POST /api/rfid`
`Content-Type: application/json`

```json
{
  "rfid": "string",
  "device_id": number,
  "potencia_sinal": number
}
```

### WebSocket

Dashboard recebe atualizações em tempo real via Flask-SocketIO.

## 📊 Dashboard

### Funcionalidades:

*   Leituras recentes e status dos dispositivos
*   Histórico persistido em SQLite
*   Atualização em tempo real via WebSocket
*   Visualização de dados em gráficos simples

## 🔮 Aplicações Futuras

*   Integração com hardware real (ESP32 + RFID)
*   Algoritmos de triangulação mais precisos
*   Notificações e alertas automáticos
*   Protocolo MQTT para menor latência
*   Expansão para mais sensores e atuadores

## 📋 Resultados Parciais

### ✅ Concluído:

*   Simuladores Python funcionais para 3 dispositivos
*   Comunicação HTTP/REST API
*   Persistência de dados com SQLite
*   Dashboard em tempo real com Flask-SocketIO
*   Estrutura modular e extensível

### 🔄 Em Desenvolvimento:

*   Algoritmo de triangulação refinado
*   Testes com hardware real
*   Alertas e notificações em tempo real

## 🚀 Próximos Passos

*   Testes de campo com hardware físico
*   API de consulta de histórico avançada
*   Dashboard com mais métricas e filtros
*   Integração com algoritmos de ML para análise de padrões

## Informações Adicionais

*   **Desenvolvido para**: DISRUPTIVE ARCHITECTURES: IOT, IOB & GENERATIVE IA
*   **Tecnologias**: Python, Flask, Flask-SocketIO, SQLite, HTTP, JSON
*   **Objetivo**: Protótipo funcional de sistema de triangulação de motos com múltiplos dispositivos IoT simulados

