
from interact import load_memory, save_memory

def apply_preferences(df, memory):
    for col, action in memory.items():
        if action == '1':
            df.dropna(subset=[col], inplace=True)
        elif action == '2':
            df[col].fillna(0, inplace=True)
        elif action == '3':
            df[col].fillna(df[col].mean(), inplace=True)
    return df

def reset_memory():
    memory = {}
    save_memory(memory)
    print("Memory has been reset. All preferences are cleared.")
    