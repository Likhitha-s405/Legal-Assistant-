from fastapi import FastAPI
from drafter_main import draft_api
from summarizer_main import assistant

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Legal AI Assistant Running"}

@app.post("/summarize")
def summarize(file_path: str):
    return assistant.process_document(file_path)

@app.post("/draft")
def draft(data: dict):
    return draft_api(data)