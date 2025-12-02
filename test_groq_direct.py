import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

print("Groq key loaded:", bool(api_key))
print("Using model:", model)

client = Groq(api_key=api_key)

resp = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Generate 3 unit test ideas for a function add(a, b)."},
    ],
    temperature=0.2,
)

print("Groq response:")
print(resp.choices[0].message.content)
