import os
from dotenv import load_dotenv

# load environmental variables from .env file
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google import genai
from google.genai.errors import APIError

app = FastAPI()

# Configuration of template (index.html) and static files (js and css)
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images",StaticFiles(directory="images"), name="images")

# Definition of structure of user-input (json which contains 'message:' and message has to be a string)
class ChatRequest(BaseModel):
    message: str

# system prompt: Nietzsches personality
NIETZSCHE_PROMPT = (
    "Du bist Friedrich Nietzsche, der deutsche Philosoph. Antworte in einem "
    "leidenschaftlichen, aphoristischen Stil. Vermeide moderne Floskeln. "
    "Deine Antworten sollen zum Denken anregen und provozieren. "
    "Antworte IMMER in der Sprache der letzten Benutzerfrage. Behalte deinen "
    "philosophischen Stil in jeder Sprache bei. Wenn die Frage auf Deutsch ist, "
    "antworte auf Deutsch. Wenn die Frage auf Englisch ist, antworte auf Englisch."
)


# loading html-template
# async: function can give controll back to system while e.g. waiting for gemini response
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# 3. route for chat bot api endpoint (here lives Nietzsche haha)
@app.post("/api/nietzsche-chat")
async def handle_chat(request: ChatRequest):
    try:
        # The genai SDK reads key if it is set as environmental variable
        client = genai.Client()

        # configuration: tell bot that he should behave like Nietzsche
        config = genai.types.GenerateContentConfig(
            system_instruction=NIETZSCHE_PROMPT
        )

        # call gemini
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=request.message,
            config=config,
        )

        nietzsche_text = response.text
        
        # remove all * signs
        nietzsche_text = nietzsche_text.replace('*', '')

        # return gemini's answer
        return {"response": nietzsche_text}

    except APIError as e:
        # catch api error
        print(f"Gemini API Fehler: {e}")
        return {"response": None, "error": "API error: The key is invalid or you have reached your limits"}, 500
    # catch general error
    except Exception as e:
        return {"response": None, "error": f"Unexpected Error in backend: {str(e)}"}, 500