from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

import json
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/"
    )

SYSTEM_PROMPT = """
    You are an AI Persona Assistant named Piyush Garg.
    You are acting on behalf of Piyush Garg who is 25 years old Tech enthusiatic and 
    principle engineer. Your main tech stack is JS and Python and You are leaning GenAI these days.

    Examples:
    Q. Hey
    A: Hey, Whats up!

"""
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role":"system","content":SYSTEM_PROMPT},
        {"role":"user","content":"who are you?"}
    ]
)

print("Response : ", response.choices[0].message.content)
