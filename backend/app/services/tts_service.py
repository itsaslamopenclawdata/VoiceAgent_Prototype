"""
RepCon Voice Agent - Text-to-Speech Service
"""
import io
import base64
from typing import Optional
import asyncio


class TTSService:
    """Text-to-Speech service using Kokoro"""
    
    # Voice IDs mapped to languages
    VOICES = {
        # English
        "af_sarah": "en_usfemale",
        "af_nicole": "en_usfemale",
        "am_michael": "en_usmale",
        # Hindi
        "hf_psharma": "hi_female",
        "hm_rahul": "hi_male",
        # Telugu
        "hf_telugu": "te_female",
        "hm_telugu": "te_male",
        # Tamil
        "hf_tamil": "ta_female",
        "hm_tamil": "ta_male",
        # Urdu
        "hf_urdu": "ur_female",
        "hm_urdu": "ur_male",
        # Kannada
        "hf_kannada": "kn_female",
        "hm_kannada": "kn_male",
    }
    
    # Language to default voice mapping
    LANGUAGE_VOICES = {
        "en": "af_sarah",
        "hi": "hf_psharma",
        "te": "hf_telugu",
        "ta": "hf_tamil",
        "ur": "hf_urdu",
        "kn": "hf_kannada",
    }
    
    def __init__(self):
        self.model = None
        self._initialized = False
    
    async def initialize(self):
        """Initialize the Kokoro TTS model"""
        if self._initialized:
            return
        
        # Import here to avoid heavy import at startup
        try:
            from kokoro import KModel, Config
            
            # Load model
            loop = asyncio.get_event_loop()
            config = Config()
            self.model = await loop.run_in_executor(
                None,
                lambda: KModel(config)
            )
            self._initialized = True
            print("TTS Model loaded: Kokoro")
        except ImportError:
            print("Warning: Kokoro not installed. Using fallback TTS.")
            self._initialized = True
    
    async def synthesize(
        self,
        text: str,
        voice_id: str = "af_sarah",
        speed: float = 0.9,
        volume: float = 1.0
    ) -> dict:
        """
        Synthesize text to speech
        
        Args:
            text: Text to speak
            voice_id: Voice ID to use
            speed: Speech speed (0.5 to 2.0)
            volume: Volume (0.0 to 1.0)
            
        Returns:
            dict with "audio" (base64), "sample_rate"
        """
        if not self._initialized:
            await self.initialize()
        
        # If Kokoro not available, use fallback
        if self.model is None:
            return await self._fallback_synthesize(text, voice_id, speed)
        
        # Get voice pack name
        voice_pack = self.VOICES.get(voice_id, "en_usfemale")
        
        # Run synthesis
        loop = asyncio.get_event_loop()
        audio_data = await loop.run_in_executor(
            None,
            lambda: self._synthesize_text(text, voice_pack, speed)
        )
        
        # Apply volume
        if volume != 1.0:
            audio_data = self._adjust_volume(audio_data, volume)
        
        # Convert to base64
        audio_b64 = base64.b64encode(audio_data).decode('utf-8')
        
        return {
            "audio": audio_b64,
            "sample_rate": 24000,
            "voice_id": voice_id,
            "text": text
        }
    
    def _synthesize_text(self, text: str, voice_pack: str, speed: float) -> bytes:
        """Internal synthesis method"""
        # This would call Kokoro's model
        # For now, return placeholder
        import struct
        
        # Generate simple sine wave as placeholder
        sample_rate = 24000
        duration = len(text) * 0.05  # Rough estimate
        samples = int(sample_rate * duration)
        
        # Generate simple tone
        import numpy as np
        t = np.linspace(0, duration, samples)
        audio = np.sin(2 * np.pi * 440 * t) * 0.3
        
        # Convert to 16-bit PCM
        audio_int16 = (audio * 32767).astype(np.int16)
        
        # Write to WAV
        buffer = io.BytesIO()
        import wave
        with wave.open(buffer, 'wb') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(sample_rate)
            wav.writeframes(audio_int16.tobytes())
        
        return buffer.getvalue()
    
    def _adjust_volume(self, audio_data: bytes, volume: float) -> bytes:
        """Adjust audio volume"""
        import numpy as np
        import wave
        
        buffer = io.BytesIO(audio_data)
        
        with wave.open(buffer, 'rb') as wav:
            frames = wav.readframes(wav.getnframes())
            audio = np.frombuffer(frames, dtype=np.int16).astype(np.float32)
            audio = audio * volume
            audio = np.clip(audio, -32768, 32767).astype(np.int16)
            
            output = io.BytesIO()
            with wave.open(output, 'wb') as out_wav:
                out_wav.setnchannels(wav.getnchannels())
                out_wav.setsampwidth(wav.getsampwidth())
                out_wav.setframerate(wav.getframerate())
                out_wav.writeframes(audio.tobytes())
            
            return output.getvalue()
    
    async def _fallback_synthesize(
        self,
        text: str,
        voice_id: str,
        speed: float
    ) -> dict:
        """Fallback TTS using gTTS or similar"""
        # Placeholder for fallback
        return {
            "audio": "",
            "sample_rate": 24000,
            "voice_id": voice_id,
            "text": text,
            "fallback": True
        }
    
    def get_voice_for_language(self, language: str) -> str:
        """Get default voice for language"""
        return self.LANGUAGE_VOICES.get(language, "af_sarah")
    
    async def synthesize_streaming(
        self,
        text: str,
        voice_id: str = "af_sarah",
        chunk_size_ms: int = 100
    ) -> AsyncIterator[bytes]:
        """Generate audio in chunks for streaming"""
        # Full synthesis first
        result = await self.synthesize(text, voice_id)
        
        if not result.get("audio"):
            return
        
        # Decode base64
        audio_data = base64.b64decode(result["audio"])
        
        # Chunk the audio
        sample_rate = result.get("sample_rate", 24000)
        bytes_per_ms = sample_rate * 2 // 1000
        chunk_size = chunk_size_ms * bytes_per_ms
        
        for i in range(0, len(audio_data), chunk_size):
            yield audio_data[i:i + chunk_size]


# Singleton instance
tts_service = TTSService()
