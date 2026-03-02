# RepCon Voice Agent - Multi-Language Support Update

## Updated: 2026-03-02

---

## Required Languages

| Language | Code | Region |
|----------|------|--------|
| English | en | pan-India |
| Hindi | hi | North India |
| Telugu | te | Andhra Pradesh, Telangana |
| Urdu | ur | South Asia |
| Tamil | ta | Tamil Nadu |
| Kannada | kn | Karnataka |

---

## Multi-Language Support Analysis

### STT (Speech-to-Text) - Open Source

| Model | Languages Supported | Latency | Notes |
|-------|---------------------|---------|-------|
| **faster-whisper** (large-v3) | 100+ languages | ~500ms | Excellent for all Indian languages ✅ |
| WhisperX | 100+ languages | ~600ms | Adds word-level timestamps |
| **Paraformer** (by Alibaba) | Chinese, English, Japanese, Korean, Arabic + 5 Indian | <200ms | Fast, but limited Hindi/Tamil |
| **Silero VAD** | Language-agnostic | <50ms | Best for voice detection |

**Recommendation:** `faster-whisper large-v3` for all 6 languages ✅

---

### TTS (Text-to-Speech) - Open Source

| Model | Languages Supported | Quality | Notes |
|-------|--------------------|---------|-------|
| **Kokoro TTS** | English, Hindi, Tamil, Telugu | ⭐⭐⭐⭐ | Best for Indian languages ✅ |
| Coqui TTS | 110+ languages | ⭐⭐⭐⭐⭐ | Good but heavier |
| **Piper TTS** | English + limited Indic | ⭐⭐⭐ | Fast, low resource |
| VITS | Hindi, Korean, English | ⭐⭐⭐⭐ | Can fine-tune for Indian |

**Recommendation:** Kokoro TTS with custom voices for each language ✅

---

### LLM (Language Model) - Open Source

| Model | Multilingual | Fine-tuned for Indic | Notes |
|-------|-------------|---------------------|-------|
| **Llama 3.2** | Yes | Limited | Can prompt in Hindi/Tamil |
| **Mistral** | Yes | Limited | Good reasoning |
| **Airobor** | Yes | No | Instruct-tuned |
| **IndicBERT** | Indic languages only | Yes | NLU tasks only |

**Recommendation:** 
- Use **Llama 3.2** with language-specific prompts
- For better Indic understanding: **OpenBuddy** or **TigerBot**

---

## Recommended Multi-Language Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  INCOMING CALL                          │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│              LANGUAGE DETECTION                          │
│              (fasttext / langdetect)                     │
│              Detects: en, hi, te, ur, ta, kn           │
└─────────────────────┬───────────────────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
   ┌─────────┐   ┌─────────┐   ┌─────────┐
   │ English │   │  Hindi  │   │ Other   │
   │  STT    │   │   STT   │   │  STT    │
   └────┬────┘   └────┬────┘   └────┬────┘
        │             │             │
        ▼             ▼             ▼
   ┌─────────────────────────────────────────────────┐
   │              OLLAMA LLM                         │
   │         (Prompt in detected language)           │
   └─────────────────────┬───────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
   ┌─────────┐   ┌─────────┐   ┌─────────┐
   │ English │   │  Hindi  │   │  Other  │
   │   TTS   │   │   TTS   │   │   TTS   │
   └─────────┘   └─────────┘   └─────────┘
        │             │             │
        └─────────────┼─────────────┘
                      │
                      ▼
              CALLER RESPONSE
```

---

## Implementation Plan - Multi-Language

### Step 1: Language Detection
```python
# services/language_detection.py
from langdetect import detect, LangDetectException

def detect_language(audio_text: str) -> str:
    """Detect language from transcribed text"""
    try:
        lang = detect(audio_text)
        # Map to supported languages
        lang_map = {
            'en': 'english',
            'hi': 'hindi',
            'te': 'telugu',
            'ur': 'urdu',
            'ta': 'tamil',
            'kn': 'kannada'
        }
        return lang_map.get(lang, 'english')
    except LangDetectException:
        return 'english'
```

### Step 2: Multi-Language STT
```python
# services/stt_handler.py
from faster_whisper import WhisperModel

class STTHandler:
    def __init__(self):
        # Use large-v3 for best Indian language support
        self.model = WhisperModel("large-v3", device="cuda")
    
    def transcribe(self, audio_path: str, language: str = None) -> str:
        # If language specified, use it for better accuracy
        segments, info = self.model.transcribe(
            audio_path,
            language=language,  # 'hi' for Hindi, 'ta' for Tamil, etc.
            task="transcribe"
        )
        return " ".join([s.text for s in segments])
