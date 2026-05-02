# Vert Agentic Validator

Este projeto é uma plataforma orientada a eventos desenvolvida para o ecossistema de Mercado de Capitais da VERT. O objetivo principal é receber operações financeiras (como CRIs, CRAs e Debêntures), distribuí-las de forma assíncrona via mensageria e validá-las em tempo real utilizando um Agente de Inteligência Artificial com regras de negócio específicas.

---

## Arquitetura e Fluxo de Dados

O projeto adota uma arquitetura de microsserviços desacoplada e orientada a eventos:

1. **Django REST Framework (Produtor):** Atua como a API de persistência das operações no banco de dados **PostgreSQL** e publica cada nova operação no tópico `financial-operations` do **Apache Kafka**.
2. **Apache Kafka (Mensageria):** Orquestra e armazena a fila de operações financeiras de forma resiliente.
3. **Agente de IA / Worker (Consumidor):** Um worker Python independente que consome as mensagens do Kafka, processa as regras de negócio via **LangChain** e valida a operação utilizando a API da **OpenAI** (`gpt-4o-mini`).

---

## Decisões Técnicas

* **Django & DRF:** Construção rápida e segura da API e da camada de persistência.
* **PostgreSQL (Docker):** Banco de dados relacional rodando na porta externa `5433` para evitar conflitos com instâncias locais.
* **Apache Kafka (Docker):** Utilizado para garantir o processamento assíncrono e tolerância a falhas.
* **LangChain & OpenAI (`gpt-4o-mini`):** Framework utilizado para criar a chain de validação com prompts estruturados que retornam respostas estritamente em JSON.
* **Python-dotenv:** Gestão segura de chaves de API e variáveis de ambiente.

---

## Como Rodar o Projeto Localmente

### Pré-requisitos

* Python 3.10 ou superior instalado.
* Docker e Docker Compose instalados na máquina.
* Chave de API da OpenAI (`OPENAI_API_KEY`).

### Passo a Passo

#### 1. Clone o repositório
```bash
git clone [https://github.com/seu-usuario/vert-agentic-validator.git](https://github.com/seu-usuario/vert-agentic-validator.git)
cd vert-agentic-validator