from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

from app.rag import router as rag_router
from app.classification import classification_router

app = FastAPI()

app.include_router(rag_router, prefix="/rag")
app.include_router(classification_router, prefix="/classification")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Mental Health Chatbot By Shashank"}

