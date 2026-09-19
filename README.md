# WhatsApp Auto-Reply Chatbot

A desktop automation bot that reads your latest WhatsApp Web conversation, asks Google Gemini to write a natural reply in your voice, and pastes that reply into the message box.

The bot works purely through **screen automation** (mouse, keyboard, and clipboard). It does not use the WhatsApp API, so it works with a normal WhatsApp Web session open in Chrome.

> **Status:** Learning / hobby project. See [Limitations](#limitations) and [Disclaimer](#disclaimer) before using it on real conversations.

---

## How It Works

1. Clicks the Chrome icon on the taskbar to bring WhatsApp Web to the front.
2. Drags the mouse over the chat area to select the visible conversation.
3. Copies the selection with `Ctrl+C` and reads it from the clipboard.
4. Checks whether the **last message was sent by the other person**.
5. If it was, sends the chat history to Gemini and asks for a short, natural reply.
6. Copies the reply to the clipboard, clicks the message box, and pastes it with `Ctrl+V`.
7. Repeats forever.

```text
WhatsApp Web (Chrome)
        |
        |  pyautogui: select + Ctrl+C
        v
   Clipboard  --pyperclip-->  chat_history
                                   |
                     last message from sender?
                                   |
                                  yes
                                   v
                     Gemini (google-genai) -> reply text
                                   |
                        pyperclip.copy(reply)
                                   |
                     pyautogui: click input + Ctrl+V
```

By default the bot **only pastes** the reply. The `Enter` key press is commented out so that you can review each message before sending.

---

## Tech Stack

| Tool | Purpose |
| --- | --- |
| [uv](https://docs.astral.sh/uv/) | Project and dependency management |
| [pyautogui](https://pyautogui.readthedocs.io/) | Mouse and keyboard automation |
| [pyperclip](https://pypi.org/project/pyperclip/) | Clipboard read/write |
| [google-genai](https://pypi.org/project/google-genai/) | Official Google Gemini SDK |

---

## Prerequisites

- **uv** installed ([installation guide](https://docs.astral.sh/uv/getting-started/installation/))
- A **Gemini API key** from [Google AI Studio](https://aistudio.google.com/apikey)
- **Google Chrome** with WhatsApp Web logged in
- A desktop environment with a screen (the bot cannot run headless)

---

## Installation

Clone the repository and install the dependencies:

```bash
git clone <your-repository-url>
cd <your-project-folder>
uv sync
```

`uv sync` creates the virtual environment and installs the exact versions from `uv.lock`.

If you are starting from scratch instead, create the project and add the dependencies:

```bash
uv init
uv add pyautogui pyperclip google-genai
```

---

## Configuration

### 1. API key

**Never hardcode your API key in the source code.** Provide it through an environment variable named `GEMINI_API_KEY`.

Option A: a `.env` file (recommended). Create a file named `.env` in the project root:

```text
GEMINI_API_KEY=your-api-key-here
```

Then run the bot with `uv run --env-file .env python main.py` (see [Usage](#usage)).

Option B: set the variable in your terminal session.

```powershell
# Windows PowerShell
$env:GEMINI_API_KEY = "your-api-key-here"
```

```bash
# macOS / Linux
export GEMINI_API_KEY="your-api-key-here"
```

Make sure `.env` is listed in `.gitignore` so it is never committed.

### 2. Screen coordinates

The bot clicks and drags at **fixed pixel positions**, so you must adjust them to match your screen resolution and browser layout.

| Action | Where in the code | What it targets |
| --- | --- | --- |
| `pyautogui.click(897, 1040)` | Before the loop | Chrome icon on the taskbar |
| `pyautogui.moveTo(680, 253)` | Loop, step 2 | Start of chat selection (top of the chat area) |
| `pyautogui.dragTo(859, 928, ...)` | Loop, step 2 | End of chat selection (bottom of the chat area) |
| `pyautogui.click(1873, 914)` | Loop, step 3 | Click to clear the text selection |
| `pyautogui.click(1057, 970)` | Reply step | WhatsApp message input box |

To find the coordinates for your own screen, run this in a terminal, move your mouse over the target, and read the printed position:

```bash
uv run python -c "import pyautogui, time; time.sleep(5); print(pyautogui.position())"
```

### 3. Sender name and persona

- `sender_name` in `is_last_message_from_sender()` must match the **contact name exactly as it appears in the copied chat text**.
- The prompt inside `generate_content()` defines who the bot pretends to be. Edit it to change the name, languages, tone, and reply length.

---

## Usage

1. Open WhatsApp Web in Chrome and open the chat you want to auto-reply to.
2. Make sure the Chrome icon and chat layout match your configured coordinates.
3. Start the bot:

```bash
# With a .env file
uv run --env-file .env python main.py

# With the variable already set in your terminal
uv run python main.py
```

4. The bot switches to Chrome after a short delay and begins its loop.

### Stopping the bot

- Press `Ctrl+C` in the terminal that is running the script.
- **Fail-safe:** `pyautogui` aborts automatically if you move the mouse to the **top-left corner** of the screen.

### Enabling auto-send

Uncomment this line in the script to send replies automatically:

```python
pyautogui.press("enter")
```

Keep it disabled until you have tested the bot and are comfortable with its replies.

---

## Project Structure

```text
.
├── main.py           # Bot logic
├── pyproject.toml    # Project metadata and dependencies (managed by uv)
├── uv.lock           # Locked dependency versions
├── .python-version   # Python version used by uv
├── .env              # Local secrets (not committed)
├── .gitignore
└── README.md
```

---

## Limitations

This project is intentionally simple. Known limitations:

- **Resolution-dependent.** All click and drag coordinates are hardcoded for one screen setup. A different resolution, zoom level, or window size will break it.
- **Timestamp parsing is year-specific.** `is_last_message_from_sender()` splits the chat text on `"/2026] "`, so it will stop working when the year changes. It also depends on the exact timestamp format WhatsApp Web copies.
- **Name matching is a substring check.** If the sender's name appears inside the message text, the bot may wrongly treat it as a message from that person.
- **No deduplication.** With auto-send disabled, the last message stays unanswered, so the loop may generate and paste a new reply on every iteration.
- **No error handling.** Network failures or API errors from Gemini will stop the script.
- **Single chat only.** The bot works on whichever chat is currently open.

---

## Security & Privacy

- **API key:** keep it in an environment variable or `.env` file, never in source code or Git history. If a key was ever committed or shared, revoke it in Google AI Studio and create a new one.
- **Chat data:** the copied conversation is sent to the Gemini API to generate replies. Do not use the bot on conversations containing sensitive or confidential information, and only use it where the other participants would not object.
- **Cost and quota:** every loop iteration that finds a new message from the sender makes an API request. Monitor your usage.

---

## Disclaimer

This project automates a WhatsApp Web session. Automated messaging may violate WhatsApp's Terms of Service and could result in account restrictions. Use it at your own risk, on your own account, for learning and personal experimentation only.

---

## Possible Improvements

- Move coordinates, sender name, and persona into a configuration file.
- Replace the fixed `/2026] ` split with a regular expression that matches any timestamp.
- Track the last processed message to avoid duplicate replies.
- Add a polling interval and a clean exit condition to the main loop.
- Add logging and specific exception handling around the Gemini call.
- Split the code into functions and a package structure with tests (`pytest`).