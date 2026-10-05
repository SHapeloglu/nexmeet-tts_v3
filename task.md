# task.md — NexMeet TTS Görevleri

## 🔜 Sıradaki

- [ ] `API_KEY`'i güçlü değerle değiştir, unit dosyasından `EnvironmentFile`'a taşı (backend `TTS_API_KEY` ile eşle)
- [ ] `peer_id` için güvenli dosya adı (ör. hash veya `[A-Za-z0-9_-]` kontrolü) — `/voice-profile` path traversal riski
- [ ] `requirements.txt` ekle (faster-whisper, kokoro-onnx, deep-translator, soundfile, numpy, fastapi, uvicorn) ve model indirme adımlarını README'ye yaz
- [ ] Hedef dil `en` değilse de `af_heart`/`en-us` kullanılıyor — dil → ses eşlemesi

## 🚧 Devam Eden

_(şu anda boş)_

## ✅ Tamamlanan

- [x] 2026-10-05 — Çalışma dosyaları kod ve servis tanımı incelenerek yeniden yazıldı
- [x] 2026-07-20 — İlk commit; `API_KEY` zorunlu ortam değişkeni oldu
