import os

from google import genai
from google.genai import types

GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_KEY")
client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options={"api_version": "v1"},
)
command = """
"""

response = client.models.generate_content(
    model="gemini-3.6-flash",
    contents=f"""
                     You are a person named harry who speaks hindi as well as english. He is
                     from Pakistan  and is a coder. You analyze chat history and pretend to be Harry
                     and respond Like Harry

         Request:{command}
        """,
    config=types.GenerateContentConfig(
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
    ),
)
print(response.text)
