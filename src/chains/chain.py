import json
import logging
from langchain import LLMChain
from langchain.schema import HumanMessage, AIMessage
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI

from src.base.template import PromptManager
from src.chains.chain_context import ContextManager

class InjectedChain:
    """Wrapper over LLMChain"""

    def __init__(self, chain: LLMChain, context_manager: ContextManager = None):
        self.chain = chain
        self.context_manager = context_manager or ContextManager()

    def update_context(self, **kwargs):
        self.context_manager.set_context(kwargs)

    def inject_prompt(self, injected_prompt):
        logging.debug(f"Injecting prompt: {injected_prompt}")
        self.chain.prompt.template = injected_prompt

    def retrieve_memory(self, as_string=False):
        try:
            memory = self.memory.chat_memory.messages
        except:
            logging.warning(f"Failed to retrieve memory from chain {self.name}")
            return []

        if as_string:
            formatted_memory = []
            for msg in memory:
                if isinstance(msg, HumanMessage):
                    formatted_memory.append(f"User: {msg.content}")
                elif isinstance(msg, AIMessage):
                    formatted_memory.append(f"AI: {msg.content}")
            return "\n".join(formatted_memory)

        return memory
        
    def step(self, user_input: str = None, external_context: dict = None) -> str:
        if external_context is None:
            external_context = {}

        combined_context = {**self.context_manager.get_context(), **external_context}
        if not user_input:
            return self.chain.run(**combined_context)
        return self.chain.run(input=user_input, **combined_context)

    def __getattr__(self, attr):
        # Delegate attribute access to the wrapped Chain instance
        return getattr(self.chain, attr)
    

class ChainBuilder:
    def __init__(self):
        self.prompt = None
        self.llm = None
        self.memory = None  # We can include memory configuration as well.
        self.context_manager = None  # Initialize context_manager as None to begin with.
    
    def with_prompt_template(self, prompt_template: str):
        self.prompt = PromptTemplate.from_template(prompt_template)
        return self
    
    def with_prompt_category(self, prompt_manager: PromptManager, category: str, language: str = "en"):
        prompt_text = prompt_manager.get_prompt(category, language)
        self.prompt = PromptTemplate.from_template(prompt_text)
        return self
    
    def with_llm(self, model_name: str, temperature: float = 0.0):
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        return self
    
    def with_memory(self, memory_instance):
        self.memory = memory_instance
        return self

    # Add a method to set the context_manager
    def with_context_manager(self, context_manager: ContextManager):
        self.context_manager = context_manager
        return self

    def build(self) -> InjectedChain:
        if not self.prompt or not self.llm:
            raise ValueError("Both prompt and llm must be specified before building the chain.")
        
        if not self.memory:
            self.memory = ConversationBufferMemory(input_key="input", memory_key="chat_history")
        
        if not self.context_manager:
            # Create a default ContextManager if none was provided.
            self.context_manager = ContextManager()
        
        llm_chain = LLMChain(llm=self.llm, prompt=self.prompt, memory=self.memory)
        return InjectedChain(llm_chain, context_manager=self.context_manager)
    
    def from_json(self, json_string: str):
        config = json.loads(json_string)
        self.with_prompt_template(config["prompt_template"])
        self.with_llm(config["llm_model"], config.get("temperature", 0.0))
        # Add more attributes as required
        return self.build()
