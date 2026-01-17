# 🚀 API de Consulta de CEP com FastAPI

Uma API simples, rápida e eficiente para consultar informações de endereço a partir de um CEP brasileiro utilizando a API pública do **ViaCEP**. Desenvolvida com **FastAPI**, essa aplicação demonstra boas práticas de criação de endpoints, tratamento de erros e consumo de APIs externas.

> Projeto 100% autoral — desenvolvido por **Caio Marques** para fins de estudo, portfólio e prática profissional.

---

## 📌 Funcionalidades

* 🔍 Consulta de CEP via endpoint REST
* ⚡ Respostas rápidas e estruturadas em JSON
* 🛑 Tratamento de erros para:

  * CEP inválido
  * CEP não encontrado
  * Falha na comunicação com a API externa

---

## 🧠 O que eu aprendi com este projeto

* Como criar e estruturar uma API REST com **FastAPI**
* Consumo de APIs externas usando a biblioteca **requests**
* Tratamento de exceções com `HTTPException`
* Validação de respostas e checagem de erros no JSON retornado
* Organização de código para facilitar manutenção e escalabilidade

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.10+**
* **FastAPI**
* **Uvicorn** (servidor ASGI)
* **Requests**
* **ViaCEP API** (serviço externo de consulta de CEP)

---

## 📂 Estrutura do Projeto

```bash
📁 api-consulta-cep
 ├── main.py
 ├── requirements.txt
 └── README.md
```

---

## ⚙️ Como Executar o Projeto

### 1️⃣ Clone o repositório

```bash
git clone https://github.com/seu-usuario/api-consulta-cep.git
cd api-consulta-cep
```

### 2️⃣ Crie e ative o ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Inicie o servidor

```bash
uvicorn main:app --reload
```

---

## 🌐 Como Usar a API

### Endpoint disponível

```http
GET /cep/{cep}
```

### Exemplo de requisição

```http
http://127.0.0.1:8000/cep/01001000
```

### Exemplo de resposta

```json
{
  "cep": "01001-000",
  "logradouro": "Praça da Sé",
  "bairro": "Sé",
  "localidade": "São Paulo",
  "uf": "SP"
}
```

---

## ❌ Possíveis Erros

| Código | Descrição               |
| ------ | ----------------------- |
| 404    | CEP não encontrado      |
| 404    | Erro ao consultar a API |

---

## 🔮 Melhorias Futuras

* ⚡ **Sistema de Cache com Redis**

  * Armazenar CEPs consultados em cache
  * Retornar do cache quando disponível
  * TTL de 24h para manter dados atualizados

* 🗄️ **Persistência em Banco de Dados (MongoDB ou SQL)**

  * Armazenar todos os CEPs consultados
  * Usar o banco como fonte secundária quando não houver cache

* 🔁 **Fluxo Inteligente de Consulta**

```text
Consulta CEP
  ↓
Verifica Cache (Redis)
  ├─ Existe? → Retorna resultado
  └─ Não existe
        ↓
     Verifica Banco (MongoDB/SQL)
        ├─ Existe? → Salva no cache (TTL 24h) → Retorna
        └─ Não existe
              ↓
        Consulta ViaCEP
              ↓
      Salva no Banco + Cache
              ↓
           Retorna
```

* 🐳 **Ambiente Containerizado com Docker**

  * Instância do Redis
  * Instância do MongoDB
  * API FastAPI rodando em container

* 🧱 **Aplicação de Princípios SOLID**

  * Separação de responsabilidades (Service, Repository, Cache Layer)
  * Código mais limpo, testável e escalável

* 📦 Implementar testes automatizados (Pytest)

* 🔐 Adicionar autenticação por token

* 📊 Criar sistema de logs e métricas

* 📦 Implementar cache para reduzir chamadas à API externa

* ✅ Validação automática de formato de CEP

* 🔐 Adicionar autenticação por token

* 📊 Criar sistema de logs e métricas

* 🐳 Containerizar a aplicação com Docker

---

## 📸 Documentação Interativa

Após iniciar o servidor, acesse:

* Swagger UI:

  ```
  http://127.0.0.1:8000/docs
  ```

* Redoc:

  ```
  http://127.0.0.1:8000/redoc
  ```

---

## 🧑‍💻 Autor

Desenvolvido por **Caio Marques**
🎯 Estudante de Ciência da Computação | Backend | APIs | Machine Learning Enthusiast

---

## ⭐ Considerações Finais

Este projeto faz parte da minha jornada de aprendizado em desenvolvimento backend e construção de APIs modernas. Ele foi pensado para ser simples, limpo e escalável, servindo como base para projetos mais robustos no futuro.

Se você gostou, deixa uma ⭐ no repositório — isso ajuda demais! 🚀🔥
