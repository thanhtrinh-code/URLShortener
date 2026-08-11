# Create a new environment for python:  python3 -m venv .venv       
# Activate the environment: source .venv/bin/activate
# Run file: python ___.py

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import model
import hashlib
import uvicorn
import json


Base.metadata.create_all(bind=engine)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/api/create_short_link")
async def create_short_link(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    link, created_at = data.get("link"), data.get("created_at")

    attempt = 0
    code = None

    while True:
        salt = str(attempt) if attempt > 0 else ""
        code = generate_short_code(link, salt)
        check_query = "SELECT 1 FROM urls WHERE short_code = :code LIMIT 1"
        result = db.execute(
            text(check_query),
            {"code": code}
        ).first()
        if result is None:
            break
        attempt += 1

    insert_query = """
        INSERT INTO urls (short_code, original_url, created_at, clicks)
        VALUES (:short_code, :original_url, :created_at, 0)
    """
    db.execute(
        text(insert_query),
        {"short_code": code, "original_url": link, "created_at": created_at}
    )
    db.commit()
    return JSONResponse({"short_code": code})

@app.get("/api/get_original_link")
async def get_original_link(request: Request, db: Session = Depends(get_db)):
    data = await request.json()
    code = data.get("code")

    find_query = "SELECT original_url FROM urls WHERE short_code = :code LIMIT 1"
    result = db.execute(
        text(find_query),
        {"code": code}
    ).first()

    if result is None:
        return JSONResponse({"original_url": None}) 

    return JSONResponse({"original_url": result.original_url})

def generate_short_code(url, salt):
    combined = url + salt
    hash_code = hashlib.sha256(combined.encode()).hexdigest()
    return hash_code[:7]

if __name__ == "__server__":
    port = 8000
    uvicorn.run(app, host="0.0.0.0", port=port)
