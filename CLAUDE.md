# CLAUDE.md — NexMeet TTS Servisi (v3, canlı)

NexMeet'in anlık konuşma çevirisi servisi. Tek dosya FastAPI (`main.py`): ses (base64 WAV) → **faster-whisper tiny** (CPU, int8) ile metin → **GoogleTranslator** (deep-translator) ile çeviri → **Kokoro ONNX** ile İngilizce ses (sabit `af_heart` sesi). Metin doğrudan gelirse STT atlanır. Whisper'ın sık halüsinasyonları ("altyazı", "abone ol" …) filtrelenir.

- GitHub: https://github.com/SHapeloglu/nexmeet-tts_v3 — **PUBLIC repo**
- **Canlı:** bu klasör, `nexmeet-tts.service` → `/root/nexmeet/venv/bin/uvicorn main:app --host 127.0.0.1 --port 5000` (NexMeet backend'in venv'ini paylaşıyor). Çağıran: `/root/nexmeet/backend/main.py` `/api/tts/*` proxy'si.
- Önceki GPU tasarımı: `nexmeet_v2-kokoro-tts-service` (Whisper small + ChatterboxTTS ses klonlama, EC2 g4dn).
- Mimari: `architect.md` · Görevler: `task.md` · Fikirler: `backlog.md` · Günlük: `session.md`

## Komutlar

```bash
sudo systemctl restart nexmeet-tts && journalctl -u nexmeet-tts -f
curl -s 127.0.0.1:5000/health
```

Model dosyaları `kokoro-v1.0.onnx` ve `voices-v1.0.bin` bu klasörde (gitignore'da; repoda yok — yeni kurulumda kokoro-onnx sürümlerinden indirilmeli).

## Kurallar ve Tuzaklar

- `API_KEY` ortam değişkeni **zorunlu** (yoksa başlamaz); şu an systemd unit'inde düz yazılı ve zayıf — değiştirirken backend `.env` `TTS_API_KEY` ile birlikte değiştir.
- `/voice-profile` sesi `voice_profiles/<peer_id>.wav` olarak kaydediyor ama **Kokoro bu profili kullanmıyor** (klonlama yok); `peer_id` dosya yoluna doğrudan giriyor — yol temizliği yapılmadan kullanıcı girdisi olarak genişletme.
- CORS `*` ama servis sadece 127.0.0.1'de dinliyor; dışarı açma.
- Modeller import anında yükleniyor (açılış birkaç saniye); istek başına model yükleme ekleme.
- Oturum sonunda `session.md`'ye kayıt düş, `task.md`'yi güncelle.
