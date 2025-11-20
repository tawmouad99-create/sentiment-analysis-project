# Usa un'immagine base leggera di Python
FROM python:3.11-slim

# Definisci la directory di lavoro all'interno del container
WORKDIR /app

# Copia il file delle dipendenze e installale
# Questo passaggio viene fatto prima del codice per ottimizzare il caching di Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia tutti gli altri file nella cartella /app del container 
# (inclusi Fast_API.py e sentimentanalysismodel.pkl)
COPY . .

# Espone la porta usata da FastAPI
EXPOSE 8000

# Comando per avviare l'API
# Usiamo 0.0.0.0 per rendere l'API accessibile dall'esterno del container
# IMPORTANTE: Usiamo Fast_API:app per riflettere il nome del tuo file!
CMD ["python", "-m", "uvicorn", "Fast_API:app", "--host", "0.0.0.0", "--port", "8000"]