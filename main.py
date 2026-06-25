from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import query

app = FastAPI(
    title="Natural Language to SQL Engine",
    description="Convert natural language questions to SQL using Claude AI",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query.router)

@app.get("/")
async def root():
    return {
        "message": "Natural Language to SQL Engine",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }
