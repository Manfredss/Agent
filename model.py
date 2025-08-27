import json, os, requests
from langchain_openai import ChatOpenAI


class GPT4o:
    def __init__(self):
        super().__init__()
        self.api_key = 'YOUR-OPENAI-API-KEY'
        self.model = 'gpt-4o'
    def getLLM(self) -> ChatOpenAI:
        os.environ["OPENAI_API_KEY"] = self.api_key
        client = ChatOpenAI(model=self.model)
        return client


class QWen:
    def __init__(self):
        super(self, QWen).__init__()

    def getLLM(self):
        pass


class DeepSeek_R1:
    def __init__(self):
        super().__init__()
        self.url = 'https://api.deepseek.com/v1'
        self.api_key = 'YOUR-DEEPSEEK-API-KEY'
        self.model = 'deepseek-chat'

    def getLLM(self) -> ChatOpenAI:
        os.environ["OPENAI_API_KEY"] = self.api_key
        client = ChatOpenAI(model=self.model,
                            base_url=self.url,
                            api_key=self.api_key)
        return client
