# zero shot prompting example
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/"
)

# zero shot prompting : Directly asking the model to perform a task without providing any examples.
SYSTEM_PROMPT = "You are an expert in Maths and only and only ans maths realted questions. That if the query is not related to maths. Just say sorry and do not ans that."
response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT},
        { "role": "user", "content": "Hey, can you Tell me a joke"}
    ]
)

print(response.choices[0].message.content)