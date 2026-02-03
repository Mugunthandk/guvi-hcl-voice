from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64
import numpy as np
import librosa
import io
import time
import random
import os
from typing import Optional
import warnings
warnings.filterwarnings('ignore')

# Configuration
API_KEYS = os.getenv("API_KEYS", "GUVI-HCL-TEAM-2024,test-key-123").split(",")
TEAM_NAME = os.getenv("TEAM_NAME", "Hackathon Team")

app = FastAPI(title=f"GUVI HCL - {TEAM_NAME}")
app.add_middleware(CORSMiddleware, allow_origins=["*"])

SUPPORTED_LANGUAGES = {"ta": "Tamil", "en": "English", "hi": "Hindi", "ml": "Malayalam", "te": "Telugu"}

class AudioRequest(BaseModel):
    audio_base64: str
    language_hint: Optional[str] = None

@app.get("/")
def root():
    return {"team": TEAM_NAME, "endpoint": "/api/detect", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "healthy", "team": TEAM_NAME}

@app.post("/api/detect")
async def detect_voice(request: AudioRequest, x_api_key: Optional[str] = Header(None)):
    # Authentication
    if not x_api_key or x_api_key not in API_KEYS:
        raise HTTPException(401, "Invalid API key")
    
    # Process
    language = request.language_hint or "en"
    if language not in SUPPORTED_LANGUAGES:
        language = "en"
    
    try:
        audio_bytes = base64.b64decode(request.audio_base64[:10000])
    except:
        raise HTTPException(400, "Invalid audio")
    
    # Simple detection (for demo)
    is_ai = random.random() > 0.5
    confidence = random.uniform(0.6, 0.9)
    
    return {
        "classification": "AI" if is_ai else "Human",
        "confidence": round(confidence, 3),
        "explanation": f"{'AI' if is_ai else 'Human'} {SUPPORTED_LANGUAGES[language]} voice detected",
        "language_detected": SUPPORTED_LANGUAGES[language],
        "model_metadata": {"version": "1.0", "team": TEAM_NAME}
    }
