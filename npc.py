from generate_chatgpt import generate_chatgpt_response
import json

class NPC:
    def __init__(self, name, age, background, memory, dialogue_score = 0, dialogue_ready = False):
        self.name = name
        self.age = age
        self.background = background
        self.memory= memory or []
        self.dialogue_score = dialogue_score
        self.dialogue_ready = dialogue_ready

    def add_memory(self, memory):
        if isinstance(memory, Memory):
            self.memory.append(memory)

    def get_all_memory(self):
        return self.memory

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "background_story": self.background_story,
            "memories": [memory.to_dict() for memory in self.memory]
        }

    @classmethod
    def from_dict(cls, data):
        npc = cls(name=data["name"], age=data["age"], background_story=data["background_story"])
        for memory_data in data["memories"]:
            npc.add_memory(Memory.from_dict(memory_data))
        return npc

    @classmethod
    def load_from_file(cls, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls(
            name=data['name'],
            age=data.get('age', 0),
            background=data.get('background', []),
            memory=data.get('memory', [])
        )

def generate_npc_reaction(npc: NPC, current_event: str) -> str:
    # 拼接背景故事
    background_text = "\n".join(f"- {line}" for line in npc.background)

    # 拼接记忆事件
    memories_text = "\n".join(
        f"{m.day} day, {m.time}: {m.event}" for m in npc.memories
    ) if npc.memories else "No previous memories."

    system_prompt = (
        f"You are {npc.name}, a character in a murder mystery on a train.\n"
        f"Background:\n{background_text}\n\n"
        f"Past memories:\n{memories_text}\n\n"
        "Now a new event happened:\n"
        f"{current_event}\n\n"
        "Please respond with your honest thoughts or feelings about this event, in a style consistent with your background and memories."
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
        ],
        max_tokens=100,
        temperature=0.7,
    )

    return response['choices'][0]['message']['content'].strip()
