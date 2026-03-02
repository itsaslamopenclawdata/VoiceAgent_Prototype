"""
RepCon Voice Agent - Speech-to-Text Service
"""
import io
import numpy as np
from typing import Optional, AsyncIterator
import asyncio


class STTService:
    """Speech-to-Text service using faster-whisper"""
    
    def __init__(self, model_size: str = "large-v3"):
        self.model_size = model_size
        self.model = None
        self._initialized = False
    
    async def initialize(self):
        """Initialize the Whisper model"""
        if self._initialized:
            return
        
        # Import here to avoid heavy import at startup
        from faster_whisper import WhisperModel
        
        # Run in executor to avoid blocking
        loop = asyncio.get_event_loop()
        self.model = await loop.run_in_executor(
            None,
            lambda: WhisperModel(
                self.model_size,
                device="cuda",
                compute_type="float16"
            )
        )
        self._initialized = True
        print(f"STT Model loaded: {self.model_size}")
    
    async def transcribe(
        self,
        audio_data: bytes,
        language: Optional[str] = None,
        task: str = "transcribe"
    ) -> dict:
        """
        Transcribe audio to text
        
        Args:
            audio_data: Raw audio bytes
            language: Language code (auto-detect if None)
            task: "transcribe" or "translate"
            
        Returns:
            dict with "text", "language", "segments"
        """
        if not self._initialized:
            await self.initialize()
        
        # Convert bytes to numpy array
        audio_array = self._bytes_to_array(audio_data)
        
        # Run transcription
        loop = asyncio.get_event_loop()
        segments, info = await loop.run_in_executor(
            None,
            lambda: self.model.transcribe(
                audio_array,
                language=language,
                task=task,
                beam_size=5,
                vad_filter=True,
                vad_parameters=dict(
                    min_silence_duration_ms=500
                )
            )
        )
        
        # Collect all segments
        text_parts = []
        segment_list = []
        
        for segment in segments:
            text_parts.append(segment.text)
            segment_list.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text
            })
        
        detected_language = info.language if info.language else language or "en"
        
        return {
            "text": " ".join(text_parts).strip(),
            "language": detected_language,
            "confidence": info.language_probability,
            "segments": segment_list
        }
    
    async def detect_language(self, audio_data: bytes) -> str:
        """Detect language from audio"""
        if not self._initialized:
            await self.initialize()
        
        audio_array = self._bytes_to_array(audio_data)
        
        loop = asyncio.get_event_loop()
        _, info = await loop.run_in_executor(
            None,
            lambda: self.model.transcribe(
                audio_array,
                language=None,
                task="transcribe"
            )
        )
        
        return info.language if info.language else "en"
    
    def _bytes_to_array(self, audio_data: bytes) -> np.ndarray:
        """Convert audio bytes to numpy array"""
        import wave
        
        # Write bytes to buffer
        buffer = io.BytesIO(audio_data)
        
        try:
            with wave.open(buffer, 'rb') as wav:
                # Read audio data
                frames = wav.readframes(wav.getnframes())
                # Convert to numpy array
                audio_array = np.frombuffer(frames, dtype=np.int16)
                # Convert to float32
                audio_array = audio_array.astype(np.float32) / 32768.0
                return audio_array
        except:
            # If not WAV, assume raw 16-bit mono
            return np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
    
    async def transcribe_stream(
        self,
        audio_chunk: bytes,
        language: Optional[str] = None
    ) -> Optional[str]:
        """Transcribe a single audio chunk"""
        result = await self.transcribe(audio_chunk, language)
        
        if result["text"].strip():
            return result["text"].strip()
        
        return None


# Singleton instance
stt_service = STTService()
