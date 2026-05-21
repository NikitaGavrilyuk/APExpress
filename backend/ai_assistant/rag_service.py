"""
RAG (Retrieval-Augmented Generation) service using OpenAI API.
Generates expert auto-parts recommendations in Ukrainian.
"""

import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_rag_response(
    query: str, category: str, context_products: str
) -> str:
    """
    Generate an AI response using GPT-4o-mini with product context.

    Args:
        query: The user's original question.
        category: The classified category (e.g. "Engine").
        context_products: Serialized product data from the database.

    Returns:
        The AI-generated recommendation text in Ukrainian.
    """
    prompt = (
        f"User query: '{query}'. "
        f"Identified Category: '{category}'. "
        f"Found products in DB: {context_products}. "
        f"Recommend ONLY products that match the user's query. "
        f"Explain why using technical terms. "
        f"Answer in Ukrainian."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert auto parts consultant. "
                        "Always answer in Ukrainian. "
                        "NEVER use markdown formatting (no **, ##, `, or other markup). "
                        "Use plain text only. "
                        "ONLY discuss products that DIRECTLY match what the user asked for. "
                        "If the user asks about a specific part (e.g. gearbox), do NOT mention "
                        "other parts from the same category (e.g. clutch, axle). "
                        "Focus strictly on what was asked."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "rate" in error_msg.lower():
            return (
                "⏳ На жаль, перевищено ліміт запитів до AI. "
                "Будь ласка, зачекайте хвилину та спробуйте ще раз."
            )
        return f"Помилка при генерації відповіді: {error_msg}"
