import chromadb
import ollama

# 1. Inicializar o ChromaDB (vai criar uma pasta 'db' no teu projeto)
client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection(name="minha_memoria")

# 2. Texto para guardar
documento = "O sol é uma estrela de tipo espectral G2V."

# 3. Gerar o "DNA" (embedding) do texto usando o Ollama
response = ollama.embeddings(model="mxbai-embed-large", prompt=documento)
embedding = response["embedding"]

# 4. Guardar na base de dados
collection.add(
    ids=["id1"],
    embeddings=[embedding],
    documents=[documento]
)

print("✅ Documento guardado e indexado no ChromaDB!")