import chromadb
import ollama

# 1. Ligar ao ChromaDB
client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection(name="minha_memoria")

# 2. Tua pergunta
pergunta = "Explica-me o que é o sol com base nos teus documentos."

# 3. Procurar o contexto no ChromaDB
response_emb = ollama.embeddings(model="mxbai-embed-large", prompt=pergunta)
results = collection.query(query_embeddings=[response_emb["embedding"]], n_results=1)

# Extrair o texto encontrado
contexto = results['documents'][0][0] if results['documents'] else "Nenhum contexto encontrado."

# 4. Enviar para o Llama 3.1 responder com base no contexto
prompt_final = f"Contexto: {contexto}\n\nPergunta: {pergunta}\n\nResponde apenas com base no contexto acima."

response = ollama.chat(model='llama3.1', messages=[
  {'role': 'user', 'content': prompt_final},
])

print(f"\n🤖 IA: {response['message']['content']}")