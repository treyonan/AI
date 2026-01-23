from pydantic import BaseModel

class GenerationRequest(BaseModel):
    prompt: str
    max_length: int = 100
    temperature: float = 1.0


class GenerationResponse(BaseModel):
    generated_text: str