# backlog.md — NexMeet TTS Fikir Havuzu

- Ses klonlama (GPU'lu ortamda ChatterboxTTS / XTTS) — v2 tasarımına dönüş. Not: v2'deki `core/cloner.py` hiç bağlanmamıştı (`chatterbox` bağımlılıklarda yoktu); başlangıç noktası olarak arşivdeki `SHapeloglu/nexmeet_v2-kokoro-tts-service`'e bakılabilir.
- Toplantı kaydı: v2 serviste `POST /recording/start|stop`, `GET /recording/download/{session_id}` vardı (`core/recorder.py`, ffmpeg ile birleştirme, 24 saat saklama) ama hiçbir ön yüz çağırmıyordu. İstenirse arşivdeki repodan alınabilir.
- Akış (streaming) çıktı: cümle cümle sentez, gecikmeyi düşürmek için (v2'deki chunker/queue fikri).
- Whisper modelini `base`/`small`'a yükseltme denemesi (CPU süresi ölçülerek).
- Çeviri için yerel model (NLLB / Argos) — dış servis bağımlılığını kaldırmak.

## Ekleme Şablonu

```markdown
### Başlık
- **Kategori:** yeni özellik / iyileştirme / teknik borç / araştırma
- **Neden:** kısa gerekçe
- **Notlar:** büyüklük, bağımlılıklar, riskler
```
