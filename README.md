# FIAP Pós Tech - Demo de Arquiteturas de Aplicações

Material prático e completo para live sobre **Diferenças e Práticas de Arquitetura de Aplicações**.

## 🎯 Objetivo

Demonstrar na prática as diferenças, vantagens, desvantagens e casos de uso de cada arquitetura através de **exemplos de código reais e funcionais**.

## 📚 Conteúdo

Este repositório contém **4 arquiteturas completas** implementadas:

1. **🏢 Arquitetura Monolítica** - Aplicação única e coesa
2. **🏗️ Arquitetura Modular** - Monolito organizado em módulos
3. **🚌 Arquitetura SOA** - Service-Oriented Architecture com ESB
4. **🔷 Arquitetura de Microsserviços** - Serviços independentes e distribuídos

Todas implementam o **mesmo e-commerce** para comparação justa.

## 🚀 Início Rápido

### 👉 Comece Aqui!

```bash
# 1. Clone o repositório
git clone <repo-url>
cd fiap-demo-arquitetura

# 2. Leia o guia de início
cat START_HERE.md

# 3. Teste uma arquitetura
cd 01-monolitica
pip install -r requirements.txt
python app.py
```

## 🔧 Tecnologias

- **Backend**: Python 3.11, Flask
- **Banco de Dados**: SQLite (demo)
- **Containerização**: Docker, Docker Compose
- **Comunicação**: REST APIs, HTTP

## 📊 Comparação Rápida

| Arquitetura | Complexidade | Escalabilidade | Deploy | Quando Usar |
|-------------|--------------|----------------|--------|-------------|
| Monolítica | ⭐ Baixa | Limitada | Único | MVP, pequenos projetos |
| Modular | ⭐⭐ Média | Limitada | Único | Monolito crescendo |
| SOA | ⭐⭐⭐⭐ Alta | Média | Coordenado | Integração corporativa |
| Microsserviços | ⭐⭐⭐⭐⭐ Muito Alta | Granular | Independente | Apps grandes, múltiplas equipes |

## 💡 Mensagem Principal

> **Não existe arquitetura perfeita. Existe a arquitetura certa para o SEU contexto.**

### Evolução Recomendada
```
MVP → Monolito → Modular → Microsserviços
                            (se necessário)
```

⚠️ **Não pule etapas!** Começar com microsserviços é geralmente um erro.

## 🎬 Demonstrações

### Monolítica (Porta 5000)
```bash
cd 01-monolitica
python app.py
curl http://localhost:5000/api/products
```

### Modular (Porta 5001)
```bash
cd 02-modular
python app.py
curl http://localhost:5001/api/products
```

### Microsserviços (Porta 9000)
```bash
cd 04-microsservicos
docker-compose up
curl http://localhost:9000/health
```

---

**FIAP Pós Tech - DevOps e Arquitetura Cloud**

*Material desenvolvido com ❤️ para educação*
