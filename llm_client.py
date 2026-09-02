from typing import Dict, List
from openai import OpenAI

def generate_response(openai_key: str, user_message: str, context: str, 
                     conversation_history: List[Dict], model: str = "gpt-3.5-turbo") -> str:
    """Generate response using OpenAI with context"""

    # Define system prompt positioning model as NASA expert
    system_prompt = """You are an expert NASA mission analyst with deep knowledge of space exploration programs.
Your role is to provide accurate, helpful information about NASA missions based on the provided context.

Guidelines:
- Always cite the source documents when referencing specific information
- If the context doesn't contain relevant information, acknowledge this limitation
- Provide detailed, technical responses when appropriate
- Maintain accuracy and avoid speculation beyond the provided context
- Use clear, accessible language while maintaining technical accuracy"""

    # Build messages list starting with system prompt
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add previous conversation history for context
    for history_item in conversation_history:
        messages.append({
            "role": history_item.get("role", "user"),
            "content": history_item.get("content", "")
        })
    
    # Add context and current user message if context exists
    if context.strip():
        context_message = f"""Here is relevant context from NASA mission documents to help answer the question:

{context}

Based on the above context, please answer the following question:"""
        messages.append({"role": "user", "content": context_message})
    
    # Add current user message
    messages.append({"role": "user", "content": user_message})
    
    # Create OpenAI Client with provided API key
    client = OpenAI(api_key=openai_key)
    
    # Send request to OpenAI
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.7,
        max_tokens=1000
    )
    
    # Return response content
    return response.choices[0].message.content