import ollama
try:
    response = ollama.list()
    print("✅ Conectado ao Ollama!")
    print("Modelos encontrados:", [m['name'] for m in response['models']])
except Exception as e:
    print(f"❌ Erro: {e}")