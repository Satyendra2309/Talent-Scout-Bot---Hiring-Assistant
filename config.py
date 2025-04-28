from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MODEL_NAME = "deepseek/deepseek-r1"  # Using DeepSeek R1 model
    API_URL = "https://openrouter.ai/api/v1/chat/completions"  # OpenRouter API endpoint
    MAX_TOKENS = 1000
    TEMPERATURE = 0.7
    INITIAL_GREETING = "Hello! I'm TalentScout Hiring Assistant. Let's begin with your full name."
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    
    if not DEEPSEEK_API_KEY:
        raise ValueError("DEEPSEEK_API_KEY not found in environment variables. Please check your .env file.")
    
    # OpenRouter specific settings
    OPENROUTER_REFERRER = "http://localhost:8501"
    OPENROUTER_TITLE = "TalentScout Hiring Assistant"

class CandidateInfo(BaseModel):
    full_name: str
    email: str
    phone: str
    years_experience: int
    desired_positions: List[str]
    current_location: str
    tech_stack: List[str]

class SessionKeys:
    CHAT_HISTORY = "chat_history"
    CURRENT_STEP = "current_step"
    CANDIDATE_INFO = "candidate_info"
    QUESTIONS_ASKED = "questions_asked"
    CONVERSATION_ACTIVE = "conversation_active"
    LAST_INPUT = "last_input"