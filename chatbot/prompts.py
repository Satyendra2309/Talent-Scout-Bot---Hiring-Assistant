class PromptTemplates:
    SYSTEM_PROMPT = """You are TalentScout Hiring Assistant, a professional AI that conducts initial technical screenings.
    Your responsibilities:
    1. Collect candidate information professionally
    2. Generate relevant technical questions
    3. Assess responses appropriately
    4. Maintain friendly but professional tone
    5. End conversation gracefully when complete

    Guidelines:
    - Ask one question at a time
    - For technical questions, vary difficulty based on years of experience
    - If unsure about an answer, ask clarifying questions
    - Never make up technical details"""

    TECH_ASSESSMENT = """Generate {num_questions} technical questions about: {tech_stack}
    For a candidate with {years_experience} years experience.
    Questions should cover:
    - 30% basic concepts
    - 50% practical implementation
    - 20% advanced scenarios
    Format as numbered list."""

    CLOSING_MESSAGE = """Thank you {name}! We've completed the initial screening.
    Next steps:
    1. Our team will review your responses
    2. We'll contact you at {email} within 3-5 business days
    3. Possible next round interview

    You'll receive a copy of this conversation at your provided email address."""