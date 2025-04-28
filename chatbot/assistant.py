import re
import time
import requests
import logging
from typing import Dict, Any, List
from config import Config, CandidateInfo
from functools import lru_cache

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HiringAssistant:
    def __init__(self):
        self.api_key = Config.DEEPSEEK_API_KEY
        self.api_url = Config.API_URL
        logger.info(f"Initializing HiringAssistant with API URL: {self.api_url}")
        self.candidate_info = {
            "full_name": "",
            "email": "",
            "phone": "",
            "years_experience": 0,
            "desired_positions": [],
            "current_location": "",
            "tech_stack": []
        }
        self.current_step = "greeting"
        self.conversation_history = []
        self._response_cache = {}
        self._cache_ttl = 3600  # Cache TTL in seconds (1 hour)
        self._cache_timestamps = {}

    def start_conversation(self) -> str:
        self.current_step = "greeting"
        return Config.INITIAL_GREETING

    def _format_prompt(self, user_input: str) -> str:
        """Dynamically format prompts based on conversation step."""
        if self.current_step == "technical_assessment":
            return (
                "Generate 3 short technical interview questions (only the questions, no explanation) "
                f"for a candidate with {self.candidate_info.get('years_experience', 0)} years of experience in "
                f"{', '.join(self.candidate_info.get('tech_stack', []))}."
            )
        return user_input

    @lru_cache(maxsize=32)
    def generate_response(self, prompt: str) -> str:
        # Generate a more robust cache key
        cache_key = f"{hash(prompt)}_{self.current_step}_{hash(str(self.candidate_info))}"
        
        # Check cache with TTL
        current_time = time.time()
        if cache_key in self._response_cache:
            if current_time - self._cache_timestamps.get(cache_key, 0) < self._cache_ttl:
                logger.info("Using cached response")
                return self._response_cache[cache_key]
            else:
                # Cache expired, remove old entry
                del self._response_cache[cache_key]
                del self._cache_timestamps[cache_key]

        max_retries = 2
        retry_delay = 3
        
        for attempt in range(max_retries):
            try:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:8501",
                    "X-Title": "TalentScout Hiring Assistant"
                }
                
                payload = {
                    "model": Config.MODEL_NAME,
                    "messages": [
                        {"role": "system", "content": "You are a professional hiring assistant conducting technical interviews."},
                        {"role": "user", "content": self._format_prompt(prompt)}
                    ],
                    "temperature": Config.TEMPERATURE,
                    "max_tokens": Config.MAX_TOKENS,
                    "stream": False
                }
                
                logger.info(f"Making API request to {self.api_url}")
                logger.info(f"Request payload: {payload}")
                
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 400:
                    logger.error(f"Bad Request. Response: {response.text}")
                    return "Error: Invalid request format. Please try again."
                
                if response.status_code == 401:
                    logger.error("Authentication failed. Please check your API key.")
                    return "Authentication error: Please check your API key configuration."
                
                response.raise_for_status()
                response_data = response.json()
                logger.info(f"API raw response: {response_data}")  # Log the raw API response
                
                # Improved error handling for missing or unexpected fields
                if "choices" not in response_data or not response_data["choices"]:
                    logger.error(f"No 'choices' field or empty choices in response: {response_data}")
                    return f"Error: Unexpected API response format. See logs for details."
                if "message" not in response_data["choices"][0]:
                    logger.error(f"Missing 'message' in choices: {response_data['choices'][0]}")
                    return f"Error: Unexpected API response format. See logs for details."
                msg = response_data["choices"][0]["message"]
                response_text = msg.get("content", "")
                if not response_text and "reasoning" in msg:
                    logger.info("Using 'reasoning' field as fallback for response_text.")
                    response_text = msg["reasoning"]
                if not response_text:
                    logger.error(f"No usable content in API response: {msg}")
                    return "Error: The model did not return any usable content."
                
                # Cache the response with timestamp
                self._response_cache[cache_key] = response_text
                self._cache_timestamps[cache_key] = current_time
                return response_text
            except requests.exceptions.RequestException as e:
                logger.error(f"API request failed: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                return f"API request failed: {str(e)}"
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                return f"An unexpected error occurred: {str(e)}"

    def process_input(self, user_input: str) -> str:
        self.conversation_history.append({"role": "user", "content": user_input})

        # Handle conversation flow
        if self.current_step == "greeting":
            self.candidate_info["full_name"] = user_input
            self.current_step = "email"
            return f"Nice to meet you, {user_input}! What's your email address?"

        elif self.current_step == "email":
            if not self.validate_email(user_input):
                return "Invalid email. Please try again (e.g., name@example.com)"
            self.candidate_info["email"] = user_input
            self.current_step = "phone"
            return "Great! What's your phone number? (e.g., +1234567890)"

        elif self.current_step == "phone":
            if not self.validate_phone(user_input):
                return "Invalid phone number. Please try again."
            self.candidate_info["phone"] = user_input
            self.current_step = "experience"
            return "How many years of professional experience do you have?"

        elif self.current_step == "experience":
            try:
                years = int(user_input)
                self.candidate_info["years_experience"] = years
                self.current_step = "position"
                return "What position(s) are you interested in? (Separate with commas)"
            except ValueError:
                return "Please enter a valid number."

        elif self.current_step == "position":
            positions = [pos.strip() for pos in user_input.split(",")]
            self.candidate_info["desired_positions"] = positions
            self.current_step = "location"
            return "What's your current location?"

        elif self.current_step == "location":
            self.candidate_info["current_location"] = user_input
            self.current_step = "tech_stack"
            return "List your tech stack (e.g., Python, JavaScript, React):"

        elif self.current_step == "tech_stack":
            tech_stack = [tech.strip() for tech in user_input.split(",")]
            self.candidate_info["tech_stack"] = tech_stack
            self.current_step = "technical_assessment"
            return self.generate_technical_questions()

        elif self.current_step == "technical_assessment":
            self.current_step = "complete"
            return self._generate_closing_message()

        elif self.current_step == "complete":
            return "Thank you for your time! The assessment is now complete. Have a great day!"

        return "Let's continue!"

    def generate_technical_questions(self) -> str:
        prompt = (
            "You are a technical interviewer. Generate exactly 3 technical interview questions. "
            "Format: Number each question (1., 2., 3.) and put each on a new line. "
            "Do not include any explanations, reasoning, or additional text. "
            "Only output the numbered questions. "
            f"Topics to cover: {', '.join(self.candidate_info.get('tech_stack', []))}. "
            f"Candidate experience: {self.candidate_info.get('years_experience', 0)} years. "
            "IMPORTANT: You must generate exactly 3 questions, no more and no less."
        )
        response = self.generate_response(prompt)
        
        # Clean up the response to ensure we only get exactly 3 questions
        lines = response.split('\n')
        questions = []
        for line in lines:
            line = line.strip()
            if line and (line.startswith(('1.', '2.', '3.', '1)', '2)', '3)')) or line[0].isdigit()):
                questions.append(line)
                if len(questions) == 3:
                    break
        
        # If we don't have exactly 3 questions, generate a new response
        if len(questions) != 3:
            logger.warning("Did not get exactly 3 questions, retrying...")
            return self.generate_technical_questions()
            
        return '\n'.join(questions)

    def validate_email(self, email: str) -> bool:
        return bool(re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email))

    def validate_phone(self, phone: str) -> bool:
        return bool(re.match(r'^\+?1?\d{9,15}$', phone))

    def get_conversation_summary(self) -> Dict[str, Any]:
        return {
            "candidate_info": self.candidate_info,
            "conversation_history": self.conversation_history
        }

    def _generate_closing_message(self) -> str:
        return """
        Thank you for taking the time to interview with us today. It was a pleasure discussing your experience and qualifications. 
        Our team will review your interview feedback, and we'll be in touch within the next week to share updates on next steps. 
        Please feel free to reach out with any questions in the meantime. We appreciate your interest in the role!
        """