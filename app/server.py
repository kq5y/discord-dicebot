import uvicorn
from fastapi import FastAPI
from threading import Thread

app = FastAPI()

@app.get("/")
def main():
    return {"message": "dicebot is running!"}

def run():
    uvicorn.run(app)

def keep_alive():
    server = Thread(target=run)
    server.start()
