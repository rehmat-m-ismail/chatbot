
import requests
from ddgs import DDGS

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "llama3.2:1b"


def search_web(query):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))

        if not results:
            return "Web par koi result nahi mila."

        search_text = ""

        for result in results:
            search_text += (
                f"Title: {result.get('title', '')}\n"
                f"Description: {result.get('body', '')}\n"
                f"Link: {result.get('href', '')}\n\n"
            )

        return search_text1

    except Exception as e:
        return f"Web search mein masla hua: {e}"


def get_answer(user_question, chat_history=None):
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful student assistant. "
                "Answer clearly and simply. "
                "Reply in the same language as the user. "
                "Use web results carefully and never invent facts."
            )
        }
    ]

    if chat_history:
        messages.extend(chat_history)

    # User ke sawal ke liye web search
    search_results = search_web(user_question)

    messages.append({
        "role": "user",
        "content": (
            f"User question: {user_question}\n\n"
            f"Actual web search results:\n{search_results}\n\n"
            "Summarize only information supported by these results. "
            "Do not invent titles, facts, dates, or sources. "
            "Include the actual links from the results. "
            "If results are insufficient, say so clearly."
        )
    })

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": messages,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]

    except requests.exceptions.ConnectionError:
        return "Ollama nahi chal raha. Pehle Ollama app open karein."

    except requests.exceptions.Timeout:
        return "AI ko jawab dene mein zyada waqt lag raha hai. Dobara try karein."

    except requests.exceptions.RequestException:
        return "AI se connection mein masla hai. Dobara try karein."
