# 🤖 Hiring Assistant Chatbot

A sophisticated AI-powered hiring assistant that conducts technical interviews and gathers candidate information through natural conversation.

## 🚀 Project Overview

The Hiring Assistant is an intelligent chatbot designed to streamline the technical interview process. It:
- Conducts structured interviews through natural conversation
- Gathers essential candidate information (contact details, experience, tech stack)
- Generates relevant technical questions based on candidate's background
- Maintains conversation context and provides appropriate responses
- Caches responses for improved performance

## 🛠️ Installation Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
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

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with:
   ```
   DEEPSEEK_API_KEY=your_api_key_here
   ```
   
   ⚠️ **Important Security Note**: 
   - The `.env` file is excluded from version control (see `.gitignore`)
   - Never commit your `.env` file to the repository
   - Keep your API keys secure and never share them publicly
   - For deployment, use environment variables or secure secret management systems

5. Run the application:
   ```bash
   streamlit run app.py
   ```

## 📖 Usage Guide

1. Start the application using the command above
2. The chatbot will initiate the conversation with a greeting
3. Follow the prompts to provide your information:
   - Full name
   - Email address
   - Phone number
   - Years of experience
   - Desired positions
   - Current location
   - Tech stack
4. Answer the technical questions provided
5. Receive a closing message with next steps

## 🔧 Technical Details

### Libraries Used
- `streamlit`: Web application framework
- `requests`: HTTP client for API calls
- `python-dotenv`: Environment variable management
- `logging`: Application logging
- `typing`: Type hints for better code quality

### Model Details
- Uses DeepSeek API for natural language processing
- Implements response caching for improved performance
- Custom prompt engineering for specific interview scenarios

### Architecture
- **Frontend**: Streamlit-based web interface
- **Backend**: Python-based chatbot logic
- **Caching**: In-memory caching with TTL
- **State Management**: Streamlit session state

## 🎯 Prompt Design

The chatbot uses carefully crafted prompts for different stages:

1. **Information Gathering**:
   - Structured prompts for collecting candidate details
   - Validation rules for email and phone numbers
   - Context-aware follow-up questions

2. **Technical Questions**:
   - Dynamic question generation based on:
     - Candidate's tech stack
     - Years of experience
     - Desired positions
   - Ensures exactly three questions per session
   - Questions are numbered and formatted consistently

3. **Conversation Flow**:
   - State-based conversation management
   - Context-aware responses
   - Professional tone maintenance

## ⚡ Challenges & Solutions

### Challenge 1: Response Consistency
**Problem**: Inconsistent number of technical questions generated
**Solution**: Implemented strict question counting and retry mechanism

### Challenge 2: Performance Optimization
**Problem**: Slow response times due to API calls
**Solution**: 
- Implemented response caching with TTL
- Added retry mechanism for failed API calls
- Optimized prompt design for faster responses

### Challenge 3: User Experience
**Problem**: Unclear conversation flow and message formatting
**Solution**:
- Removed unnecessary prefixes from messages
- Added clear progress indicators
- Implemented proper error handling
- Added loading spinners for better feedback

### Challenge 4: State Management
**Problem**: Difficulty maintaining conversation context
**Solution**:
- Implemented robust session state management
- Added clear conversation steps
- Improved error recovery mechanisms

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. 