```

### Step 3: Multi-Language TTS
```python
# services/tts_handler.py
from kokoro import KokoroTTS

class TTSHandler:
    def __init__(self):
        # Kokoro voices for Indian languages
        self.voices = {
            'english': 'af_sarah',
            'hindi': 'hf_psharma',  # Hindi voice
            'tamil': 'hf_tamil',    # Tamil voice
            'telugu': 'hf_telugu',  # Telugu voice
            'urdu': 'hf_urdu',      # Urdu voice
            'kannada': 'hf_kannada' # Kannada voice
        }
    
    def speak(self, text: str, language: str = 'english') -> bytes:
        voice = self.voices.get(language, 'af_sarah')
        audio = self.kokoro.generate(text, voice=voice)
        return audio
```

### Step 4: Language-Specific Prompts
```python
# prompts/multilingual.py

SYSTEM_PROMPTS = {
    'english': """You are a helpful voice assistant for an educational institute.
    Provide accurate information about courses, fees, and career opportunities.
    Be polite and concise.""",
    
    'hindi': """आप एक शैक्षणिक संस्थान के लिए एक सहायक वॉइस सहायक हैं।
    पाठ्यक्रम, शुल्क और करियर के अवसरों के बारे में सटीक जानकारी दें।
    विनम्र और संक्षिप्त रहें।""",
    
    'tamil': """நீங்கள் ஒரு கல்வி நிறுவனத்திற்கான உதவியாளர் குரல் உதவியாளர்.
    படிப்புகள், கட்டணங்கள் மற்றும் தொழில் வாய்ப்புகள் பற்றி துல்லியமான தகவல்களை வழங்கவும்.
    மரியாதையுடனும் சுருக்கமாகவும் இருக்கவும்.""",
    
    'telugu': """మీరు విద్యా సంస్థలో ఉత్తమ హెల్ప్‌ఫుల్ వoice assistant.
    కోర్సులు, ఫీజ్‌లు, ఉద్యోగావకాశాల గురించి ఖచ్చితమైన information ఇవ్వండ.
    almostly Polite and concise గా ఉండండ."""
}
```

---

## Updated Tech Stack

| Component | Technology | Multi-Language Support |
|-----------|------------|----------------------|
| **STT** | faster-whisper large-v3 | ✅ All 6 languages |
| **TTS** | Kokoro TTS | ✅ All 6 languages |
| **VAD** | Silero VAD | ✅ Language-agnostic |
| **LLM** | Ollama + Llama 3.2 | ✅ Prompt-based |
| **Lang Detect** | langdetect / fasttext | ✅ 6 languages |

---

## Language Detection Summary

| Language | STT Model | TTS Voice | Prompt |
|----------|-----------|-----------|--------|
| **English** | Whisper large-v3 | af_sarah | English |
| **Hindi** | Whisper large-v3 | hf_psharma | Hindi |
| **Telugu** | Whisper large-v3 | hf_telugu | Telugu |
| **Urdu** | Whisper large-v3 | hf_urdu | Urdu |
| **Tamil** | Whisper large-v3 | hf_tamil | Tamil |
| **Kannada** | Whisper large-v3 | hf_kannada | Kannada |

---

## Updated Docker Services

```yaml
# docker-compose.yml - Add new services
services:
  # ... existing services ...
  
  # Language detection
  lang-detect:
    image: python:3.11
    volumes:
      - ./services:/app
    command: python -c "from langdetect import detect; print('Ready')"

  # Kokoro TTS (custom build)
  kokoro-tts:
    build: ./docker/kokoro
    ports:
      - "5002:5002"
    environment:
      - VOICES=en,hi,ta,te,ur,kn
```

---

## Testing Plan

| Language | Test Phrase | Expected Response |
|----------|-------------|------------------|
| English | "What courses do you offer?" | English response |
| Hindi | "Aap kya courses provide karte ho?" | Hindi response |
| Telugu | "Mee courses ela undi?" | Telugu response |
| Urdu | "Aap kon si courses dete hain?" | Urdu response |
| Tamil | "Enna courses irukku?" | Tamil response |
| Kannada | "Yaaru courses ide?" | Kannada response |

---

## Cost Impact

| Addition | Cost Change |
|----------|-------------|
| larger Whisper model | +10% GPU |
| Multiple TTS voices | Minimal |
| Language detection | Negligible |

**Total Prototype Cost:** ₹2,500-3,500/mo ✅

---

## Conclusion

✅ **YES - The infrastructure CAN support all 6 languages!**

With:
- **faster-whisper large-v3** for STT (all languages)
- **Kokoro TTS** with Indian voices
- **Llama 3.2** with language-specific prompts

The system will detect caller language and respond appropriately.
