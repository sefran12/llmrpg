from pydantic import BaseModel
from abc import ABC, abstractmethod
import json

from src.core.runner import Runner
from src.models.models import CharacterState, WorldState
from src.chains.chain import ChainBuilder
from src.base.template import PromptManager
from src.utils.parse_response import extract_json_from_response
from src.chains.chain_context import ContextManager

prompt_manager = PromptManager()

class Form:

    def __init__(self, state_model: type[BaseModel], runner: Runner, llm_name: str, prompt_template: str, context_manager: ContextManager = None):
        self.state_model = state_model
        self.runner = runner
        
        # Initialize chain using ChainBuilder
        chain_builder = ChainBuilder()
        chain_builder.with_prompt_template(prompt_template)
        chain_builder.with_llm(llm_name)
        chain_builder.with_context_manager(context_manager)
        self.chain = chain_builder.build()

        # Set context for the chain
        self.chain.update_context(form_fields=self.get_form_fields())

        # Create current state
        self.current_state = self.state_model()
    
    def get_form_fields(self) -> str:
        return ", ".join(field for field in self.state_model.__annotations__)
    
    def step(self, user_input: str, external_context: dict = None) -> str:
        response = self.chain.step(user_input, external_context)
        
        # Extract potential JSON from the response
        updated_data = extract_json_from_response(response)
        if updated_data:
            self.current_state = self.state_model(**updated_data)

        return response

    def update_context(self, new_context):
        self.chain.update_context(**new_context)

    def is_complete(self) -> bool:
        return all([getattr(self.current_state, field) for field in self.state_model.__annotations__])

    def run_until_complete(self, max_steps=20):
        step = 0
        while not self.is_complete() and (step < max_steps):
            step += 1
            user_input = self.runner.get_input()
            output = self.step(user_input)
            self.runner.send_output(output)
    
    def get_current_state(self):
        return self.current_state.dict()


class CharacterForm(Form):

    def __init__(self, runner: Runner, language = "en"):
        character_template = prompt_manager.get_prompt(language, "character_form")
        super().__init__(CharacterState, runner, "gpt-3.5-turbo", character_template)

class WorldForm(Form):

    def __init__(self, runner: Runner, language = "en"):
        world_template = prompt_manager.get_prompt(language, "world_form")
        super().__init__(WorldState, runner, "gpt-3.5-turbo", world_template)
