# Vert Agentic Validator

Este projeto é uma API REST desenvolvida em Django e Django REST Framework para o ecossistema de Mercado de Capitais da VERT. O objetivo principal é servir como a camada de persistência e gerenciamento de Operações Financeiras (como CRIs e CRAs) que serão validadas por Agentes de IA.

---

## Arquitetura e Decisões Técnicas

A arquitetura foi desenhada pensando em isolamento de ambiente, performance e boas práticas de desenvolvimento:

* **Django & Django REST Framework:** Utilizados para a construção rápida de uma API robusta, segura e de fácil manutenção.
* **PostgreSQL (Docker):** Banco de dados relacional robusto rodando em container para garantir que o ambiente de desenvolvimento seja idêntico ao de produção.
* **Psycopg 3:** Utilizado como driver de conexão com o banco de dados por oferecer melhor suporte nativo a encoding (UTF-8) em sistemas Windows.
* **Isolamento de Portas:** O PostgreSQL do Docker foi mapeado para a porta externa `5433` para evitar conflitos com instâncias locais do Postgres rodando na porta padrão (`5432`).

---

## Como Rodar o Projeto Localmente

### Pré-requisitos

* Python 3.10 ou superior instalado.
* Docker e Docker Compose instalados na máquina.

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/vert-agentic-validator.git](https://github.com/seu-usuario/vert-agentic-validator.git)
    cd vert-agentic-validator
    ```

2.  **Inicie o Banco de Dados no Docker:**
    ```bash
    docker compose up -d
    ```
    *Nota: O banco de dados estará disponível na porta `5433`.*

3.  **Crie e ative o ambiente virtual (Windows):**
    ```powershell
    python -m venv venv
    .\venv\Scripts\Activate
    ```

4.  **Instale as dependências:**
    ```powershell
    python -m pip install --upgrade pip
    pip install django djangorestframework "psycopg[binary]"
    ```

5.  **Execute as migrations do Django:**
    ```powershell
    python manage.py migrate
    ```

6.  **Inicie o servidor de desenvolvimento:**
    ```powershell
    python manage.py runserver
    ```

Acesse a API em seu navegador através do endereço: `http://127.0.0.1:8000/api/operations/`

---

## Endpoints Principais

* `GET /api/operations/` - Lista todas as operações financeiras cadastradas.
* `POST /api/operations/` - Registra uma nova operação para validação.

### Estrutura do Objeto (Financial Operation)

```json
{
  "id": "uuid-v4-gerado-automaticamente",
  "asset_code": "CRI001",
  "issuer": "VERT Securitizadora",
  "volume": "1500000.00",
  "status": "PENDING",
  "created_at": "2026-05-01T18:41:00Z",
  "updated_at": "2026-05-01T18:41:00Z"
}