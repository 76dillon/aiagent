import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from prompts import system_prompt
from call_function import available_functions
from call_function import call_function
from config import MAX_NUM_LOOPS


def main():
    load_dotenv()
    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = generate_content(client, messages, verbose)
    print(response)
    #response = generate_content(client, messages, verbose)
    #for candidate in response.candidates:
    #    messages.append(candidate.content)
    
    #if response.function_calls:
    #    for function_call_part in response.function_calls:



def generate_content(client, messages, verbose, iterations=0):

    while iterations < MAX_NUM_LOOPS:
        iterations += 1
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            ),
        )
        for candidate in response.candidates:
            messages.append(candidate.content)
        if verbose:
            print("Prompt tokens:", response.usage_metadata.prompt_token_count)
            print("Response tokens:", response.usage_metadata.candidates_token_count)

        if not response.function_calls:
            return response.text

        for function_call_part in response.function_calls:
            function_call_result = call_function(function_call_part, verbose)
            messages.append(function_call_result)
            if (not function_call_result.parts[0].function_response.response) or (not function_call_result.parts):
                raise Exception("Empty function call result")
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
    return "Max iterations reached"

if __name__ == "__main__":
    main()