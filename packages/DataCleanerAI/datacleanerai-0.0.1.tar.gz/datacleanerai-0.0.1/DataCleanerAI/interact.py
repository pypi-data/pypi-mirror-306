
import json
import os

MEMORY_FILE = "DataCleanerAI/memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f)

def prompt_user(column, issue, memory):
    if column in memory:
        return memory[column]

    print(f"Issue detected in column '{column}': {issue}")
    response = input("Choose an option: (1) Remove, (2) Fill with 0, (3) Fill with mean, (4) Skip: ")
    memory[column] = response
    save_memory(memory)
    return response
    