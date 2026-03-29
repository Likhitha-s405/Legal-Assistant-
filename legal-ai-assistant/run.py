# run.py - Start the FastAPI server
import uvicorn

if __name__ == "__main__":
    print("="*60)
    print("LEGAL AI ASSISTANT - STARTING")
    print("="*60)
    print("Server will run at: http://127.0.0.1:8000")
    print("API docs at: http://127.0.0.1:8000/docs")
    print("="*60)
    
    uvicorn.run(
        "main:app",  # This points to 'app' in main.py
        host="127.0.0.1",
        port=8000,
        reload=True  # Auto-restart when code changes
    )