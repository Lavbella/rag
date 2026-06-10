import chromadb
import ollama
from pypdf import PdfReader

# 1. Configuração
PDF_PATH = "teu_documento.pdf"  # 👈 Coloca aqui o nome do teu ficheiro
client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection(name="minha_memoria")

# 2. Ler o PDF
reader = PdfReader(PDF_PATH)
print(f"📖 A ler {len(reader.pages)} páginas de {PDF_PATH}...")

for i, page in enumerate(reader.pages):
    texto = page.extract_text()
    if texto:
        # Gerar embedding para a página
        res = ollama.embeddings(model="mxbai-embed-large", prompt=texto)
        
        # Guardar no ChromaDB
        collection.add(
            ids=[f"page_{i}"],
            embeddings=[res["embedding"]],
            documents=[texto],
            metadatas=[{"source": PDF_PATH, "page": i}]
        )

print("✅ PDF indexado com sucesso!")

### Por que fazer assim?
###*   **Divisão por páginas:** Se o PDF for muito grande, a IA não consegue ler tudo de uma vez. Ao guardar por páginas, o ChromaDB encontra apenas a página relevante para a tua pergunta.
###*   **Metadados:** Guardamos o número da página para que, no futuro, a IA te possa dizer: *"Encontrei isto na página 5"*.

###**Dica:** Coloca o ficheiro PDF na **mesma pasta** do teu projeto para o script o encontrar facilmente.

###Já tens o teu **primeiro PDF** pronto para testar ou queres que te ajude a melhorar a forma como o texto é dividido (**chunking**) para resultados mais precisos?