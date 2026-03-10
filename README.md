# 🤖 MBA Engenharia de Software com IA — Desafio: Ingestão e Busca com RAG

> Desafio prático do MBA Full Cycle com foco em Engenharia de Software com IA.  
> Esta solução implementa um pipeline completo de **RAG (Retrieval-Augmented Generation)** para ingestão de documentos PDF e consulta via chat conversacional, utilizando embeddings do Google e banco vetorial com PostgreSQL + pgvector.

---

## 📐 Arquitetura da Solução

```
PDF (document.pdf)
       │
       ▼
  [ ingest.py ]  ──► Extrai texto, gera embeddings via Google AI
       │
       ▼
PostgreSQL + pgvector  (coleção vetorial)
       │
       ▼
  [ chat.py ]  ──► Busca semântica + resposta gerada pelo modelo Google
       │
       ▼
   💬 Interface de chat no terminal
```

O fluxo é dividido em duas etapas principais:

1. **Ingestão** — o documento PDF é lido, fragmentado em chunks e cada trecho é convertido em um vetor de embeddings, armazenado no PostgreSQL com a extensão pgvector.
2. **Busca e Chat** — ao receber uma pergunta, o sistema realiza busca semântica nos vetores armazenados e envia os trechos mais relevantes como contexto para o modelo de linguagem, que gera a resposta final.

---

## 🧰 Pré-requisitos

Certifique-se de ter instalado em sua máquina:

- [Docker](https://www.docker.com/) e Docker Compose
- Python 3.10+
- Uma chave de API do [Google AI Studio](https://aistudio.google.com/app/apikey) (`GOOGLE_API_KEY`)

---

## ⚙️ Configuração do Ambiente

### 1. Clone o repositório

```bash
git clone https://github.com/thiag-o/mba-ia-desafio-ingestao-busca.git
cd mba-ia-desafio-ingestao-busca
```

### 2. Crie o arquivo `.env`

Copie o arquivo de exemplo e preencha as variáveis:

```bash
cp .env.example .env
```

Edite o `.env` com seus valores:

```env
# Chave da API do Google AI Studio
GOOGLE_API_KEY=sua_chave_aqui

# Modelo de embeddings do Google (ex: models/text-embedding-004)
GOOGLE_EMBEDDING_MODEL=models/text-embedding-004

# URL de conexão com o banco PostgreSQL (padrão do docker-compose)
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rag

# Nome da coleção vetorial no pgvector
PG_VECTOR_COLLECTION_NAME=documentos

# Caminho para o PDF a ser ingerido
PDF_PATH=document.pdf
```


### 3. Instale as dependências Python

```bash
pip install -r requirements.txt
```

---

## 🚀 Como Executar

### Passo 1 — Suba o banco de dados

```bash
docker compose up -d
```

Isso inicializa um container PostgreSQL com a extensão **pgvector** habilitada, pronto para armazenar os embeddings.

### Passo 2 — Ingira o documento PDF

```bash
python src/ingest.py
```

Este script irá:
- Carregar e processar o PDF definido em `PDF_PATH`
- Dividir o conteúdo em chunks de texto
- Gerar os embeddings via Google AI
- Armazenar os vetores na coleção configurada em `PG_VECTOR_COLLECTION_NAME`

> ✅ Execute este passo apenas uma vez por documento (ou sempre que o PDF for atualizado).

### Passo 3 — Inicie o chat

```bash
python src/chat.py
```

Um chat interativo será aberto no terminal. Você pode fazer perguntas em linguagem natural sobre o conteúdo do documento ingerido. O sistema irá:
- Buscar os trechos mais semanticamente relevantes no banco vetorial
- Enviar o contexto ao modelo do Google para gerar uma resposta precisa

Para encerrar o chat, pressione `Ctrl+C`.

---

## 🗂️ Estrutura do Projeto

```
mba-ia-desafio-ingestao-busca/
├── src/
│   ├── ingest.py          # Pipeline de ingestão do PDF
│   └── chat.py            # Interface de chat com RAG
├── .env.example           # Exemplo de variáveis de ambiente
├── .gitignore
├── docker-compose.yml     # Configuração do PostgreSQL + pgvector
├── document.pdf           # Documento de exemplo para ingestão
├── requirements.txt       # Dependências Python
├── Challange.md           # Enunciado do desafio
└── README.md
```

---

## 🐳 Detalhes do Docker Compose

O `docker-compose.yml` sobe um serviço PostgreSQL configurado com a extensão `pgvector`, necessária para o armazenamento e busca de embeddings.

| Serviço    | Porta | Usuário    | Senha      | Banco |
|------------|-------|------------|------------|-------|
| PostgreSQL | 5432  | `postgres` | `postgres` | `rag` |

---

## 🔑 Variáveis de Ambiente — Referência Completa

| Variável                  | Descrição                                              | Exemplo                                                    |
|---------------------------|--------------------------------------------------------|------------------------------------------------------------|
| `GOOGLE_API_KEY`          | Chave de acesso à API do Google AI                     | `AIzaSy...`                                                |
| `GOOGLE_EMBEDDING_MODEL`  | Modelo de embeddings do Google                         | `models/text-embedding-004`                                |
| `DATABASE_URL`            | String de conexão com o PostgreSQL                     | `postgresql+psycopg://postgres:postgres@localhost:5432/rag`|
| `PG_VECTOR_COLLECTION_NAME` | Nome da coleção de vetores no pgvector               | `documentos`                                               |
| `PDF_PATH`                | Caminho para o arquivo PDF a ser processado            | `document.pdf`                                             |

---

## 🛠️ Tecnologias Utilizadas

- **Python** — linguagem principal
- **LangChain** — orquestração do pipeline RAG
- **Google Generative AI** — embeddings e modelo de linguagem
- **PostgreSQL + pgvector** — armazenamento e busca vetorial
- **Docker** — containerização do banco de dados

---