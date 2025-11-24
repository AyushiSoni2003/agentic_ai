from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import requests

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

image_path = "https://images.pexels.com/photos/34594456/pexels-photo-34594456.jpeg?_gl=1*1hq1dgg*_ga*MTgyNzQ4Mzc3MC4xNzU3MTczNTA5*_ga_8JE65Q40S6*czE3NjM5NzY2NjEkbzckZzEkdDE3NjM5NzY3MDAkajIxJGwwJGgw"
image_bytes = requests.get(image_path).content
image = types.Part.from_bytes(
  data=image_bytes, mime_type="image/jpeg"
)

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=["What is this image?Explain in short", image],
)

print(response.text)