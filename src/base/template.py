import os
import random

class TemplateManager:
    def __init__(self, base_directory: str):
        self.base_directory = base_directory
        self.templates = self._load_templates()

    def _load_templates(self) -> dict:
        """This method should be overridden by subclasses."""
        return {}


class PromptManager(TemplateManager):
    def __init__(self, base_directory: str = os.path.join("templates", "prompts")):
        super().__init__(base_directory)

    def _load_templates(self) -> dict:
        prompts = {}
        for root, _, files in os.walk(self.base_directory):
            for file in files:
                category = os.path.basename(root)
                language, _ = os.path.splitext(file)
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    content = f.read()
                if category not in prompts:
                    prompts[category] = {}
                prompts[category][language] = content
        return prompts

    def get_prompt(self, category: str, language: str) -> str:
        return self.templates.get(language, "").get(category, {})


class TropeManager(TemplateManager):
    def __init__(self, base_directory: str = os.path.join("templates", "tropes")):
        super().__init__(base_directory)

    def _load_templates(self) -> dict:
        tropes = {}
        for root, _, files in os.walk(self.base_directory):
            for file in files:
                category = os.path.basename(root)
                language, _ = os.path.splitext(file)
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    content = f.readlines()  # Read lines since each trope is on a new line
                if category not in tropes:
                    tropes[category] = {}
                tropes[category][language] = [line.strip() for line in content]
        return tropes

    def get_tropes(self, category: str, language: str) -> list:
        return self.templates.get(category, {}).get(language, [])

    def get_trope_by_position(self, category: str, language: str, position: int) -> str:
        tropes_list = self.get_tropes(category, language)
        if 0 <= position < len(tropes_list):
            return tropes_list[position]
        return None

    def get_trope_randomly(self, category: str, language: str) -> str:
        tropes_list = self.get_tropes(category, language)
        return random.choice(tropes_list) if tropes_list else None