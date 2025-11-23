# Arquitetura SOA (Service-Oriented Architecture)

## 📖 Conceito

SOA é uma arquitetura onde a aplicação é composta por **serviços independentes** que se comunicam através de um **Enterprise Service Bus (ESB)**. Os serviços são mais granulares que um monolito, mas menos que microsserviços.

## 🏗️ Características

### Componentes Principais
- **ESB (Enterprise Service Bus)**: Barramento central de comunicação
- **Serviços**: Componentes de negócio independentes
- **Contratos**: Interfaces bem definidas (WSDL, SOAP, REST)
- **Orquestração**: Coordenação de serviços pelo ESB

### Vantagens ✅
- **Reutilização**: Serviços podem ser reutilizados por múltiplas aplicações
- **Integração**: Facilita integração entre sistemas heterogêneos
- **Governança**: Controle centralizado no ESB
- **Padrões**: Uso de padrões estabelecidos (SOAP, WSDL)
- **Transformação**: ESB pode transformar mensagens entre formatos

### Desvantagens ❌
- **ESB como gargalo**: Ponto único de falha e bottleneck
- **Complexidade**: ESB adiciona camada de complexidade
- **Acoplamento ao ESB**: Serviços dependem do barramento
- **Performance**: Overhead de comunicação via ESB
- **Pesado**: Geralmente requer infraestrutura robusta

## 🆚 SOA vs Microsserviços

| Aspecto | SOA | Microsserviços |
|---------|-----|----------------|
| Comunicação | ESB centralizado | Ponto a ponto |
| Granularidade | Serviços maiores | Serviços menores |
| Governança | Centralizada | Descentralizada |
| Banco de dados | Compartilhado | Por serviço |
| Deploy | Coordenado | Independente |

## 🎯 Quando Usar

- ✅ Integração de sistemas legados
- ✅ Ambiente corporativo com governança forte
- ✅ Necessidade de transformação de mensagens
- ✅ Reutilização de serviços entre aplicações
- ✅ Padrões empresariais estabelecidos

## 🚫 Quando Evitar

- ❌ Startups e projetos ágeis
- ❌ Necessidade de alta escalabilidade
- ❌ Equipes pequenas
- ❌ Deploy frequente e independente

## 💻 Exemplo Prático

Este exemplo implementa SOA com:
- **ESB Simples**: Barramento de mensagens
- **Serviços**: Auth, Products, Orders, Payment
- **Comunicação**: Via ESB com transformação de mensagens
- **Orquestração**: Coordenação de fluxos complexos

```
03-soa/
├── esb/                  # Enterprise Service Bus
│   ├── message_bus.py   # Barramento de mensagens
│   ├── orchestrator.py  # Orquestrador de serviços
│   └── transformer.py   # Transformador de mensagens
├── services/            # Serviços independentes
│   ├── auth_service/
│   ├── product_service/
│   ├── order_service/
│   └── payment_service/
└── gateway/             # API Gateway
    └── api_gateway.py
```

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8+
- Pip

### Passo a Passo

Esta arquitetura requer a execução de múltiplos processos. Você precisará de **6 terminais**.

1. **Preparação (em qualquer terminal)**
   ```bash
   cd 03-soa
   # Criar venv (recomendado)
   python -m venv venv
   source venv/bin/activate
   # Instalar dependências
   pip install -r requirements.txt
   ```

2. **Terminal 1 - Enterprise Service Bus (ESB)**
   ```bash
   source venv/bin/activate
   python esb/message_bus.py
   ```

3. **Terminal 2 - Auth Service (Porta 5010)**
   ```bash
   source venv/bin/activate
   python services/auth_service/app.py
   ```

4. **Terminal 3 - Product Service (Porta 5011)**
   ```bash
   source venv/bin/activate
   python services/product_service/app.py
   ```

5. **Terminal 4 - Order Service (Porta 5012)**
   ```bash
   source venv/bin/activate
   python services/order_service/app.py
   ```

6. **Terminal 5 - Payment Service (Porta 5013)**
   ```bash
   source venv/bin/activate
   python services/payment_service/app.py
   ```

7. **Terminal 6 - API Gateway (Porta 8000)**
   ```bash
   source venv/bin/activate
   python gateway/api_gateway.py
   ```

### 🧪 Teste Rápido

```bash
# Verificar status do ESB
curl http://localhost:8000/esb/status

# Listar produtos (via Gateway -> ESB -> Product Service)
curl http://localhost:8000/api/products
```

