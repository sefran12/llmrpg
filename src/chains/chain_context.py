class ContextManager:
    def __init__(self, initial_context=None):
        self._context = initial_context or {}

    def get_context(self):
        return self._context

    def set_context(self, new_context: dict):
        self._context.update(new_context)
