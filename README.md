# Federated RPG: Automated Multi-Agent Role-Playing Game System
## Overview

Federated RPG is a software architecture designed to facilitate automated storytelling and gameplay in role-playing games (RPGs). It employs a federated system of intelligent agents that work in coordination to provide a rich and dynamic RPG experience.

## Features

### Generators

    Generate challenges based on a given state of the game.
    Support for multiple types of challenges (physical, intellectual, emotional).
    Implement a tiered difficulty system.

### Parsers

    Extract and identify game elements from textual input.
    Output includes characters, items, spells, and relationships between characters.

### Summarizers

    Create concise summaries of game states or story arcs.
    Highlight crucial decision points and past events.

### Threaders

    Generate complex actions in the narrative based on parsed/generated input.
    Support for multiple genres (fantasy, sci-fi, etc.)

### Updaters

    Update previous states of the game world and characters.
    Track and update emotional states of characters for enhanced depth.

## Complex Classes
### Federation

    Directed Acyclic Graph (DAG) of dependencies for agent coordination.
    Features feedback loops for state consistency.

### Forms

    Collect required information through stateful form-filling agents.
    Support for adaptive questioning based on prior responses.

### Gamemaster

    Overarching agent that synthesizes federated outputs into a coherent narrative.
    Features include narrative pacing and style selection.

## Documentation

See the full documentation for a detailed breakdown of components and their functionalities.
Installation and Usage

    Clone the repository: git clone https://github.com/sefran12/FederatedRPG.git
    Install required packages: pip install -r requirements.txt
    Run the main application: python main.py

## Contributing

Contributions are welcome. See CONTRIBUTING.md for guidelines.