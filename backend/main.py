"""FastAPI 应用入口"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from backend.api import routes_chat  # noqa: E402
from backend.api import routes_bazi  # noqa: E402

app = FastAPI(title="AI Fortune Teller API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_chat.router)
app.include_router(routes_bazi.router)


@app.get("/")
async def root():
    return {"message": "AI Fortune Teller API v2.0", "docs": "/docs"}
