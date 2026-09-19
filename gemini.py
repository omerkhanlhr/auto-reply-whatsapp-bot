import os

from google import genai
from google.genai import types

GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_KEY")
client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options={"api_version": "v1"},
)
command = """
[2:49 PM, 8/19/2026] Omer Khan: Ok
[2:49 PM, 8/19/2026] +92 317 7081525: @Omer Khan @~Fairy  
Ok
[2:50 PM, 8/19/2026] Omer Khan: Photo
Ye university ki slip ha?
[2:50 PM, 8/19/2026] +92 310 5786021: G
[2:51 PM, 8/19/2026] Omer Khan: Got it
[7:08 PM, 9/8/2026] Omer Khan: Assalam-o-Alaikum 
Kisi k portal pr marks upload howa hn fyp ka
@~Fairy @~Fairy
[7:09 PM, 9/8/2026] +92 317 7081525: Assalam-o-Alaikum 
Kisi k portal pr marks upload howa hn fyp ka
@~Fairy @~Fairy
Ni
[7:12 PM, 9/8/2026] Omer Khan: @~Hts Axon
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
