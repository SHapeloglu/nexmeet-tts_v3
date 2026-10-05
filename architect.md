# architect.md — NexMeet TTS Servisi Mimarisi

```
NexMeet backend (/api/tts/*) ──HTTP, X-API-Key──► main.py (127.0.0.1:5000)
   POST /synthesize {audio_base64 | text, peer_id, source_lang=tr, target_lang=en, session_id}
        ├─ text yoksa: base64 → geçici WAV → WhisperModel("tiny", cpu, int8).transcribe(language=source_lang)
        │              → HALLUCINATIONS filtresi
        ├─ GoogleTranslator(source, target).translate(text)
        └─ Kokoro("kokoro-v1.0.onnx","voices-v1.0.bin").create(text, voice="af_heart", lang="en-us")
             → WAV → base64 yanıt
   POST /voice-profile {audio_base64, peer_id} → voice_profiles/<peer_id>.wav
   GET  /voice-profile/{peer_id} → {exists}
   GET  /health
```

## Mimari Kararlar

- **CPU-only modeller** (Whisper tiny int8 + Kokoro ONNX): GPU sunucusu maliyetinden kaçınmak için; bedeli ses klonlamanın olmaması ve STT doğruluğunun düşmesi.
- **Çeviri dış servise (Google, anahtarsız deep-translator)**: kurulum kolaylığı; kota/erişim garantisi yok.
- **Ses profili saklama korunmuş**: v2 API sözleşmesiyle uyumluluk için; ileride klonlama gelirse kullanılacak.
