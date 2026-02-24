from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "astro-ai backend is running"}
