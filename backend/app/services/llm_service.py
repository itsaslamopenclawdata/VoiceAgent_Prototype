"""
RepCon Voice Agent - LLM Service (Ollama)
"""
from typing import Optional, AsyncIterator, List, Dict
import asyncio
import json
import httpx


class LLMService:
    """LLM service using Ollama"""
    
    # System prompts for different languages
    SYSTEM_PROMPTS = {
        "en": """You are a professional voice assistant for an educational institute called TechVision Academy.
Your role is to help callers with:
- Providing information about courses
- Answering questions about fees and duration
- Capturing leads (name, phone, email)
- Scheduling callbacks

Guidelines:
- Keep responses concise and clear
- Speak naturally as if on a phone call
- Confirm information before ending
- Always be polite and helpful""",
        
        "hi": """आप TechVision Academy के लिए पेशेवर वॉइस असिस्टेंट हैं।
आपकी भूमिका है:
- पाठ्यक्रमों के बारे में जानकारी देना
- फीस और अवधि के बारे में प्रश्नों का उत्तर देना
- लीड कैप्चर करना (नाम, फोन, ईमेल)
- कॉलबैक शेड्यूल करना

दिशानिर्देश:
- जवाब संक्षिप्त और स्पष्ट रखें
- फोन पर बात करने जैसे स्वाभाविक बोलें
- समाप्त करने से पहले जानकारी की पुष्टि करें
- हमेशा विनम्र और सहायक रहें""",
        
        "te": """మీరు TechVision Academy కి professional voice assistant.
మీ బాధ్యత:
- courses గురిచి information ఇవ్వటం
- fees, duration గురిచి questions answer చేయటం
- leads capture చేయటం (name, phone, email)
- callbacks schedule చేయటం

Guidelines:
- responses concise and clear గా ఉంచండ
- phone call లాగ naturally speak చేయండ
- end చేయక ముందు information confirm చేయండ
- always polite and helpful ఉండండ""",
        
        "ta": """நீங்கள் TechVision Academy-க்கு professional voice assistant.
உங்கள் பணி:
- படிப்புகள் பற்றிய தகவலை வழங்குதல்
- கட்டணம் மற்றும் காலம் பற்றிய கேள்விகளுக்கு பதிலளித்தல்
- லீடுகளைப் பதிவு செய்தல் (பெயர், தொலைபேசி, மின்னஞ்சல்)
- கallsபேக் நேரத்தைத் திட்டமிடுதல்

வழிகாட்டுதல்கள்:
- பதில்கள் சுருக்கமாகவும் தெளிவாகவும் இருக்க வேண்டும்
- தொலைபேசி அழைப்பைப் போல் இயற்கையாகப் பேசுங்கள்
- முடிப்பதற்கு முன் தகவலை உறுதிப்படுத்துங்கள்
- எப்போதும் மரியாதையுடனும் உதவியாகவும் இருங்கள்""",
        
        "ur": """آپ TechVision Academy کے لیے پیشہ ورانہ وائس اسسٹینٹ ہیں۔
آپ کا کردار:
- کورسز کے بارے میں معلومات فراہم کرنا
- فیس اور مدت کے بارے میں سوالات کا جواب دینا
- لیڈز کیپچر کرنا (نام، فون، ای میل)
- کال بیک شیڈول کرنا

ہدایات:
- جوابات مختصر اور واضح رکھیں
- فون پر بات کرنے کی طرح قدرتی بات کریں
- ختم کرنے سے پہلے معلومات کی تصدیق کریں
- ہمیشہ مہذب اور مددگار رہیں""",
        
        "kn": """ನೀವು TechVision Academy ಗೆ professional voice assistant.
ನಿಮ್ಮ ಕಾರ್ಯ:
- ಕೋರ್ಸ್‌ಗಳ ಬಗ್ಗೆ ಮಾಹಿತಿ ನೀಡುವುದು
- ಶುಲ್ಕ ಮತ್ತು ಅವಧಿಯ ಬಗ್ಗೆ ಪ್ರಶ್ನೆಗಳಿಗೆ ಉತ್ತರಿಸುವುದು
- ಲೀಡ್‌ಗಳನ್ನು ಸೆರೆಹಿಡಿಯುವುದು (ಹೆಸರು, ಫೋನ್, ಇಮೇಲ್)
- ಕಾಲ್‌ಬ್ಯಾಕ್ ನಿಗದಿಪಡಿಸುವುದು

ಮಾರ್ಗಸೂಚಿಗಳು:
- ಉತ್ತರಗಳನ್ನು ಸಂಕ್ಷಿಪ್ತ ಮತ್ತು ಸ್ಪಷ್ಟವಾಗಿ ಇರಿಸಿ
- ಫೋನ್ ಕರೆಯಂತೆ ನೈಸರ್ಗಿಕವಾಗಿ ಮಾತನಾಡಿ
- ಕೊನೆಗೊಳಿಸುವ ಮೊದಲು ಮಾಹಿತಿಯನ್ನು ದೃಢೀಕರಿಸಿ
- ಯಾವಾಗಲೂ ವಿನೀತರಾಗಿ ಮತ್ತು ಸಹಾಯಕರಾಗಿ ಇರಿ"""
    }
    
    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "llama3.2"
    ):
        self.base_url = base_url
        self.model = model
        self._client = None
    
    async def initialize(self):
        """Initialize the Ollama client"""
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=60.0
        )
        print(f"LLM Client initialized: {self.model}")
    
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        language: str = "en",
        context: Optional[dict] = None,
        conversation_history: Optional[List[dict]] = None
    ) -> str:
        """
        Generate a response using LLM
        
        Args:
            prompt: User input
            system_prompt: Custom system prompt
            language: Language code
            context: Additional context (courses, etc.)
            conversation_history: Previous messages
            
        Returns:
            Generated response text
        """
        if not self._client:
            await self.initialize()
        
        # Build messages
        messages = []
        
        # System prompt
        sys_prompt = system_prompt or self.SYSTEM_PROMPTS.get(
            language,
            self.SYSTEM_PROMPTS["en"]
        )
        
        # Add context if provided
        if context:
            context_str = self._format_context(context)
            sys_prompt += f"\n\nContext:\n{context_str}"
        
        messages.append({
            "role": "system",
            "content": sys_prompt
        })
        
        # Add conversation history
        if conversation_history:
            messages.extend(conversation_history[-10:])  # Last 10 messages
        
        # Add current prompt
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        # Make request
        try:
            response = await self._client.post(
                "/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "max_tokens": 500
                    }
                }
            )
            
            response.raise_for_status()
            data = response.json()
            
            return data.get("message", {}).get("content", "")
            
        except Exception as e:
            print(f"LLM generation error: {e}")
            return "I'm sorry, I couldn't process that. Could you please repeat?"
    
    async def generate_streaming(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        language: str = "en"
    ) -> AsyncIterator[str]:
        """Generate response with streaming"""
        if not self._client:
            await self.initialize()
        
        messages = [{
            "role": "system",
            "content": system_prompt or self.SYSTEM_PROMPTS.get(language, self.SYSTEM_PROMPTS["en"])
        }, {
            "role": "user",
            "content": prompt
        }]
        
        async with self._client.stream(
            "POST",
            "/api/chat",
            json={
                "model": self.model,
                "messages": messages,
                "stream": True
            }
        ) as response:
            async for line in response.aiter_lines():
                if line.strip():
                    try:
                        data = json.loads(line)
                        content = data.get("message", {}).get("content", "")
                        if content:
                            yield content
                    except:
                        continue
    
    def _format_context(self, context: dict) -> str:
        """Format context for prompt"""
        lines = []
        
        if "courses" in context:
            lines.append("Available Courses:")
            for course in context["courses"][:10]:  # Limit to 10
                lines.append(
                    f"- {course.get('course_name')}: "
                    f"₹{course.get('fee')} for {course.get('duration')}"
                )
        
        return "\n".join(lines)
    
    async def close(self):
        """Close the client"""
        if self._client:
            await self._client.aclose()


# Singleton instance
llm_service = LLMService()
