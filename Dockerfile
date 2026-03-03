FROM python:3.12.3

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Agora copiamos o projeto inteiro, não apenas o que está dentro da pasta app
COPY . .

# Mudamos o comando para rodar a partir da pasta raiz
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]