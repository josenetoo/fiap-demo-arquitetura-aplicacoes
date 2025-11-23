# Arquitetura Monolítica

## 📖 Conceito

Uma aplicação monolítica é construída como uma **única unidade indivisível**. Todo o código (UI, lógica de negócio, acesso a dados) está em um único projeto e é implantado como uma única aplicação.

## 🏗️ Características

### Vantagens ✅
- **Simplicidade inicial**: Fácil de desenvolver e testar no início
- **Deploy simples**: Um único artefato para implantar
- **Performance**: Chamadas internas são mais rápidas (sem latência de rede)
- **Transações**: ACID garantido dentro da aplicação
- **Debugging**: Mais fácil rastrear problemas em um único codebase

### Desvantagens ❌
- **Escalabilidade limitada**: Precisa escalar toda a aplicação, não partes específicas
- **Acoplamento**: Mudanças em uma parte podem afetar toda a aplicação
- **Deploy arriscado**: Uma falha pode derrubar toda a aplicação
- **Tecnologia única**: Difícil usar diferentes tecnologias para diferentes problemas
- **Crescimento**: Código cresce e fica difícil de manter

## 🎯 Quando Usar

- ✅ Projetos pequenos e médios
- ✅ Equipes pequenas
- ✅ MVPs e protótipos
- ✅ Aplicações com requisitos simples
- ✅ Quando simplicidade é prioridade

## 🚫 Quando Evitar

- ❌ Aplicações muito grandes
- ❌ Múltiplas equipes trabalhando simultaneamente
- ❌ Necessidade de escalar partes específicas
- ❌ Diferentes requisitos de tecnologia por módulo

## 💻 Exemplo Prático

Este exemplo implementa um **e-commerce simples** com:
- Gerenciamento de produtos
- Carrinho de compras
- Processamento de pedidos
- Autenticação de usuários
- Tudo em uma única aplicação Flask

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8+
- Pip

### Passo a Passo

1. **Acesse a pasta**
   ```bash
   cd 01-monolitica
   ```

2. **Crie um ambiente virtual (opcional, mas recomendado)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação**
   ```bash
   python app.py
   ```

5. **Acesse**
   - API: http://localhost:5000/api/products
   - Health Check: http://localhost:5000/

### 🧪 Teste Rápido

```bash
# Listar produtos
curl http://localhost:5000/api/products
```
