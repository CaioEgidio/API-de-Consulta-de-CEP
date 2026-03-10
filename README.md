# API de Consulta de CEP (Arquitetura DDD & SOLID)

Uma API backend em **FastAPI** que consulta dados de CEP usando a **ViaCEP**, com sistema inteligente de **cache em Redis** e persistência em **MongoDB** para performance, escalabilidade e economia de requisições externas.

Este projeto foi refatorado para aplicar os princípios do **Domain-Driven Design (DDD)** e **SOLID**, garantindo um código altamente escalável, testável e de fácil manutenção.

---

## 🚀 O que há de novo? (Evolução da Arquitetura)

O projeto evoluiu de uma estrutura simples para uma arquitetura em camadas focada no domínio:

* **Domain Layer (`app/domain`)**: Contém os modelos de dados (como a entidade `Address`) e os contratos/interfaces (`ICacheRepository`, `IDatabaseRepository`, `IExternalApi`), aplicando o princípio de **Inversão de Dependência (D do SOLID)**.
* **Application Layer (`app/application`)**: Orquestra a regra de negócio através do `CepService`, decidindo quando buscar no cache, no banco ou na API externa.
* **Infrastructure Layer (`app/infrastructure`)**: Implementações concretas das interfaces, isolando a lógica de acesso ao MongoDB, Redis e ViaCEP.

Além disso, novas features de segurança foram implementadas:
* 🔐 **Autenticação com API Key**: Rotas agora são protegidas e exigem um header de autorização.
* ⏱️ **Rate Limiting**: Bloqueio de abusos utilizando o Redis (limite de 100 requisições a cada 20 segundos por chave).

---

## ⚙️ Como funciona (Fluxo de Consulta)

Quando você faz uma requisição para um CEP, a API segue esse caminho na camada de serviço:

```text
Cliente → Redis (cache) → MongoDB → ViaCEP (API externa)
```

### Ordem de prioridade:
1. **Redis (Cache)** → Resposta instantânea ⚡
2. **MongoDB** → Se não estiver no cache 🗄️
3. **ViaCEP API** → Se não estiver salvo em lugar nenhum 🌐

Depois que consulta na ViaCEP, a API salva os dados no **MongoDB** e no **Redis com um TTL de 24 horas (86400 segundos)**.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.12**
* **FastAPI** (Framework Web)
* **Redis** (Cache e Rate Limit)
* **MongoDB** (Persistência)
* **Docker & Docker Compose** (Infraestrutura)
* **Pydantic** (Validação de Dados)

---

## 📂 Estrutura do Projeto

```text
API-de-Consulta-de-CEP/
│
├── app/
│   ├── application/     # Casos de uso e serviços (CepService)
│   ├── domain/          # Entidades (Address) e Interfaces abstratas
│   ├── infrastructure/  # Repositórios (Redis, Mongo) e chamadas externas (ViaCEP)
│   └── main.py          # Entrypoint, Injeção de Dependências e Rotas
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 Rodando com Docker (Recomendado)

### 1️⃣ Crie suas variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto (use o `.env.example` como base):
```env
MONGO_HOST=mongo
MONGO_PORT=27017
REDIS_HOST=redis
REDIS_PORT=6379
```

### 2️⃣ Suba os containers
```bash
docker-compose up --build
```
A API estará disponível em 👉 [http://localhost:8000](http://localhost:8000)

A documentação interativa (Swagger) pode ser acessada em 👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Testando a API

### Endpoint
```http
GET /cep/{cep}
```

**Atenção:** A API agora exige o envio de uma chave de acesso válida através do Header `x-api-key`. 
Chaves de teste disponíveis por padrão: `abc123` ou `teste456`.

### Exemplo via cURL
```bash
curl -H "x-api-key: abc123" http://localhost:8000/cep/01001000
```

### Exemplo de Resposta
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

## 👨‍💻 Autor

**Caio Egidio**
Estudante de Ciência da Computação

Se esse projeto te ajudou, deixa uma ⭐ no repositório — isso dá buff de motivação nível lendário 😄🔥

---

## 📄 Licença

Este projeto está sob a licença MIT. Sinta-se livre para usar, estudar, modificar e evoluir.