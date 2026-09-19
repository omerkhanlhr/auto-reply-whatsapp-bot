import time

import pyautogui
import pyperclip
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
load_dotenv()

GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_KEY")
client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options={"api_version": "v1"},
)


def is_last_message_from_sender(chat_log, sender_name="Burhan"):
    messages = chat_log.strip().split("/2026] ")[-1]
    if sender_name in messages:
        return True
    return False
    
    


# 1.Click on the chrome icon at cordinates
pyautogui.click(897, 1040)
time.sleep(2)

while True:
    # 2. Drag the mouse from (576,146) to (1864,965)
    pyautogui.moveTo(680, 253)

    pyautogui.dragTo(859, 928, duration=1.0, button="left")  # Drag for 1 second
    # 3. Copy the selected text to the clipboard
    pyautogui.hotkey("ctrl", "c")
    pyautogui.click(1873, 914)
    time.sleep(2)

    # 4. Retrive the text from clipboard and store it in a variable

    chat_history = pyperclip.paste()

    # Print the copied text to verify

    print(chat_history)
    if is_last_message_from_sender(chat_history):
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=f"""
                You are a person named Umar who speaks Hindi as well as English.
                You are from Pakistan and you are a coder.

                Analyze the chat history and pretend to be Harry.
                Respond naturally like Umar.Output should be next chat response (text message only)
                Keep the response short, preferably 1-2 lines.

                Chat history:
                {chat_history}
                """,
            config=types.GenerateContentConfig(
                automatic_function_calling=types.AutomaticFunctionCallingConfig(
                    disable=True
                )
            ),
        )

        response_text = response.text

        pyperclip.copy(response_text)

        pyautogui.click(1057, 970)
        pyautogui.hotkey("ctrl", "v")

        # pyautogui.press("enter")

        # print(response_text)
