import os
import google.generativeai as genai

from utils.env_loader import *

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use a model that is available to your API key
model = genai.GenerativeModel("gemini-3.5-flash")

def is_career_related(user_message, chat_history=""):

    text = (
        user_message + " " + chat_history
    ).lower()

    career_keywords = [

        "career",
        "job",
        "jobs",
        "hired",
        "employment",
        "profession",

        "resume",
        "cv",

        "interview",

        "skill",
        "skills",

        "coding",
        "programming",
        "programmer",
        "developer",

        "college",
        "study",
        "course",
        "courses",
        "learning",

        "internship",
        "internships",

        "placement",

        "salary",
        "package",
        "lpa",

        "python",
        "java",
        "javascript",
        "react",
        "flask",
        "api",
        "sql",

        "ai",
        "machine learning",
        "deep learning",
        "data science",

        "software engineer",
        "frontend",
        "backend",
        "full stack",
        "data analyst",
        "data scientist"
    ]

    for keyword in career_keywords:

        if keyword in text:
            return True

    return False


def ask_gemini(user_message, chat_history=""):

    greetings = [
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]

    if user_message.lower().strip() in greetings:

        return """
    Hello! 👋

    I'm CareerPilot AI.

    I can help with:

    - Career guidance
    - Resume review
    - Interview preparation
    - Learning roadmaps
    - Internship guidance
    - Job preparation

    How can I help you today?
    """

    if not is_career_related(
        user_message,
        chat_history
    ):

        return """
    I specialize in career guidance, resume assistance,
    interview preparation, learning roadmaps and
    professional growth.

    Please ask a career-related question and I'll be happy to help.
    """

    system_prompt = f"""
You are CareerPilot AI, a professional AI Career Assistant.

Your purpose is to help students and professionals with:

- Career guidance
- Resume review
- Resume generation
- Interview preparation
- Learning roadmaps
- Skill gap analysis
- Internship guidance
- Job preparation
- Higher studies
- Salary guidance

Instructions:

You are a STRICT Career Assistant.

You ONLY answer questions related to:

- Career Guidance
- Resume Review
- Resume Building
- Interview Preparation
- Learning Roadmaps
- Skill Development
- Internships
- Job Search
- Higher Studies
- Salary Guidance
- Artificial Intelligence Careers
- Software Development Careers
- Data Science Careers

Rules:

1. Never answer questions outside the career domain.

2. If the user asks anything unrelated to careers, jobs, learning, resumes, interviews, education, skills or professional growth, politely refuse.

3. For off-topic questions reply exactly in this style:

"I specialize in career guidance, resume assistance, interview preparation, learning roadmaps and professional growth.

Please ask a career-related question and I'll be happy to help."

4. Do not provide recipes.

5. Do not provide movie recommendations.

6. Do not answer general entertainment questions.

7. Do not answer random trivia.

8. Do not engage in unrelated casual conversation.

9. Use headings and bullet points whenever useful.

10. Respond professionally.

11. Respond in clean Markdown.

Previous Conversation:

{chat_history}

Current User Question:

{user_message}
"""

    try:
        response = model.generate_content(system_prompt)

        if response.text:
            return response.text

        return "Sorry, I couldn't generate a response."

    except Exception as e:

        print("Gemini Error:", e)

        if "429" in str(e):

            return """
    ⚠️ **Rate limit reached**

    The AI service is temporarily busy because too many requests were sent.

    Please wait about **1 minute** and try again.
    """

        return """
    Sorry, something went wrong while generating a response.

    Please try again in a moment.
"""