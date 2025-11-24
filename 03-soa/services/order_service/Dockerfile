FROM python:3.11-slim

WORKDIR /app

# Copiar requirements
COPY ../../requirements.txt .
RUN pip install -r requirements.txt

# Copiar código do serviço
COPY . .

# Copiar ESB (necessário para comunicação)
COPY ../../esb /app/esb

EXPOSE 5012

CMD ["python", "app.py"]
