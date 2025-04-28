# Hiring Assistant Chatbot 🤖

## Project Overview
The Hiring Assistant is an intelligent chatbot designed to streamline the technical interview process. It conducts structured interviews by gathering candidate information and generating relevant technical questions based on the candidate's experience and tech stack. The assistant maintains a natural conversation flow while systematically collecting necessary information and providing appropriate technical assessments.

### Key Features
- Natural conversation flow
- Structured information gathering
- Dynamic technical question generation
- Candidate information validation
- Response caching for improved performance
- Modern, user-friendly interface

## Installation Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

### Setup Steps
1. Clone the repository:
```bash
git clone [repository-url]
cd hiring-assistant
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following variables:
```
DEEPSEEK_API_KEY=your_api_key_here
API_URL=your_api_endpoint_here
```

5. Run the application:
```bash
streamlit run app.py
```

## Usage Guide

1. **Starting the Interview**
   - Launch the application using the command above
   - The chatbot will greet you and begin the interview process

2. **Information Collection**
   - Follow the chatbot's prompts to provide:
     - Your name
     - Email address
     - Phone number
     - Years of experience
     - Desired positions
     - Current location
     - Tech stack

3. **Technical Assessment**
   - The chatbot will generate three technical questions based on your experience
   - Answer each question to the best of your ability

4. **Interview Completion**
   - After completing the technical assessment, you'll receive a closing message
   - The interview data will be saved for review

## Technical Details

### Libraries Used
- `streamlit`: Web application framework
- `requests`: HTTP client for API calls
- `python-dotenv`: Environment variable management
- `logging`: Application logging
- `typing`: Type hints for better code quality

### Model Details
- Utilizes DeepSeek API for natural language processing
- Custom prompt engineering for specific interview scenarios
- Response caching for improved performance
- Error handling and retry mechanisms

### Architecture
- **Frontend**: Streamlit-based web interface
- **Backend**: Python-based chatbot logic
- **Caching**: In-memory caching with TTL
- **State Management**: Streamlit session state
- **Error Handling**: Comprehensive error catching and logging

## Prompt Design

### Information Gathering
Prompts are designed to:
- Maintain a natural conversation flow
- Validate input data
- Progress systematically through required information
- Handle edge cases and invalid inputs

### Technical Question Generation
- Questions are generated based on:
  - Candidate's tech stack
  - Years of experience
  - Desired positions
- Each question is:
  - Technically relevant
  - Experience-appropriate
  - Clearly formatted
  - Numbered for easy reference

## Challenges & Solutions

### Challenge 1: Maintaining Conversation Flow
**Solution**: Implemented a state machine approach with clear conversation steps and validation at each stage.

### Challenge 2: Response Consistency
**Solution**: 
- Added caching mechanism with TTL
- Implemented retry logic for failed API calls
- Standardized response formatting

### Challenge 3: Technical Question Quality
**Solution**:
- Developed specific prompt templates
- Added validation for question count
- Implemented retry mechanism for insufficient questions

### Challenge 4: Performance Optimization
**Solution**:
- Implemented response caching
- Added TTL for cache entries
- Optimized UI rendering
- Used Streamlit's caching decorators

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
[Your chosen license]

## Contact
[Your contact information] 