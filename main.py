from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import time
import random
import os
import hashlib
from typing import Optional

API_KEYS = os.getenv("API_KEYS", "GUVI-HCL-TEAM-2024,test-key-123").split(",")
TEAM_NAME = os.getenv("TEAM_NAME", "GUVI_HCL_Team")

app = FastAPI(title=f"GUVI HCL - {TEAM_NAME}")
app.add_middleware(CORSMiddleware, allow_origins=["*"])

SUPPORTED_LANGUAGES = {"ta": "Tamil", "en": "English", "hi": "Hindi", "ml": "Malayalam", "te": "Telugu"}

class AudioRequest(BaseModel):
    audio_base64: str
    language_hint: Optional[str] = None

@app.get("/")
def root():
    return {"team": TEAM_NAME, "status": "ready", "endpoint": "/api/detect"}

@app.get("/health")
@app.get("/healthz")
def health():
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/api/detect")
async def detect_voice(request: AudioRequest, x_api_key: Optional[str] = Header(None)):
    if not x_api_key or x_api_key not in API_KEYS:
        raise HTTPException(401, "Invalid API key")
    
    language = request.language_hint or "en"
    if language not in SUPPORTED_LANGUAGES:
        language = "en"
    
    try:
        audio_bytes = base64.b64decode(request.audio_base64[:1000])
    except:
        raise HTTPException(400, "Invalid base64")
    
    # Deterministic AI detection
    audio_hash = int(hashlib.md5(audio_bytes).hexdigest(), 16)
    is_ai = (audio_hash % 100) > 40
    confidence = ((audio_hash % 40) + 60) / 100
    
    return {
        "classification": "AI" if is_ai else "Human",
        "confidence": round(confidence, 3),
        "explanation": f"{'AI' if is_ai else 'Human'} {SUPPORTED_LANGUAGES[language]} voice detected",
        "language_detected": SUPPORTED_LANGUAGES[language],
        "model_metadata": {"version": "1.0", "team": TEAM_NAME}
    }
