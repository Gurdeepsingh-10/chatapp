from AppOpener  import close , open as appopen
from webbrowser import open as webopen
from pywhatkit import search , playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup 
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os


env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

classes = ["zCubwf","hgKElc","LTKOO sY7ric","Z0LcW","gsrt vk_bk FzvWSb YwPhnf","pclqee","tw-Data-text tw-text-small tw-ta-IZ66rdc","OSuR6d LTKOO","vlzY6d","webanswers-webanswers_table__webanswers-table","dDoNo ikb48b gsrt","sXLaOe","LWkfKe","VQF4g","qv3Wpe","kno-rdesc","SPZz6b"]

useragent = "Morzilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"


client = Groq(api_key = "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")

professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",
    "I'm at your service for any additional questions or support you amy need-don't hesitate to ask."

]

messages = []


SystemChatBot = [{"role":"system","content":f"Hello, I am {os.environ['Username']} , You're a content writter. You have to write content like letter , mail, cv , resume ,etc"}]



def GoogleSearch(Topic):
    search(Topic)
    return True

def Content(Topic):

    def OpenNotepad(File):
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor,File])
    

    def ContentWriterAI(prompt):
        messages.append({"role":"user","content":f"{prompt}"})
        completion = client.chat.completions.create(
            model ='llama-3.3-70b-versatile',
            messages = SystemChatBot+messages,
            max_tokens = 2048,
            temperature = 0.7,
            top_p = 1,
            stream = True,
            stop = None
        )

        Answer = ""


        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>","")
        messages.append({"role":"assitant","content":Answer})
        return Answer
    
    Topic: str = Topic.replace("Content ","")
    ContentByAI  = ContentWriterAI(Topic)


    with open(rf"Data/{Topic.lower().replace(' ','')}.txt","w",encoding="utf-8") as file:
        file.write(ContentByAI)
        file.close()

    OpenNotepad(rf"Data/{Topic.lower().replace(' ','')}.txt")
    return True

    
def YoutubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?searchquery={Topic}"
    webbrowser.open(Url4Search)

def PlayYoutube(query):
    playonyt(query)
    return True

def OpenApp(app,sess = requests.session()):

    try:
        appopen(app,match_closest = True , output = True , throw_error = True)
        return True
    except : 
        def extract_links(html):
            if html is None:
                return []
            soup = BeautifulSoup(html,'html.parser')
            links = soup.find_all('a',{'jsname' : 'UWckNb'})
            return [link.get('href') for link in links]
        

        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers =  {"User-Agent":useragent}
            response = sess.get(url,headers)

            if response.status_code == 200:
                return response.text
            else:
                print("Failed to retrive search results.")

            return None
    
        html = search_google(app)

        if html:
            link = extract_links(html)[0]
            webopen(link)

        return True
    
def CloseApp(app):
    if 'chrome' in app:
        pass
    else:
        try:
            close(app,match_closest = True,output = True,throw_error = True)
            return True
        except:
            return False


def System(command):

    def mute():
        keyboard.press_and_release("volume mute")

    def unmute():
        keyboard.press_and_release("volume mute")
    
    def volume_up():
        keyboard.press_and_release("volume up")
    
    def volume_down():
        keyboard.press_and_release("volume down")


    if command in 'mute':
        
        
        mute()

    elif command in 'unmute':
            mute()

    elif command in 'volume up':
        volume_up()

    elif command in 'volume down':
        volume_down()


    return True


async def TranslateandExecute(commands:list[str]):
    funcs = []

    for command in commands:
        if command.startswith('open '):
            if 'open it' in command:
                pass
            if 'open file' == command:
                pass
            else:
                fun = asyncio.to_thread(OpenApp,command.removeprefix("open "))
                funcs.append(fun)

        elif command.startswith("general "):
            pass
        
        elif command.startswith("realtime "):
            pass
        
        elif command.startswith("close "):
            
            fun = asyncio.to_thread(OpenApp,command.removeprefix("close " ))
            funcs.append(fun)
            
        elif command.startswith("play "):
            fun = asyncio.to_thread(OpenApp,command.removeprefix("play " ))
            funcs.append(fun)


        elif command.startswith("content "):
            fun = asyncio.to_thread(OpenApp,command.removeprefix("content " ))
            funcs.append(fun)

        elif command.startswith("google search "):
            fun = asyncio.to_thread(OpenApp,command.removeprefix("google search " ))
            funcs.append(fun)
        
        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(OpenApp,command.removeprefix("youtube search " ))
            funcs.append(fun)
        
        elif command.startswith("system "):
            fun = asyncio.to_thread(OpenApp,command.removeprefix("system " ))
            funcs.append(fun)
            
        else:
            print(f"No function found for the command {command}")
    
    results = await asyncio.gather(*funcs)

    for results in results:
        if isinstance(results, str):
            yield results
        else:
            yield results


async def Automation(commands : list[str]):
    async for result in TranslateandExecute(commands):
        pass

    return True


System("unmute")