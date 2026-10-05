# NexMeet TTS Servisi

[NexMeet](https://github.com/SHapeloglu/nexmeet_v3) video konferans uygulamasının **anlık konuşma çevirisi** servisi. Konuşmacının sesini metne çevirir, metni hedef dile tercüme eder ve İngilizce konuşma sesi üretir — tamamen CPU üzerinde.

```
ses (base64 WAV) ─► faster-whisper "tiny" (STT) ─► Google Translate (TR→EN) ─► Kokoro ONNX (TTS) ─► ses (base64 WAV)
```

Metin doğrudan gönderilirse STT adımı atlanır. Whisper'ın sessizlikte ürettiği tipik halüsinasyonlar ("altyazı", "abone ol" vb.) filtrelenir.

## Kurulum

```bash
python -m venv venv && . venv/bin/activate
pip install fastapi uvicorn pydantic faster-whisper deep-translator kokoro-onnx soundfile numpy
```

Kokoro model dosyalarını bu klasöre indirin (git'e girmez):

- `kokoro-v1.0.onnx`
- `voices-v1.0.bin`

(kaynak: [kokoro-onnx sürümleri](https://github.com/thewh1teagle/kokoro-onnx/releases))

## Çalıştırma

`API_KEY` ortam değişkeni **zorunludur**:

```bash
export API_KEY="<uzun-rastgele-anahtar>"
uvicorn main:app --host 127.0.0.1 --port 5000
```

NexMeet backend'inde aynı değer `TTS_API_KEY`, servis adresi `TTS_SERVICE_URL` olarak tanımlanmalıdır.

## API

Tüm istekler `X-API-Key` başlığı ister.

| Uç nokta | Açıklama |
|---|---|
| `GET /health` | Durum |
| `POST /synthesize` | `{audio_base64 \| text, peer_id, source_lang="tr", target_lang="en", session_id}` → çevrilmiş metin + ses |
| `POST /voice-profile` | `{audio_base64, peer_id}` — ses örneği kaydeder |
| `GET /voice-profile/{peer_id}` | Profil var mı |

## Sınırlamalar

- Ses klonlama yoktur; tüm çıktı aynı İngilizce sesle (`af_heart`) üretilir. Kaydedilen ses profilleri şimdilik kullanılmaz.
- Çeviri dış servise (Google) bağlıdır.
- Servisi yalnız yerel ağda / `127.0.0.1` üzerinde çalıştırın.

GPU ve ses klonlamalı önceki tasarım: [nexmeet_v2-kokoro-tts-service](https://github.com/SHapeloglu/nexmeet_v2-kokoro-tts-service).
