import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

conversation = []  # this list acts as a memory to the chatbot

def movie_recommendation_chat(user_message, mood_context=""):
    """This function acts as a Movie Recommendation System Chatbot."""

    if not user_message or not user_message.strip():
        return "Please tell me what kind of movies you enjoy, and I’ll recommend one."

    # Add mood/context to the request so the model can personalize the answer
    context_text = user_message.strip()
    if mood_context and mood_context.strip():
        context_text = (
            f"User mood/context: {mood_context.strip()}\n\n"
            f"Movie request: {user_message.strip()}"
        )

    # Step 1: Append the user's message to the conversation history/List
    conversation.append({"role": "user", "parts": [{"text": context_text}]})

    # Force Gemini 3.1 Flash Lite via environment variable
    model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

    # Step 2: Send the conversation history to the LLM for generating a response
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        response = client.models.generate_content(
            model=model_name,
            contents=conversation,
            config={
                "system_instruction": (
                    "You are a witty movie recommendation assistant. "
                    "Always consider the user's mood/context before recommending movies. "
                    "Recommend movies that match the tone, genre, vibe, and priorities the user mentions. "
                    "Your responses should be friendly, entertaining, and concise. "
                    "Include 3 to 5 suggestions when possible. "
                    "For each movie suggestion, you MUST present it in this exact, tight Markdown format without leaving blank lines between the details:\n\n"
                    "### X. [Movie Title] ([Year])\n"
                    "* **Genre:** [Genre]\n"
                    "* **Rating:** [Rating]\n"
                    "* **Starring:** [Cast]\n"
                    "* **Plot:** [One-line summary]\n"
                    "* **Why it fits:** [Reason]\n\n"
                    "CRITICAL FORMATTING & ENGAGEMENT RULES:\n"
                    "1. Do not add extra empty lines or double line breaks (\\n\\n) between the bullet points. Keep the block perfectly compact.\n"
                    "2. Always end your response with a catchy, witty conclusion sentence followed by an engaging, open-ended question that naturally compels the user to reply and keep the conversation going. For example, ask if they want a wild-card alternative, a deeper dive into a specific actor, or if they are ready to pop the popcorn."
                ),
                "temperature": 0.8
            }
        )
        reply = response.text

    except Exception as e:
        print(f"Error occurred: {e}")
        return "Sorry, I encountered an error while processing your request."

    # Step 3: Append the LLM's response to the conversation history
    conversation.append({"role": "assistant", "parts": [{"text": reply}]})

    return reply

# Backward-compatible alias for the older typo:
movie_recommedation_chat = movie_recommendation_chat

def reset_conversation():
    """Resets the conversation history."""
    conversation.clear()