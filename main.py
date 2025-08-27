import sys
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

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

    generate_content(client, messages, verbose)



def generate_content(client, messages, verbose):
    MAX_ITERATIONS = 20
    try:
        for _ in range(MAX_ITERATIONS):
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )

            for cand in (response.candidates or []):
                if getattr(cand, "content", None):
                    messages.append(cand.content)
            
            if verbose and getattr(response, "usage_metadata", None):
                print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                print("Response tokens:", response.usage_metadata.candidates_token_count)

            if getattr(response, "text", None):
                print(response.text)
                break

            for function_call_part in response.function_calls:
                tool_resp = call_function(function_call_part, verbose=verbose)
                messages.append(tool_resp)

                try:
                    payload = tool_resp.parts[0].function_response.response
                except Exception as e:
                    raise RuntimeError("Tool call did not return function_response") from e

                if verbose:
                    print(f"-> {payload}")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
