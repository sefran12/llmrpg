from langchain.chat_models import ChatOpenAI

class LLMBuilder:
    def __init__(self, model_type, **kwargs):
        self.model_type = model_type
        self.kwargs = kwargs

    def build(self):
        if self.model_type == "gpt-3.5-turbo-16k":
            return ChatOpenAI(**self.kwargs)
        if self.model_type == "gpt-4":
            return ChatOpenAI(**self.kwargs)
        else:
            raise ValueError(f"Unsupported model: {self.model_type}")
        
