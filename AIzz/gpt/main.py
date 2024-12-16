import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai

app = FastAPI()
load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

class TextRequest(BaseModel):
    text: str

@app.post("/get_emojis")
async def get_emojis(request: TextRequest):
    user_text = request.text

    messages = [
        {"role": "system", "content": "You are a helpful assistant that suggests emojis."},
        {"role": "user", "content": f"Suggest 3 emojis matching the text's mood, emotion, and theme. Reply with emojis only.'{user_text}'"}
    ]
    try:
        respense = openai.chat.completions.create(
            model = "gpt-4o-mini",
            messages = messages,
            max_tokens = 50,
            temperature = 0,
        )
        emojis = respense.choices[0].message.content.strip()
        return {"emojis": emojis}
    except Exception as e:
        return {"error": str(e)}