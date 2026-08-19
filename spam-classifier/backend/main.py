from fastapi import FastAPI

app = FastAPI(title="Spam Email Classifier")

@app.get("/")
def home():
    return {
        "message": "Spam Email Classifier API is running"
    }