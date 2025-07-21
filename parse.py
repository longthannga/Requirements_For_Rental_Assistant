from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

template = (
    
)

model = OllamaLLM(model="gemma3:4b", streaming=True, temperature=0.2)
