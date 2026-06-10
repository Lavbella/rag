import chromadb
import ollama

# 1. Ligar à base de dados que já criaste
client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection(name="minha_memoria")

# 2. A tua pergunta
pergunta = "O que é o sol?"

# 3. Gerar o embedding da pergunta (tem de ser o mesmo modelo que usaste para guardar!)
response = ollama.embeddings(model="mxbai-embed-large", prompt=pergunta)
query_embedding = response["embedding"]

# 4. Procurar no ChromaDB os 2 resultados mais parecidos
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=2
)

# 5. Mostrar o que a "memória" encontrou
print(f"\n🔍 Pergunta: {pergunta}")
print("-" * 30)
for doc in results['documents'][0]:
    print(f"📖 Resultado encontrado: {doc}")
