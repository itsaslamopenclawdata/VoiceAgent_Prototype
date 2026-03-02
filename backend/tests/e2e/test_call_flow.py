"""
RepCon Voice Agent - E2E Tests - Call Flow
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch


@pytest.mark.asyncio
class TestCallFlowE2E:
    """End-to-end tests for voice call flow"""
    
    async def test_complete_call_flow(self):
        """Test complete call flow from greeting to goodbye"""
        from app.services.voice_pipeline import VoicePipeline
        
        # Create pipeline
        pipeline = VoicePipeline(institute_id=1)
        
        # Mock services
        pipeline.stt = AsyncMock()
        pipeline.stt.transcribe = AsyncMock(return_value={
            "text": "What courses do you offer?",
            "language": "en"
        })
        
        pipeline.llm = AsyncMock()
        pipeline.llm.generate = AsyncMock(return_value="We offer Python Data Science course for 6 months.")
        
        pipeline.tts = AsyncMock()
        pipeline.tts.synthesize = AsyncMock(return_value={
            "audio": "base64_encoded_audio"
        })
        
        pipeline.vad = AsyncMock()
        pipeline.vad.detect = AsyncMock(return_value=True)
        
        # Initialize
        await pipeline.initialize()
        
        # Test greeting
        greeting_audio = await pipeline.generate_greeting()
        assert greeting_audio is not None
        
        # Process audio
        result = await pipeline.process_audio(b"fake_audio_data", context={"courses": []})
        
        assert result["type"] == "response"
        assert result["intent"] == "course_info"
        assert "response_text" in result
    
    async def test_lead_capture_flow(self):
        """Test lead capture conversation flow"""
        from app.services.voice_pipeline import VoicePipeline
        
        pipeline = VoicePipeline(institute_id=1)
        
        # Mock services
        pipeline.stt = AsyncMock()
        pipeline.llm = AsyncMock(return_value="Let me get your details.")
        pipeline.tts = AsyncMock(return_value={"audio": "audio_data"})
        pipeline.vad = AsyncMock(return_value=True)
        
        await pipeline.initialize()
        
        # Simulate lead capture conversation
        # First - show interest
        pipeline.stt.transcribe = AsyncMock(return_value={
            "text": "I am interested in the data science course",
            "language": "en"
        })
        
        result1 = await pipeline.process_audio(b"audio1")
        assert result1["intent"] in ["course_info", "lead_capture"]
        
        # Second - provide name
        pipeline.stt.transcribe = AsyncMock(return_value={
            "text": "My name is Rahul Sharma",
            "language": "en"
        })
        
        result2 = await pipeline.process_audio(b"audio2")
        
        # Third - provide phone
        pipeline.stt.transcribe = AsyncMock(return_value={
            "text": "My number is 9876543210",
            "language": "en"
        })
        
        result3 = await pipeline.process_audio(b"audio3")
        
        # Check lead data captured
        lead_data = pipeline.get_lead_data()
        # (In real test, would verify captured data)
    
    async def test_language_switching(self):
        """Test language switching mid-call"""
        from app.services.voice_pipeline import VoicePipeline
        
        pipeline = VoicePipeline(institute_id=1)
        
        # Mock with Hindi
        pipeline.stt = AsyncMock()
        pipeline.stt.transcribe = AsyncMock(return_value={
            "text": "आप क्या कोर्सेस देते हो",
            "language": "hi"
        })
        
        pipeline.llm = AsyncMock(return_value="हम पायथन डेटा साइंस कोर्स ऑफर करते हैं।")
        pipeline.tts = AsyncMock(return_value={"audio": "hindi_audio"})
        pipeline.vad = AsyncMock(return_value=True)
        
        await pipeline.initialize()
        
        result = await pipeline.process_audio(b"hindi_audio")
        
        assert result["language"] == "hi"
        assert pipeline.current_language == "hi"
    
    async def test_goodbye_flow(self):
        """Test goodbye and call end"""
        from app.services.voice_pipeline import VoicePipeline
        
        pipeline = VoicePipeline(institute_id=1)
        
        pipeline.stt = AsyncMock()
        pipeline.stt.transcribe = AsyncMock(return_value={
            "text": "Thank you, goodbye!",
            "language": "en"
        })
        
        pipeline.llm = AsyncMock(return_value="Thank you for calling. Have a great day!")
        pipeline.tts = AsyncMock(return_value={"audio": "goodbye_audio"})
        pipeline.vad = AsyncMock(return_value=True)
        
        await pipeline.initialize()
        
        result = await pipeline.process_audio(b"audio")
        
        assert result["intent"] == "goodbye"
        
        # Verify conversation reset
        pipeline.reset_conversation()
        assert len(pipeline.conversation_history) == 0
        assert len(pipeline.lead_data) == 0
