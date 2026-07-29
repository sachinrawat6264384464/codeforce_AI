import json
from typing import Dict, Any
from openai import OpenAI
from app.core.config import settings

# Initialize Groq client using OpenAI SDK
client = OpenAI(
    api_key=settings.GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def generate_microservice_via_llm(prompt: str, db_context: str) -> Dict[str, Any]:
    system_message = """You are ContextForge AI Code Generator, an expert Python and FastAPI developer.
You are tasked with generating a production-ready FastAPI microservice based on a user's prompt and their provided DataHub database context.

Output your response STRICTLY as a JSON object with the following exact schema:
{
  "entity_name": "the primary singular entity name in lowercase (e.g. 'patient' or 'tenant')",
  "downstream_impacts": ["list", "of", "two", "related", "entities"],
  "reasoning": "A brief 1-sentence explanation of what you generated and how it relates to the database context",
  "files_map": {
    "app/main.py": "Python code here...",
    "app/models/{entity_name}_model.py": "Python code here using SQLAlchemy...",
    "app/api/{entity_name}_router.py": "Python code here using FastAPI...",
    "app/services/{entity_name}_service.py": "Python code here...",
    "alembic/versions/001_add_{entity_name}.py": "Python code here...",
    "tests/test_{entity_name}.py": "Python code here...",
    "README.md": "markdown content here detailing the setup and context..."
  }
}

CRITICAL RULES:
1. Replace `{entity_name}` in the JSON keys with the actual singular entity name you choose (e.g. `app/models/tenant_model.py`).
2. Ensure the code directly uses tables and columns mentioned in the DataHub database context if applicable.
3. You output MUST be a valid JSON object.
   CRITICAL RULE: You MUST use SINGLE QUOTES ('') for all strings in your generated code. DO NOT use double quotes ("") anywhere inside the code content, because it will break the JSON parser.
   Do not include markdown code blocks around the JSON."""

    user_message = f"User Prompt: {prompt}\n\nDatabase Context: {db_context}"

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
            max_tokens=4000
        )
        
        content = response.choices[0].message.content
        llm_output = json.loads(content)
        
        return {
            "status": "success",
            "data": llm_output
        }
    except Exception as e:
        print(f"LLM Generation Error: {e}")
        return {
            "status": "error",
            "error": str(e)
        }
