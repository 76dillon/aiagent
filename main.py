import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


#Add arguments
verbose = "--verbose" in sys.argv
args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

if not args:
    print("AI Code Assistant")
    print('\nUsage: python main.py "your prompt here" [--verbose]')
    print('Example: python main.py "How do I build a calculator app?"')
    sys.exit(1)

user_prompt = sys.argv[1]


#Enable Gemini Client
api_key = os.environ.get("GEMINI_API_KEY") #Load API key from .env
client = genai.Client(api_key=api_key)
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)
print(response.text)
prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count

if verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")