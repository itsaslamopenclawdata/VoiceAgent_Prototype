"""
RepCon Voice Agent - Voice Activity Detection Service
"""
import numpy as np
import asyncio
from typing import Optional, AsyncIterator


class VADService:
    """Voice Activity Detection using Silero VAD"""
    
    def __init__(
        self,
        threshold: float = 0.5,
        min_silence_duration_ms: int = 500,
        speech_pad_ms: int = 400
    ):
        self.threshold = threshold
        self.min_silence_duration_ms = min_silence_duration_ms
        self.speech_pad_ms = speech_pad_ms
        self.model = None
        self._initialized = False
    
    async def initialize(self):
        """Initialize Silero VAD model"""
        if self._initialized:
            return
        
        try:
            import torch
            from silero import silero_vad
            
            # Load model
            loop = asyncio.get_event_loop()
            self.model = await loop.run_in_executor(
                None,
                lambda: silero_vad(
                    weights_path=None,  # Use default
                    device="cuda" if torch.cuda.is_available() else "cpu"
                )
            )
            self._initialized = True
            print("VAD Model loaded: Silero VAD")
            
        except ImportError:
            print("Warning: Silero VAD not installed. Using simple threshold.")
            self._initialized = True
    
    async def detect(
        self,
        audio_data: bytes,
        sample_rate: int = 16000
    ) -> bool:
        """
        Detect if audio contains speech
        
        Args:
            audio_data: Audio bytes
            sample_rate: Sample rate (default 16000)
            
        Returns:
            True if speech detected
        """
        if not self._initialized:
            await self.initialize()
        
        # Convert bytes to array
        audio_array = self._bytes_to_array(audio_data, sample_rate)
        
        if audio_array is None or len(audio_array) == 0:
            return False
        
        # If model available, use it
        if self.model is not None:
            return await self._detect_with_model(audio_array, sample_rate)
        
        # Fallback to simple energy detection
        return self._detect_simple(audio_array)
    
    async def _detect_with_model(
        self,
        audio_array: np.ndarray,
        sample_rate: int
    ) -> bool:
        """Detect speech using Silero model"""
        loop = asyncio.get_event_loop()
        
        # Get probabilities
        speech_prob = await loop.run_in_executor(
            None,
            lambda: self.model(
                audio_array,
                sample_rate
            ).item()
        )
        
        return speech_prob > self.threshold
    
    def _detect_simple(self, audio_array: np.ndarray) -> bool:
        """Simple energy-based VAD"""
        # Calculate RMS energy
        rms = np.sqrt(np.mean(audio_array ** 2))
        
        # Threshold for speech
        return rms > 0.02
    
    def _bytes_to_array(
        self,
        audio_data: bytes,
        target_sample_rate: int = 16000
    ) -> Optional[np.ndarray]:
        """Convert audio bytes to numpy array"""
        try:
            import wave
            
            buffer = audio_data
            
            # Try to read as WAV
            try:
                with wave.open(buffer, 'rb') as wav:
                    channels = wav.getnchannels()
                    width = wav.getsampwidth()
                    rate = wav.getframerate()
                    frames = wav.readframes(wav.getnframes())
                    
                    # Convert to numpy
                    if width == 2:  # 16-bit
                        audio = np.frombuffer(frames, dtype=np.int16)
                    else:
                        audio = np.frombuffer(frames, dtype=np.int8)
                    
                    # Convert to mono
                    if channels > 1:
                        audio = audio.reshape(-1, channels).mean(axis=1)
                    
                    # Resample if needed
                    if rate != target_sample_rate:
                        audio = self._resample(audio, rate, target_sample_rate)
                    
                    # Normalize
                    audio = audio.astype(np.float32) / 32768.0
                    
                    return audio
            except:
                # If not WAV, assume raw 16-bit mono
                audio = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
                return audio
                
        except Exception as e:
            print(f"VAD audio conversion error: {e}")
            return None
    
    def _resample(
        self,
        audio: np.ndarray,
        orig_rate: int,
        target_rate: int
    ) -> np.ndarray:
        """Simple resampling"""
        # This is a simple approximation
        ratio = target_rate / orig_rate
        new_length = int(len(audio) * ratio)
        
        indices = np.linspace(0, len(audio) - 1, new_length)
        return np.interp(indices, np.arange(len(audio)), audio).astype(np.float32)
    
    async def get_speech_segments(
        self,
        audio_data: bytes,
        sample_rate: int = 16000
    ) -> list:
        """
        Get speech segments from audio
        
        Returns:
            List of (start_ms, end_ms) tuples
        """
        if not self._initialized:
            await self.initialize()
        
        audio_array = self._bytes_to_array(audio_data, sample_rate)
        
        if audio_array is None or len(audio_array) == 0:
            return []
        
        if self.model is not None:
            return await self._get_segments_with_model(audio_array, sample_rate)
        
        # Fallback: entire audio is speech
        duration_ms = len(audio_array) / sample_rate * 1000
        return [(0, duration_ms)]
    
    async def _get_segments_with_model(
        self,
        audio_array: np.ndarray,
        sample_rate: int
    ) -> list:
        """Get speech segments using model"""
        # This would use Silero's get_speech_timestamps
        # Simplified for now
        duration_ms = len(audio_array) / sample_rate * 1000
        return [(0, duration_ms)]
    
    async def process_stream(
        self,
        audio_chunks: AsyncIterator[bytes],
        sample_rate: int = 16000
    ) -> AsyncIterator[tuple]:
        """
        Process audio stream and yield speech segments
        
        Yields:
            (is_speech: bool, audio_chunk: bytes)
        """
        buffer = b""
        
        async for chunk in audio_chunks:
            buffer += chunk
            
            # Process in chunks
            if len(buffer) >= sample_rate * 0.1:  # 100ms
                is_speech = await self.detect(buffer, sample_rate)
                yield (is_speech, buffer)
                buffer = b""


# Singleton instance
vad_service = VADService()
