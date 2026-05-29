FROM ollama/ollama:latest

# Permitir conexiones desde cualquier origen (Frontend) y escuchar en todas las interfaces
ENV OLLAMA_ORIGINS="*"
ENV OLLAMA_HOST="0.0.0.0"

EXPOSE 11434

# Lanzamos el servidor de Ollama de forma nativa
ENTRYPOINT ["ollama", "serve"]