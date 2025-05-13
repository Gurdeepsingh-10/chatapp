from googlesearch import search 
from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")

Username = env_vars.get("Username") 
Assistantname = env_vars.get("Assistantname")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize Groq client
client = Groq(api_key="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")

# System prompt
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

# Load or create chat log
try:
    with open(r"Data/ChatLog.json", "r") as f:
        messages = load(f)
except:
    messages = []
    with open(r"Data/ChatLog.json", "w") as f:
        dump(messages, f)

# Function to get Google search result
def GoogleSearch(query):
    results = list(search(query, advanced=True, num_results=5))
    Answer = f"The search results for '{query}' are:\n[start]\n"
    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"
    Answer += "[end]"
    return Answer

# Clean up the output
def AnswerModifier(answer):
    lines = answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    return "\n".join(non_empty_lines)

# Get real-time date and time
def Information():
    current_date_time = datetime.datetime.now()
    return (
        f"Use this Real-Time Information if needed:\n"
        f"Day: {current_date_time.strftime('%A')}\n"
        f"Date: {current_date_time.strftime('%d')}\n"
        f"Month: {current_date_time.strftime('%B')}\n"
        f"Year: {current_date_time.strftime('%Y')}\n"
        f"Time: {current_date_time.strftime('%H')} hours, "
        f"{current_date_time.strftime('%M')} minutes, "
        f"{current_date_time.strftime('%S')} seconds.\n"
    )

# Main chatbot function
def RealtimeSearchEngine(prompt):
    global messages

    with open("Data/ChatLog.json", 'r') as f:
        messages = load(f)

    messages.append({"role": "user", "content": prompt})

    # Add system messages
    chat = [
        {"role": "system", "content": System},
        {"role": "system", "content": GoogleSearch(prompt)},
        {"role": "system", "content": Information()},
        *messages
    ]

    completion = client.chat.completions.create(
        model='llama3-70b-8192',
        messages=chat,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True
    )

    Answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    Answer = Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})

    with open("Data/ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

    return AnswerModifier(Answer)

# CLI Interface
if __name__ == "__main__":
    while True:
        prompt = input("Enter your question: ")
        print(RealtimeSearchEngine(prompt))
