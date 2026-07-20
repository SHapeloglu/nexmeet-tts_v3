import os
import base64
import tempfile
import logging
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from faster_whisper import WhisperModel
from deep_translator import GoogleTranslator
from kokoro_onnx import Kokoro
import soundfile as sf
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY = os.environ["API_KEY"]  # ortam değişkeni zorunlu, sabit değer yok
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("Whisper modeli yükleniyor...")
stt_model = WhisperModel("tiny", device="cpu", compute_type="int8")
logger.info("✅ Whisper hazır")

logger.info("Kokoro modeli yükleniyor...")
kokoro = Kokoro("kokoro-v1.0.onnx", "voices-v1.0.bin")
logger.info("✅ Kokoro hazır")

HALLUCINATIONS = [
    "altyazı", "subtitle", "abone ol", "subscribe", "m.k",
    "teşekkür", "thanks for watching", "sesli betim",
    "audio description", "bu dizinin", "derneği", "betimleme"
]

class SynthesizeRequest(BaseModel):
    audio_base64: str = ""
    text: str = ""
    peer_id: str
    source_lang: str = "tr"
    target_lang: str = "en"
    session_id: str = ""

class VoiceProfileRequest(BaseModel):
    audio_base64: str
    peer_id: str

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Geçersiz API key")
    return x_api_key

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/voice-profile")
async def save_voice_profile(req: VoiceProfileRequest, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)
    audio_bytes = base64.b64decode(req.audio_base64)
    os.makedirs("voice_profiles", exist_ok=True)
    profile_path = f"voice_profiles/{req.peer_id}.wav"
    with open(profile_path, "wb") as f:
        f.write(audio_bytes)
    logger.info(f"Ses profili kaydedildi: {req.peer_id}")
    return {"success": True, "message": "Ses profili kaydedildi"}

@app.get("/voice-profile/{peer_id}")
async def get_voice_profile(peer_id: str, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)
    profile_path = f"voice_profiles/{peer_id}.wav"
    exists = os.path.exists(profile_path)
    return {"exists": exists}

@app.post("/synthesize")
async def synthesize(req: SynthesizeRequest, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)

    # Metin direkt geldiyse STT'yi atla
    if req.text:
        text = req.text
        logger.info(f"Direkt metin: {text}")
    else:
        # STT ile ses tanı
        audio_bytes = base64.b64decode(req.audio_base64)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(audio_bytes)
            audio_path = f.name

        try:
            segments, _ = stt_model.transcribe(audio_path, language=req.source_lang)
            text = " ".join([s.text for s in segments]).strip()
        finally:
            if os.path.exists(audio_path):
                os.unlink(audio_path)

        if not text:
            raise HTTPException(status_code=400, detail="Ses tanınamadı")

        if any(h in text.lower() for h in HALLUCINATIONS):
            logger.info(f"Halüsinasyon filtrelendi: {text}")
            raise HTTPException(status_code=400, detail="Ses tanınamadı")

        logger.info(f"STT: {text}")

    # Çeviri
    translated = GoogleTranslator(source=req.source_lang, target=req.target_lang).translate(text)
    logger.info(f"Çeviri: {translated}")

    # Kokoro TTS
    if req.target_lang == "en":
        voice = "af_heart"
        lang = "en-us"
    else:
        voice = "af_heart"
        lang = "en-us"

    samples, sample_rate = kokoro.create(translated, voice=voice, speed=1.0, lang=lang)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        out_path = f.name

    try:
        sf.write(out_path, samples, sample_rate)
        with open(out_path, "rb") as f:
            out_bytes = f.read()
    finally:
        if os.path.exists(out_path):
            os.unlink(out_path)

    return {
        "audio_base64": base64.b64encode(out_bytes).decode(),
        "text": text,
        "translated": translated,
        "duration_ms": len(samples) * 1000 // sample_rate
    }
