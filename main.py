import argparse
import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if not(api_key):
    raise RuntimeError("API KEY NOT FOUND, VERY HELPFUL MESSAGE")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
# Now we can access `args.user_prompt`

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]


response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    tools=available_functions,
)

if response.usage is None:
    raise RuntimeError("API response did not include usage metadata")

if args.verbose:
    print("User prompt:", args.user_prompt)
    print("Prompt tokens:", response.usage.prompt_tokens)
    print("Response tokens:", response.usage.completion_tokens)

message = response.choices[0].message

if message.tool_calls:
    for tool_call in message.tool_calls:
        function_args = json.loads(tool_call.function.arguments or "{}")
        result_message = call_function(tool_call=tool_call)
    
if args.verbose:
    print(f"-> {result_message['content']}")

print(message.content)
