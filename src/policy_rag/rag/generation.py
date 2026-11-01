'''Documentation String'''
import time
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from policy_rag.rag.config import LLM_MODEL,LLM_MAX_TOKENS

load_dotenv()

SYSTEM_PROMPT = (
    "You are PolicyCopilot, an assistant that answers employee questions "
    "about company policies. Answer only from the policies provided in the "
    "user's message. If the policies don't contain the answer, say so "
    "plainly instead of guessing. Mention the policy name you are relying "
    "on, and include any limits, deadlines, or approval requirements."
)

_client = None

def _get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    return _client

def generate_response(augmented_prompt: str) -> str :
    '''Replace with real LLM call to generate response'''
    print("\nSECTION 6: RESPONSE GENERATION")
    print("=" * 50)
    print("⏳ Processing with LLM...")

    time.sleep(1)

    result = _get_client().models.generate_content(
        model = LLM_MODEL,
        contents = augmented_prompt,
        config = types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            max_output_tokens=LLM_MAX_TOKENS
        )
    )

    response = result.text or "Waiting For Response..."

    # response = """
    #     Based on the company policies provided, here's the answer to your question:

    #     The relevant policies contain information about various company guidelines and procedures.
    #     The retrieved context provides specific details that can help answer your question.

    #     Key points from the policies:
    #     - Multiple policy sources were consulted
    #     - Information is current and accurate
    #     - Specific requirements and limitations are included

    #     Please refer to the specific policy documents for complete details and any recent updates.
    # """

    print(f"\nGenerated response length: {len(response)} characters")
    print("Response includes: Policy references, key points, limitations")

    return response