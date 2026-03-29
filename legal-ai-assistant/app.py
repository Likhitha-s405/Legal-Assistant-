from fastapi import FastAPI
from drafter_main import draft_api
from main import get_assistant

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Legal AI Assistant Running"}

@app.post("/summarize")
def summarize(file_path: str):
    assistant = get_assistant()
    return assistant.process_document(file_path)

