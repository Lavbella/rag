# AI RAG: Document Intelligence with LangChain, ChromaDB & Ollama

---

## 🌍 Language / Idioma
* [Português (#-português)](#-português)
* [English (#-english)](#-english)

---

## 🇵🇹 Português

Este projeto implementa um ecossistema de **RAG (Retrieval-Augmented Generation)** utilizando modelos de linguagem locais via Ollama. A aplicação permite carregar documentos PDF, processá-los em pedaços (chunks), indexá-los numa base de dados vetorial e interagir com o conteúdo através de um chat inteligente.

### Estrutura de Evolução Contínua
O projeto foi desenhado seguindo uma abordagem de desenvolvimento incremental. Cada script representa um passo consecutivo em direção à arquitetura final:
1. **`ler_pdf.py`**: Extração de texto cru a partir dos PDFs da pasta `docs`.
2. **`testeChromaDB_docDNA.py`**: Testes de embeddings e indexação de vetores no ChromaDB.
3. **`responde_pergunta.py`**: Pesquisa semântica e geração de respostas com o modelo.
4. **`chatbot_rag.py`**: Consolidação da lógica RAG e histórico em modo terminal.
5. **`interface.py` (Versão Final)**: A aplicação definitiva que integra todos os passos anteriores numa interface gráfica Streamlit.
6. **`teste.py`**: Sandbox isolada para testes rápidos.

### Pré-requisitos (O que é necessário instalar)
Antes de começar, precisa de instalar na sua máquina local:
1. [Git](https://git-scm.com) (Para descarregar o código).
2. [Docker e Docker Compose](https://docker.com) (Recomendado para execução isolada).
3. [Python 3.10 ou superior](https://python.org) (Apenas se pretender correr localmente sem Docker).
4. [Ollama](https://ollama.com) (Caso corra fora do Docker, necessita do Ollama instalado e do modelo ativo, ex: `ollama run llama3` ou o modelo à sua escolha).

---

## Como Executar o Projeto

### 1. Fazer o Pull (Clonar) do Repositório
Abra o seu terminal e execute o comando abaixo para descarregar o projeto:
```bash
git clone https://github.com/Lavbella/rag.git
cd rag
```

### 2. Opção A: Criar o Ambiente Python Local (Via requirements.txt)
Se preferir correr o projeto diretamente na sua máquina para desenvolvimento:

```bash
# 1. Criar o ambiente virtual
python -m venv venv

# 2. Ativar o ambiente virtual
# No Windows (Prompt de Comando):
venv\Scripts\activate
# No Windows (PowerShell):
.\venv\Scripts\activate
# No Linux/macOS:
source venv/bin/activate

# 3. Instalar todas as dependências do projeto
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Opção B: Criar o Docker a partir dos Ficheiros de Configuração (Recomendado)
O Docker Compose lê o seu `Dockerfile` e `docker-compose.yaml` para construir a aplicação com todas as ferramentas isoladas, incluindo a recriação limpa de imagens e volumes (garantindo que a base de dados `db/` e os documentos `docs/` são reprocessados do zero):

```bash
# Parar o ambiente anterior e apagar volumes antigos (Limpeza total de cache/vetores)
docker compose down -v

# Construir as imagens a partir do Dockerfile e iniciar os componentes
docker compose up -d --build
```

### 4. Como Correr no Final
Dependendo da opção de ambiente que escolheu nos passos anteriores, use o comando respetivo para iniciar a **versão final (`interface.py`)**:

* **Se utilizou o Ambiente Python Local:**
  ```bash
  streamlit run interface.py
  ```
* **Se utilizou a execução via Docker:**
  O contentor já inicia o Streamlit automaticamente em segundo plano.

**Aceder à Aplicação:**
Abra o seu navegador de internet e aceda ao painel gráfico do Streamlit:
* **URL:** [http://localhost:8501](http://localhost:8501)

---

## 🇬🇧 English

This project implements a **RAG (Retrieval-Augmented Generation)** ecosystem powered by local LLMs via Ollama. The application allows you to upload PDF documents, process them into chunks, index them into a vector database, and converse with your data through an intelligent chat interface.

### Continuous Evolution Structure
The codebase is designed following an incremental development approach. Each script represents a consecutive step leading up to the final application architecture:
1. **`ler_pdf.py`**: Raw text extraction from PDFs inside the `docs` folder.
2. **`testeChromaDB_docDNA.py`**: Testing embeddings generation and vector indexing within ChromaDB.
3. **`responde_pergunta.py`**: Semantic search logic and answer generation using the LLM.
4. **`chatbot_rag.py`**: Consolidation of core RAG logic and conversation history in terminal mode.
5. **`interface.py` (Final Version)**: The definitive application integrating all stages into a polished Streamlit web UI.
6. **`teste.py`**: Isolated sandbox for quick feature experiments.

### Prerequisites (What needs to be installed)
Before starting, ensure you have the following installed on your host machine:
1. [Git](https://git-scm.com) (To download the code).
2. [Docker & Docker Compose](https://docker.com) (Recommended for isolated execution).
3. [Python 3.10 or higher](https://python.org) (Only if running locally without Docker).
4. [Ollama](https://ollama.com) (If running outside Docker, you need Ollama installed and the model downloaded, e.g., `ollama run llama3`).

---

## How to Run the Project

### 1. Pull (Clone) the Repository
Open your terminal and run the following command to download the project:
```bash
git clone https://github.com/Lavbella/rag.git
cd rag
```

### 2. Option A: Setup the Local Python Environment (Via requirements.txt)
If you prefer running the project directly on your machine for development purposes:

```bash
# 1. Create the virtual environment
python -m venv venv

# 2. Activate the virtual environment
# On Windows (Command Prompt):
venv\Scripts\activate
# On Windows (PowerShell):
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

# 3. Install all project python components
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Option B: Create the Docker Environment from Configuration Files (Recommended)
Docker Compose will read your `Dockerfile` and `docker-compose.yaml` to build the app with all components isolated, forcing a clean recreation of images and volumes (ensuring that the `db/` vector database and `docs/` folder are fresh):

```bash
# Stop previous environment and wipe old volumes (Clear cache/vector db completely)
docker compose down -v

# Build the images from the Dockerfile and launch all configuration components
docker compose up -d --build
```

### 4. How to Run in the End
Depending on the environment choice you made above, use the corresponding command to launch the **final version (`interface.py`)**:

* **If using the Local Python Environment:**
  ```bash
  streamlit run interface.py
  ```
* **If using Docker Execution:**
  The container automatically spins up Streamlit in the background.

**Accessing the Application:**
Open your web browser and navigate to the Streamlit graphical UI:
* **URL:** [http://localhost:8501](http://localhost:8501)

---

## License / Licença
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

