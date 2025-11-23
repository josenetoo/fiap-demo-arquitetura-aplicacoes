# Arquitetura de Microsserviços

## 📖 Conceito

Microsserviços é uma arquitetura onde a aplicação é composta por **serviços pequenos, independentes e autônomos** que se comunicam através de APIs leves (geralmente HTTP/REST ou mensageria).

## 🏗️ Características

### Princípios Fundamentais
- **Serviços independentes**: Cada serviço é autônomo
- **Banco de dados por serviço**: Cada serviço tem seu próprio BD
- **Comunicação leve**: REST, gRPC, mensageria
- **Deploy independente**: Serviços sobem separadamente
- **Organização por domínio**: Bounded contexts (DDD)

### Vantagens ✅
- **Escalabilidade independente**: Escala apenas o que precisa
- **Tecnologias heterogêneas**: Cada serviço pode usar tech diferente
- **Deploy independente**: Agilidade e menos risco
- **Resiliência**: Falha isolada não derruba tudo
- **Times autônomos**: Equipes podem trabalhar independentemente
- **Facilita CI/CD**: Deploy contínuo de serviços individuais

### Desvantagens ❌
- **Complexidade operacional**: Mais serviços para gerenciar
- **Latência de rede**: Comunicação entre serviços via rede
- **Transações distribuídas**: Difícil manter consistência
- **Debugging complexo**: Rastrear problemas entre serviços
- **Overhead de infraestrutura**: Requer orquestração (K8s, etc)
- **Duplicação de código**: Pode haver duplicação entre serviços

## 🆚 Comparação com Outras Arquiteturas

| Aspecto | Monolito | Modular | SOA | Microsserviços |
|---------|----------|---------|-----|----------------|
| **Granularidade** | Uma aplicação | Módulos | Serviços médios | Serviços pequenos |
| **Deploy** | Único | Único | Coordenado | Independente |
| **Banco de dados** | Único | Único | Compartilhado | Por serviço |
| **Comunicação** | Interna | Interna | ESB | Ponto a ponto |
| **Escalabilidade** | Vertical | Vertical | Horizontal limitada | Horizontal granular |
| **Tecnologia** | Única | Única | Múltiplas | Múltiplas |
| **Complexidade** | Baixa | Média | Alta | Muito alta |

## 🎯 Quando Usar

- ✅ Aplicações grandes e complexas
- ✅ Múltiplas equipes trabalhando simultaneamente
- ✅ Necessidade de escalar partes específicas
- ✅ Deploy frequente e independente
- ✅ Diferentes requisitos tecnológicos por domínio
- ✅ Alta disponibilidade e resiliência

## 🚫 Quando Evitar

- ❌ Projetos pequenos (over-engineering)
- ❌ Equipes pequenas sem experiência
- ❌ Infraestrutura limitada
- ❌ Requisitos simples
- ❌ Quando monolito atende bem

## 💻 Exemplo Prático

Este exemplo implementa microsserviços com:
- **4 serviços independentes**: Auth, Products, Orders, Payment
- **Banco de dados por serviço**: Cada um tem seu BD
- **API Gateway**: Ponto de entrada único
- **Service Discovery**: Registro de serviços
- **Comunicação REST**: APIs HTTP entre serviços
- **Docker**: Containerização de cada serviço

```
04-microsservicos/
├── api-gateway/          # Gateway de entrada
├── auth-service/         # Serviço de autenticação
│   ├── app.py
│   ├── database.db      # BD próprio
│   └── Dockerfile
├── product-service/      # Serviço de produtos
│   ├── app.py
│   ├── database.db      # BD próprio
│   └── Dockerfile
├── order-service/        # Serviço de pedidos
│   ├── app.py
│   ├── database.db      # BD próprio
│   └── Dockerfile
├── payment-service/      # Serviço de pagamento
│   ├── app.py
│   └── Dockerfile
└── docker-compose.yml    # Orquestração local
```

## 🚀 Como Executar

### Opção 1: Docker Compose (Recomendado 🌟)

Esta é a forma mais fácil e próxima de um ambiente real.

1. **Acesse a pasta**
   ```bash
   cd 04-microsservicos
   ```

2. **Suba os serviços**
   ```bash
   docker-compose up --build
   ```

3. **Acesse**
   - Gateway: http://localhost:9000/health
   - Auth: http://localhost:6001/health
   - Products: http://localhost:6002/health

### Opção 2: Execução Manual (Desenvolvimento)

Se não quiser usar Docker, você precisará de **5 terminais**.

1. **Preparação (em qualquer terminal)**
   ```bash
   cd 04-microsservicos
   # Instalar dependências comuns
   pip install -r requirements.txt
   ```

2. **Terminal 1 - Auth Service**
   ```bash
   cd auth-service
   pip install -r requirements.txt
   python app.py
   ```

3. **Terminal 2 - Product Service**
   ```bash
   cd product-service
   pip install -r requirements.txt
   python app.py
   ```

4. **Terminal 3 - Order Service**
   ```bash
   cd order-service
   pip install -r requirements.txt
   python app.py
   ```

5. **Terminal 4 - Payment Service**
   ```bash
   cd payment-service
   pip install -r requirements.txt
   python app.py
   ```

6. **Terminal 5 - API Gateway**
   ```bash
   cd api-gateway
   pip install -r requirements.txt
   python app.py
   ```

### 🧪 Teste Rápido

```bash
# Verificar saúde de todos os serviços
curl http://localhost:9000/health

# Listar produtos (via Gateway)
curl http://localhost:9000/api/products
```

## 🔧 Padrões Importantes

- **API Gateway**: Ponto de entrada único
- **Service Discovery**: Registro e descoberta de serviços
- **Circuit Breaker**: Proteção contra falhas em cascata
- **Saga Pattern**: Transações distribuídas
- **CQRS**: Separação de leitura e escrita
- **Event Sourcing**: Histórico de eventos
- **Sidecar Pattern**: Funcionalidades auxiliares
