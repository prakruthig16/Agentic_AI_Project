
import ollama

MODEL = "llama3.2:3b"

SYSTEM_PROMPT = """
You are an AI Teaching Assistant.

Teach the following subjects:
- Python Programming
- Artificial Intelligence
- Machine Learning
- Deep Learning
- IoT
- Agentic AI

Instructions:
1. Explain concepts in simple language.
2. Provide real-world examples.
3. Explain Python code step by step.
4. Use headings and bullet points when appropriate.
5. Give practical examples suitable for college students.
6. Answer follow-up questions using conversation context.
"""


def generate_response(question, history=None):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    if history:
        messages.extend(history)

    messages.append({
        "role": "user",
        "content": question
    })

    response = ollama.chat(
        model=MODEL,
        messages=messages
    )

    return response.message.content
