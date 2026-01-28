# API de Consulta de CEP com Cache e Banco de Dados

Uma API backend em **FastAPI** que consulta dados de CEP usando a **ViaCEP**, com sistema inteligente de **cache em Redis** e persistência em **MongoDB** para performance, escalabilidade e economia de requisições externas.

Projeto ideal para quem quer aprender sobre:

* Arquitetura de cache
* Integração com APIs externas
* Banco NoSQL (MongoDB)
* Containers com Docker
* Boas práticas em backend

---

## Como funciona (Fluxo de Consulta)

Quando você faz uma requisição para um CEP, a API segue esse caminho:

```
Cliente → Redis (cache) → MongoDB → ViaCEP (API externa)
```

### Ordem de prioridade:

1. **Redis (Cache)** → Resposta instantânea ⚡
2. **MongoDB** → Se não estiver no cache
3. **ViaCEP API** → Se não estiver salvo em lugar nenhum

Depois que consulta na ViaCEP:

* Salva no **MongoDB**
* Salva no **Redis (TTL de 24h)**

Resultado: próximas requisições ficam  rápidas 

---

## Stack
### Backend & Linguagem
<p>
  <img src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/python.png" alt="Python" height="40" style="margin-right: 10px;"/>
  <img src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/fastapi.png" alt="FastAPI" height="40"/>
</p>

### Banco de Dados e Cache
<p>
  <img src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/mongodb.png" alt="MongoDB" height="40" style="margin-right: 10px;"/>
  <img src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/redis.png" alt="Redis" height="40"/>
</p>

### Containers & Infra
<p>
  <img src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/docker.png" alt="Docker" height="40" style="margin-right: 10px;"/>
</p>

### HTTP & API
<p>
  <img src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/rest.png" alt="REST" height="40" style="margin-right: 10px;"/>

  <img src="https://raw.githubusercontent.com/marwin1991/profile-technology-icons/refs/heads/main/icons/http.png" alt="HTTP" height="40"/>
</p>

* **Python 3.10+**
* **FastAPI**
* **Redis** (cache)
* **MongoDB** (persistência)
* **Docker & Docker Compose**
* **ViaCEP API**

---

## Estrutura do Projeto

```
API-de-Consulta-de-CEP/
│
├── app/
│   └── main.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Variáveis de Ambiente

Crie um arquivo `.env` baseado no `.env.example`:

```
MONGO_HOST=mongo
MONGO_PORT=27017
REDIS_HOST=redis
REDIS_PORT=6379
```

---

## Rodando com Docker (Recomendado)

### 1️⃣ Suba os containers

```bash
docker-compose up --build
```

### 2️⃣ Acesse a API

* API:
  👉 [http://localhost:8000](http://localhost:8000)

* Documentação automática (Swagger):
  👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Testando a API

### Endpoint

```
GET /cep/{cep}
```

### Exemplo

```bash
curl http://localhost:8000/cep/01001000
```

### Resposta

```json
{
  "source": "cache",
  "data": {
    "cep": "01001-000",
    "logradouro": "Praça da Sé",
    "bairro": "Sé",
    "localidade": "São Paulo",
    "uf": "SP"
  }
}
```

### Campo `source`

| Valor     | Significado                |
| --------- | -------------------------- |
| `cache`   | Veio do Redis ⚡            |
| `mongodb` | Veio do banco de dados 🗄️ |
| `api`     | Veio da ViaCEP 🌐          |

---

## Cache

* TTL configurado para: **24 horas (86400 segundos)**
* Após esse tempo, o Redis apaga o registro automaticamente
* Na próxima requisição, a API busca no MongoDB ou ViaCEP

---

##  Dependências

Arquivo `requirements.txt`:

```
fastapi
uvicorn
requests
redis
pymongo
```

---

##  Conceitos Aplicados

* Cache First Strategy
* Integração com API externa
* Banco NoSQL
* Arquitetura em containers
* Performance backend
* Separação de responsabilidades

---

##  Próximas Features (Ideias)

* 🔐 Autenticação com API Key
* 📊 Dashboard de métricas (quantas consultas por CEP)
* ⏱️ Rate limit por IP
* 🌍 Suporte a múltiplos serviços de CEP
* 📦 Deploy na AWS / Railway / Render

---

## Autor

**Caio Egidio**
Estudante de Ciência da Computação 

Se esse projeto te ajudou, deixa uma ⭐ no repositório — isso dá buff de motivação nível lendário 😄🔥

---

## Licença

Este projeto está sob a licença MIT.
Sinta-se livre para usar, estudar, modificar e evoluir.

---

