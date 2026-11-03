import httpx

from app.intelligence.knowledge_base import search_knowledge_base


# Ollama configuration
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "qwen2.5:3b"


async def generate_answer(question: str):

    if not question or not question.strip():
        raise ValueError("Customer question cannot be empty.")

    # STEP 1: Retrieve relevant business information
    documents = search_knowledge_base(
        query=question,
        top_k=3
    )

    # STEP 2: Handle missing knowledge
    if not documents:
        return {
            "success": True,
            "question": question,
            "answer": (
                "I could not find this information in the "
                "business knowledge base. Please contact "
                "customer support for further assistance."
            ),
            "sources": []
        }

    # STEP 3: Prepare retrieved context
    context_parts = []

    for document in documents:
        context_parts.append(
            f"Source: {document['source']}\n"
            f"Page: {document['page']}\n"
            f"Business Information: {document['text']}"
        )

    context = "\n\n".join(context_parts)

    # STEP 4: System prompt
    system_prompt = """
You are VaaniSetu, a professional multilingual
customer support assistant for Indian small businesses.

YOUR RESPONSIBILITY:
Understand the customer's problem and provide a useful,
accurate and polite customer support response.

STRICT RULES:

1. Use ONLY the supplied business knowledge.
2. Never invent business policies or information.
3. Never invent order status, tracking numbers,
   delivery dates or payment confirmation.
4. Never repeat the customer's question as your answer.
5. Understand the customer's intent before answering.
6. Give a direct answer to the actual question.
7. Keep the response natural, helpful and concise.
8. Do not generate unnecessary explanations.
9. If information is missing, clearly say it is unavailable.
10. Suggest contacting customer support when necessary.

LANGUAGE RULES:

1. Identify the language of the customer's question.
2. Respond in exactly the same language.
3. Support Telugu, Hindi and English.
4. Use natural, conversational Telugu when the customer
   speaks Telugu.
5. Do not translate the customer's question and return
   it as the answer.

ACCURACY RULE:

If the customer asks about live order tracking but the
business context does not contain live tracking details,
explain that live tracking information is unavailable.

Do not pretend to access an order management system.
"""

    # STEP 5: User prompt
    user_prompt = f"""
BUSINESS KNOWLEDGE:

{context}

CUSTOMER MESSAGE:

{question}

YOUR TASK:

Understand the customer's actual problem.

Provide a helpful customer support response based
on the business knowledge above.

Important:
- Do not repeat the customer's message.
- Do not make up missing information.
- Respond in the customer's language.
- Keep the answer clear and conversational.
- If the requested information is unavailable,
  politely explain that.
"""

    # STEP 6: Prepare Ollama request
    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        "stream": False,
        "keep_alive": "10m",
        "options": {
            "temperature": 0.1,
            "num_predict": 180
        }
    }

    # STEP 7: Generate answer
    async with httpx.AsyncClient(timeout=300.0) as client:

        response = await client.post(
            OLLAMA_URL,
            json=payload
        )

        response.raise_for_status()

        result = response.json()

    answer = (
        result.get("message", {})
        .get("content", "")
        .strip()
    )

    if not answer:
        raise ValueError(
            "The AI model returned an empty answer."
        )

    # STEP 8: Prepare source references
    sources = []

    for document in documents:
        sources.append({
            "source": document["source"],
            "page": document["page"],
            "distance": document["distance"]
        })

    # STEP 9: Return final result
    return {
        "success": True,
        "question": question,
        "answer": answer,
        "model": OLLAMA_MODEL,
        "sources": sources
    }