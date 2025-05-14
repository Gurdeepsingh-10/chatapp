import pygame
import random
import asyncio
import edge_tts
import os
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice", "en-US-AriaNeural")  # fallback voice

# Text-to-Audio async function using plain text
async def TextToAudioFile(text) -> None:
    file_path = r"Data/speech.mp3"

    # Remove existing file if already exists
    if os.path.exists(file_path):
        os.remove(file_path)

    communicate = edge_tts.Communicate(text, AssistantVoice)
    await communicate.save(file_path)

# Synchronous wrapper for TTS
def TTS(text, func=lambda r=None: True):
    while True:
        try:
            asyncio.run(TextToAudioFile(text))
            pygame.mixer.init()
            pygame.mixer.music.load("Data/speech.mp3")
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                if func() is False:
                    break
                pygame.time.Clock().tick(10)  # correct instantiation

            return True

        except Exception as e:
            print(f"Error in TTS: {e}")

        finally:
            try:
                func(False)
                if pygame.mixer.get_init():
                    pygame.mixer.music.stop()
                    pygame.mixer.quit()
            except Exception as e:
                print(f"Error in finally block: {e}")

# Handles long text responses
def TextToSpeech(text, func=lambda r=None: True):
    sentences = str(text).split(".")
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer."
    ]

    if len(sentences) > 4 and len(text) >= 250:
        TTS(". ".join(sentences[:2]) + ". " + random.choice(responses), func)
    else:
        TTS(text, func)

# Main CLI usage
if __name__ == "__main__":
    os.makedirs("Data", exist_ok=True)  # Make sure folder exists
    while True:
        TextToSpeech(input("Enter the text: "))
