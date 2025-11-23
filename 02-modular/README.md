# Arquitetura Modular

## 📖 Conceito

Uma arquitetura modular é um **monolito bem organizado** em módulos independentes e coesos. Ainda é uma única aplicação, mas com separação clara de responsabilidades através de módulos.

## 🏗️ Características

### Vantagens ✅
- **Organização**: Código bem estruturado e fácil de navegar
- **Separação de responsabilidades**: Cada módulo tem sua função clara
- **Manutenibilidade**: Mais fácil de manter que monolito desorganizado
- **Reutilização**: Módulos podem ser reutilizados
- **Deploy simples**: Ainda é um único artefato
- **Transições**: Base para migração futura para microsserviços

### Desvantagens ❌
- **Ainda é monolito**: Limitações de escalabilidade permanecem
- **Disciplina necessária**: Requer disciplina para manter separação
- **Acoplamento possível**: Módulos podem se acoplar se não houver cuidado
- **Deploy único**: Ainda precisa subir tudo junto

## 🎯 Quando Usar

- ✅ Monolitos que estão crescendo
- ✅ Equipes que querem melhor organização
- ✅ Preparação para microsserviços no futuro
- ✅ Projetos médios que precisam de estrutura
- ✅ Quando quer benefícios de organização sem complexidade de distribuição

## 🚫 Quando Evitar

- ❌ Projetos muito pequenos (over-engineering)
- ❌ Quando já precisa de escalabilidade independente
- ❌ Múltiplas equipes autônomas

## 💻 Exemplo Prático

Este exemplo implementa o **mesmo e-commerce**, mas organizado em módulos:

```
02-modular/
├── app.py                 # Aplicação principal
├── config.py              # Configurações
├── modules/
│   ├── auth/             # Módulo de autenticação
│   │   ├── models.py
│   │   ├── services.py
│   │   └── routes.py
│   ├── products/         # Módulo de produtos
│   │   ├── models.py
│   │   ├── services.py
│   │   └── routes.py
│   ├── orders/           # Módulo de pedidos
│   │   ├── models.py
│   │   ├── services.py
│   │   └── routes.py
│   └── payment/          # Módulo de pagamento
│       ├── services.py
│       └── routes.py
└── shared/               # Código compartilhado
    └── database.py
```

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8+
- Pip

### Passo a Passo

1. **Acesse a pasta**
   ```bash
   cd 02-modular
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
   - API: http://localhost:5001/api/products
   - Health Check: http://localhost:5001/health

### 🧪 Teste Rápido

```bash
# Listar produtos
curl http://localhost:5001/api/products
```