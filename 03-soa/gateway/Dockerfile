FROM python:3.11-slim

WORKDIR /app

# Copiar requirements
COPY ../requirements.txt .
RUN pip install -r requirements.txt

# Copiar código do gateway
COPY . .

# Copiar ESB (necessário para comunicação)
COPY ../esb /app/esb

EXPOSE 8000

CMD ["python", "api_gateway.py"]
