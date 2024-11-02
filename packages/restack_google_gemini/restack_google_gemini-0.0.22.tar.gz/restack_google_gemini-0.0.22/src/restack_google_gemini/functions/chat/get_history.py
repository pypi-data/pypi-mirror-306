from pydantic import BaseModel
import google.generativeai as genai

class GeminiGetHistoryInput(BaseModel):
    chat: genai.ChatSession
    model_config = {
        "arbitrary_types_allowed": True
    }    

def gemini_get_history(input: GeminiGetHistoryInput):
    return input.chat.history