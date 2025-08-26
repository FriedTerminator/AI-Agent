import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Ensure functions is a package: ai_agent/ai_agent/functions/__init__.py
from functions.get_files_info import schema_get_files_info, build_schema_get_files_info

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not set")

if len(sys.argv) == 1:
    raise Exception("No prompt given")

user_prompt = sys.argv[1]
verbose = len(sys.argv) == 3 and sys.argv[2] == "--verbose"

client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# If eager schema failed at import, build it now
if schema_get_files_info is None:
    schema_get_files_info = build_schema_get_files_info()

available_functions = types.Tool(function_declarations=[schema_get_files_info])

config = types.GenerateContentConfig(
    tools=[available_functions],
    system_instruction=system_prompt,
)

messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=config,
)

# Extract function calls, if any
function_calls = []
if getattr(response, "candidates", None):
    for cand in response.candidates:
        parts = getattr(cand.content, "parts", []) if getattr(cand, "content", None) else []
        for part in parts:
            fc = getattr(part, "function_call", None)
            if fc:
                try:
                    args_dict = dict(fc.args)  # ensure Python dict repr with single quotes
                except Exception:
                    args_dict = fc.args
                function_calls.append((fc.name, args_dict))

# ALWAYS print the function call if present (tests look for this)
if function_calls:
    for name, args in function_calls:
        print(f"Calling function: {name}({args})")
else:
    print(response.text or "")

if verbose and getattr(response, "usage_metadata", None):
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
