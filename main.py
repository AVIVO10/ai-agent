import argparse
import os
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt


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
)

if response.usage is None:
    raise RuntimeError("API response did not include usage metadata")

if args.verbose:
    print("User prompt:", args.user_prompt)
    print("Prompt tokens:", response.usage.prompt_tokens)
    print("Response tokens:", response.usage.completion_tokens)
print(response.choices[0].message.content)
