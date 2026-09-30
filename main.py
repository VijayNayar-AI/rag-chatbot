from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.routes import router


app = FastAPI(
    title="Transformer RAG Chatbot API",
    description="API for the Transformer RAG Chatbot",
    version="1.0.0"
)


app.include_router(router)


app.mount(
    "/",
    StaticFiles(directory="frontend", html=True),
    name="frontend"
)