"""
RepCon Voice Agent - Main Voice Pipeline
"""
import asyncio
from typing import Optional, List, Dict, AsyncIterator
from datetime import datetime

from app.services.stt_service import stt_service
from app.services.tts_service import tts_service
from app.services.llm_service import llm_service
from app.services.vad_service import vad_service


class VoicePipeline:
    """Main voice pipeline orchestrator"""
    
    # Intent patterns
    INTENT_PATTERNS = {
        "course_info": [
            "what courses", "which courses", "tell me about courses",
            "courses offered", "what do you teach", "training",
            "कोर्स", "पाठ्यक्रम", "courses"
        ],
        "fee_inquiry": [
            "fee", "fees", "cost", "price", "charges", "how much",
            "शुल्क", "कीमत", "cost"
        ],
        "duration": [
            "how long", "duration", "time", "months", "weeks",
            "अवधि", "कितना समय", "duration"
        ],
        "placement": [
            "job", "placement", "career", "salary", "package",
            "नौकरी", "रोजगार", "job"
        ],
        "lead_capture": [
            "my name", "i am", "i'm", "this is", "call me",
            "interested", "want to join", "enroll",
            "नाम", "मेरा नाम"
        ],
        "goodbye": [
            "thank you", "bye", "goodbye", "see you", "talk to you later",
            "धन्यवाद", "अलविदा", "bye"
        ],
        "callback": [
            "call back", "callback", "contact me", "reach me",
            "वापस कॉल", "संपर्क"
        ]
    }
    
    def __init__(self, institute_id: int = 1):
        self.institute_id = institute_id
        self.conversation_history: List[Dict] = []
        self.current_language = "en"
        self.lead_data: Dict = {}
        self.is_lead_capture_mode = False
        
        # Services
        self.stt = stt_service
        self.tts = tts_service
        self.llm = llm_service
        self.vad = vad_service
    
    async def initialize(self):
        """Initialize all services"""
        await self.stt.initialize()
        await self.tts.initialize()
        await self.llm.initialize()
        await self.vad.initialize()
        print("Voice Pipeline initialized")
    
    async def process_audio(
        self,
        audio_data: bytes,
        context: Optional[Dict] = None
    ) -> Dict:
        """
        Process incoming audio and generate response
        
        Args:
            audio_data: Raw audio bytes
            context: Additional context (courses, etc.)
            
        Returns:
            Dict with response_audio, text, intent, etc.
        """
        # Step 1: Detect speech
        has_speech = await self.vad.detect(audio_data)
        
        if not has_speech:
            return {
                "type": "silence",
                "text": None,
                "response_audio": None
            }
        
        # Step 2: Speech to text
        stt_result = await self.stt.transcribe(
            audio_data,
            language=None  # Auto-detect
        )
        
        user_text = stt_result.get("text", "").strip()
        
        if not user_text:
            return {
                "type": "no_understanding",
                "text": user_text,
                "response_audio": None
            }
        
        # Update language
        if stt_result.get("language"):
            self.current_language = stt_result["language"]
        
        # Step 3: Classify intent
        intent = self.classify_intent(user_text)
        
        # Step 4: Generate response
        if intent == "lead_capture" and not self.is_lead_capture_mode:
            self.is_lead_capture_mode = True
        
        # Build prompt based on intent
        prompt = self._build_prompt(user_text, intent)
        
        # Get course context if available
        llm_context = context or {}
        
        # Generate LLM response
        response_text = await self.llm.generate(
            prompt=prompt,
            language=self.current_language,
            context=llm_context,
            conversation_history=self.conversation_history[-5:]
        )
        
        # Step 5: Text to speech
        voice_id = self.tts.get_voice_for_language(self.current_language)
        tts_result = await self.tts.synthesize(
            text=response_text,
            voice_id=voice_id
        )
        
        # Step 6: Update conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_text,
            "timestamp": datetime.utcnow().isoformat()
        })
        self.conversation_history.append({
            "role": "assistant",
            "content": response_text,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Step 7: Extract lead info if in lead capture mode
        if self.is_lead_capture_mode:
            self._extract_lead_info(user_text)
        
        return {
            "type": "response",
            "text": user_text,
            "response_text": response_text,
            "intent": intent,
            "language": self.current_language,
            "response_audio": tts_result.get("audio"),
            "lead_captured": self._check_lead_complete()
        }
    
    def classify_intent(self, text: str) -> str:
        """Classify user intent from text"""
        text_lower = text.lower()
        
        for intent, patterns in self.INTENT_PATTERNS.items():
            for pattern in patterns:
                if pattern.lower() in text_lower:
                    return intent
        
        # Default to course_info
        return "course_info"
    
    def _build_prompt(self, user_text: str, intent: str) -> str:
        """Build prompt based on intent"""
        prompts = {
            "course_info": f"The caller is asking about courses. Respond with course information. User said: {user_text}",
            "fee_inquiry": f"The caller is asking about fees. Provide fee details. User said: {user_text}",
            "duration": f"The caller is asking about course duration. Provide duration information. User said: {user_text}",
            "placement": f"The caller is asking about placements/jobs. Provide placement information. User said: {user_text}",
            "lead_capture": f"The caller wants to provide their details. Capture their name and phone number. User said: {user_text}",
            "goodbye": f"The caller is saying goodbye. End the call politely. User said: {user_text}",
            "callback": f"The caller wants a callback. Note their phone number. User said: {user_text}"
        }
        
        return prompts.get(intent, user_text)
    
    def _extract_lead_info(self, text: str):
        """Extract lead information from text"""
        import re
        
        text_lower = text.lower()
        
        # Extract name (simple patterns)
        name_patterns = [
            r"my name is (.+)",
            r"i am (.+)",
            r"i'm (.+)",
            r"this is (.+)",
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, text_lower)
            if match:
                self.lead_data["name"] = match.group(1).strip().title()
                break
        
        # Extract phone
        phone_patterns = [
            r"(\+91\d{10})",
            r"(0?\d{10})",
            r"(nine\d{9})",
            r"(nine one \d{9})"
        ]
        
        for pattern in phone_patterns:
            match = re.search(pattern, text_lower.replace(" ", ""))
            if match:
                phone = match.group(1)
                if not phone.startswith("+91"):
                    phone = "+91" + phone
                self.lead_data["phone"] = phone
                break
    
    def _check_lead_complete(self) -> bool:
        """Check if lead capture is complete"""
        required_fields = ["name", "phone"]
        return all(field in self.lead_data for field in required_fields)
    
    def get_lead_data(self) -> Dict:
        """Get captured lead data"""
        return self.lead_data.copy()
    
    def reset_conversation(self):
        """Reset conversation state"""
        self.conversation_history = []
        self.lead_data = {}
        self.is_lead_capture_mode = False
        self.current_language = "en"
    
    async def generate_greeting(self) -> bytes:
        """Generate greeting audio"""
        greeting_text = "Hello! Welcome to TechVision Academy. How can I help you today?"
        
        voice_id = self.tts.get_voice_for_language(self.current_language)
        result = await self.tts.synthesize(greeting_text, voice_id)
        
        if result.get("audio"):
            import base64
            return base64.b64decode(result["audio"])
        
        return b""
    
    async def generate_goodbye(self) -> bytes:
        """Generate goodbye audio"""
        goodbye_text = "Thank you for calling TechVision Academy. Have a great day!"
        
        voice_id = self.tts.get_voice_for_language(self.current_language)
        result = await self.tts.synthesize(goodbye_text, voice_id)
        
        if result.get("audio"):
            import base64
            return base64.b64decode(result["audio"])
        
        return b""


# Create pipeline instance
voice_pipeline = VoicePipeline()
