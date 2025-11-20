import pickle
from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator

# 1. Inizializziamo l'App
app = FastAPI(title="Sentiment Analysis API")

# 2. Configuriamo Prometheus per il monitoraggio
# Questo crea automaticamente l'endpoint /metrics che useremo dopo
Instrumentator().instrument(app).expose(app)

# 3. Carichiamo il modello all'avvio
# Nota: Assicurati che il nome del file sia identico a quello che hai scaricato
MODEL_FILE = "sentiment_analysis_model.pkl"

try:
    with open(MODEL_FILE, 'rb') as f:
        model = pickle.load(f)
    print("Modello caricato correttamente!")
except FileNotFoundError:
    print(f"ERRORE: Il file {MODEL_FILE} non è stato trovato nella cartella.")
    model = None

# 4. Definiamo il formato dei dati in input (deve essere un JSON)
class ReviewRequest(BaseModel):
    review: str

# 5. Endpoint per la previsione
@app.post("/predict")
def predict_sentiment(request: ReviewRequest):
    if not model:
        return {"error": "Modello non caricato"}
    
    # Il modello si aspetta una lista di testi
    prediction = model.predict([request.review])
    
    # Restituiamo il risultato (es. "positive" o "negative")
    return {
        "review": request.review,
        "sentiment": prediction[0]
    }

# 6. Endpoint di test (opzionale, giusto per vedere se l'app è viva)
@app.get("/")
def read_root():
    return {"status": "API is running", "model_loaded": model is not None}