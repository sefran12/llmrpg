from typing import Callable

from src.chains.chain import InjectedChain
from src.chains.chain_context import ChainContext

class GameRoom:

    def __init__(self, initial_chain: InjectedChain):
        self.current_chain = initial_chain
        self.chain_context = ChainContext()
        self.transitions = {}

    def step(self, user_input: str) -> str:
        # Step the current chain with the user input
        response = self.current_chain.step(user_input=user_input)
        
        # Check if we need to transition to a new chain
        self.check_transitions()
        
        return response

    def set_transition(self, source_chain: type, condition: Callable, target_chain: type):
        """
        Define a transition from `source_chain` to `target_chain` when `condition` is True.
        """
        self.transitions[source_chain] = (condition, target_chain)

    def check_transitions(self):
        """
        Check if we should transition from the current chain to a new one.
        """
        condition, target_chain = self.transitions.get(type(self.current_chain), (None, None))
        if condition and condition(self.current_chain):
            self.switch_chain(target_chain)

    def switch_chain(self, new_chain: type):
        """
        Switch to a new chain, initializing it in the process.
        """
        self.current_chain = new_chain()

    # Additional utility methods to manage the internal context can be added as necessary.
