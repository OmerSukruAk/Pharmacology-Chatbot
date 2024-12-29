from pydantic import BaseModel

class api_input_message_format(BaseModel):
    message: str

class chat_history_format(BaseModel):
    messages: list[dict]

class api_response_format(BaseModel):
    response: str
    functions_called: list[str]
    chat_history: chat_history_format