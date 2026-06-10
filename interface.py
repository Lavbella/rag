import streamlit as st
import re
import chromadb
import ollama
from pypdf import PdfReader
import shutil
import os
from langchain_text_splitters  import RecursiveCharacterTextSplitter
# Se quiseres usar outras ferramentas do LangChain no futuro:
# from langchain_community.document_loaders import PyPDFLoader 

# Define o host do Ollama (se estiver no Docker usa o nome do serviço, senão usa localhost)
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
client = ollama.Client(host=OLLAMA_HOST)

# Configuração e Base de Dados
st.set_page_config(page_title="AI RAG WITH PDFs", layout="wide")
DB_PATH = "./db"

def inicializar_db():
    # No topo do ficheiro, usa este modo de inicialização mais seguro
    if 'chroma_client' not in st.session_state:
        st.session_state.chroma_client = chromadb.PersistentClient(path=DB_PATH)

    # Inicializa a Coleção (Separado para evitar erros de Rust bindings)
    if 'collection' not in st.session_state:
        try:
            st.session_state.collection = st.session_state.chroma_client.get_or_create_collection(name="minha_memoria")
        except Exception as e:
            # Se falhar, tentamos recriar o cliente
            st.session_state.chroma_client = chromadb.PersistentClient(path=DB_PATH)
            st.session_state.collection = st.session_state.chroma_client.get_or_create_collection(name="minha_memoria")
    
    return 1 # Apenas para confirmar que correu


# Inicia logo ao carregar a página
inicializar_db()

st.title("📄 IA RAG com PDFs - " \
"Local")

with st.sidebar:

    st.header("📚 Documentos na Memória")

    # 1. Procurar todos os metadados na coleção
    todos_dados = st.session_state.collection.get(include=['metadatas'])

    if todos_dados['metadatas']:
        # Extrair nomes únicos dos ficheiros guardados
        ficheiros_na_memoria = sorted(list(set([m['source'] for m in todos_dados['metadatas'] if m])))
        
        if ficheiros_na_memoria:
            for f in ficheiros_na_memoria:
                # Criar duas colunas: 80% para o nome, 20% para o botão
                col_nome, col_btn = st.columns([0.8, 0.2])
                
                col_nome.write(f"📄 {f}")
                
                # Botão de lixo com chave única para cada ficheiro
                if col_btn.button("🗑️", key=f"btn_{f}"):
                    try:
                        # Apaga apenas os pedaços que pertencem a este ficheiro
                        st.session_state.collection.delete(where={"source": f})
                        st.success(f"Removido: {f}")
                        st.rerun() # Atualiza a lista imediatamente
                    except Exception as e:
                        st.error(f"Erro ao apagar: {e}")
        else:
            st.info("Nenhum ficheiro indexado.")
    else:
        st.info("A base de dados está vazia.")

    st.divider()

    st.header("Gestão de Dados")
    
    # --- BOTÃO PARA APAGAR TUDO ---
    if st.button("🗑️ Esvaziar Tabelas", help="Apaga os dados mas mantém a pasta física"):
        try:
            # 1. Usa o cliente que está na sessão para apagar a coleção (a tabela)
            if 'chroma_client' in st.session_state:
                st.session_state.chroma_client.delete_collection(name="minha_memoria")
                
                # 2. Recria a coleção imediatamente (vazia)
                st.session_state.collection = st.session_state.chroma_client.get_or_create_collection(name="minha_memoria")
            
            # 3. Limpa o que está no ecrã (Session State)
            for key in list(st.session_state.keys()):
                # Não apagamos o cliente, apenas os dados e o chat
                if key != 'chroma_client':
                    del st.session_state[key]
            
            st.success("Tabelas limpas com sucesso!")
            st.rerun()

        except Exception as e:
            st.error(f"Erro ao limpar tabelas: {e}")

    st.divider()
    
    # Upload de Ficheiros
    uploaded_file = st.file_uploader("Carregar novo PDF", type="pdf")

    if uploaded_file and st.button("Indexar Documento"):

        # GARANTE que a BD existe antes de escrever
        inicializar_db() 
        
        with st.spinner("A dividir texto e a gerar memória..."):
            reader = PdfReader(uploaded_file)
            texto_completo = ""
            for page in reader.pages:

                # ... dentro do loop das páginas ...
                raw_text = page.extract_text() or ""
                # Mantém apenas letras, números e pontuação básica (remove lixo de imagens)
                texto_limpo = re.sub(r'[^\w\s.,!?;:-]', '', raw_text)

                texto_completo += texto_limpo + "\n"

            # Configurar o divisor inteligente
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=800,    # Tamanho de cada pedaço (caracteres)
                chunk_overlap=80,  # Sobreposição para não perder o contexto entre blocos
                separators=["\n\n", "\n", " ", ""]
            )
            
            # Criar os pedaços
            chunks = text_splitter.split_text(texto_completo)
            
            # Guardar cada pedaço no ChromaDB
            for i, chunk in enumerate(chunks):
                 
                try:
                     
                    # Se o chunk estiver vazio após a limpeza, ignora
                    if len(chunk.strip()) < 5: continue 

                    # res = ollama.embeddings(model="mxbai-embed-large", prompt=chunk, options={"num_ctx": 4096})
                    res = client.embeddings(model="mxbai-embed-large", prompt=chunk, options={"num_ctx": 4096})
                    
                    st.session_state.collection.add(
                        ids=[f"{uploaded_file.name}_{i}"],
                        embeddings=[res["embedding"]],
                        documents=[chunk],
                        metadatas={"source": uploaded_file.name}
                    )

                except Exception as e:
                    # Se um bloco der erro (como o das imagens), ele avisa e continua
                    st.warning(f"Bloco {i} ignorado devido a ruído no PDF.")
                    continue
        
        # --- ONDE ADICIONAR O KEEP_ALIVE ---
        # Isto limpa o modelo da RAM assim que o ficheiro acaba de ser indexado
        # RESET DE MEMÓRIA (KEEP_ALIVE)
        # Força o Ollama a libertar a RAM após terminar este ficheiro
        try:
            ollama.generate(model="mxbai-embed-large", keep_alive=0)    
        except:
            pass
        
        st.success(f"Indexados {len(chunks)} pedaços de texto!")


# --- Área Principal: Chat ---
pergunta = st.text_input("Faz uma pergunta sobre os teus documentos:")

if pergunta:
    with st.chat_message("user"):
        st.write(pergunta)
    
    # 1. Indicador visual de processamento
    status_placeholder = st.info("🔍 A procurar na memória e a gerar resposta...")

    try:
        # 2. Procura no ChromaDB
        res_emb = ollama.embeddings(model="mxbai-embed-large", prompt=pergunta)
        results = st.session_state.collection.query(query_embeddings=[res_emb["embedding"]], n_results=3)
        contexto = "\n".join(results['documents'][0]) if results['documents'] else ""

        # 3. Resposta do Llama 3.1
        with st.chat_message("assistant"):
            prompt = f"Contexto: {contexto}\n\nPergunta: {pergunta}\n\nResponde de forma clara com base no contexto."
            response = ollama.chat(model='llama3.1:8b', messages=[{'role': 'user', 'content': prompt}])
            st.write(response['message']['content'])
            
        # Remove o indicador de "A procurar..." quando a resposta aparece
        status_placeholder.empty()

    except Exception as e:
        st.error(f"Ocorreu um erro: {e}")
