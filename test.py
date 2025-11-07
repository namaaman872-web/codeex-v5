import requests
import pyttsx3
import subprocess
import time

# 🛠️ Configuration
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "phi3:mini"

# 🎙️ Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)  # Change index for female voice

def speak(text):
    engine.say(text)
    engine.runAndWait()

def start_ollama():
    try:
        # Launch Ollama model in background
        subprocess.Popen(["ollama", "run", MODEL_NAME], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"🚀 Starting codeex with model: {MODEL_NAME}")
        speak("Starting codeex server with Phi-3 Mini.")
        time.sleep(5)  # Give it a few seconds to initialize
    except Exception as e:
        print(f"⚠️ Failed to start codeex: {e}")
        speak("Failed to start codeex.")

def chat_with_ollama():
    start_ollama()
    print("🧠✨ Welcome to the CODEEX Chat! Type 'exit' to quit.\n")
    messages = []

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            farewell = "Goodbye, brave explorer!"
            print(f"👋 {farewell}")
            speak(farewell)
            break

        messages.append({"role": "user", "content": user_input})

        try:
            response = requests.post(
                OLLAMA_URL,
                json={"model": MODEL_NAME, "messages": messages, "stream": False}
            )
            response.raise_for_status()
            reply = response.json().get("message", {}).get("content", "")
            print(f"🧠 CODEEX: {reply}")
            speak(reply)
            messages.append({"role": "assistant", "content": reply})

        except requests.exceptions.ConnectionError:
            error_msg = "Could not connect to codeex. Is it running on port 11434?"
            print(f"🚫 {error_msg}")
            speak(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error: {e}"
            print(f"⚠️ {error_msg}")
            speak("Something went wrong. Please check your setup.")

if __name__ == "__main__":
    chat_with_ollama()
