import openai
import json
from openai import OpenAI

openai.api_key = "YOUR-API-KEY"
client = OpenAI(api_key=openai.api_key)

def generate_chatgpt_response(system_prompt: str, user_prompt: str, max_tokens=60, temperature=0.8) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return response.choices[0].message.content.strip()

def generate_npc_daily_plan_with_schedule_and_time(npc):
    prompt = f"""
NPC Name: {npc.name}
Background: {' '.join(npc.background)}
Memory: {' '.join([m['event'] for m in npc.memory])}

Please generate a detailed daily plan for this NPC on a train.  
The plan should be split into three time slots with specific times included (like "08:00", "13:00", "19:00"):

- After breakfast (around 08:00 - 10:00)
- After lunch (around 13:00 - 15:00)
- After dinner (around 19:00 - 21:00)

For each time slot, provide one main activity description that fits the NPC's personality, motivation, and behavior.  
Format the response exactly as a JSON list of objects, where each object has:

- "time": the starting time string (e.g., "08:30")
- "activity": the activity description string

Example:
[
  {{"time": "08:30", "activity": "Ethan sharpens his fighting skills in the empty train car."}},
  {{"time": "13:00", "activity": "Ethan explores Carriage 9 to find clues related to Marcus."}},
  {{"time": "19:30", "activity": "Ethan reflects on his past while writing in his journal."}}
]
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    content = response.choices[0].message.content.strip()

    import json
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # 简单解析fallback
        plan = []
        for line in content.split('\n'):
            if line.strip().startswith('{') and line.strip().endswith('}'):
                try:
                    plan.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue
        return plan


def generate_npc_action_reaction(npc, action):
    all_events = [m['event'] for m in npc.memory]
    all_reactions = [m['reaction'] for m in npc.memory]

    prompt = f"""
You are simulating the behavior of a fictional character involved in a mysterious train murder.

NPC Name: {npc.name}
Background Summary: {' '.join(npc.background)}

Current Day Action: {action}

Recent Events:
{" | ".join(all_events)}

Recent Reactions:
{" | ".join(all_reactions)}

Context:
- On Day 1, Marcus was found dead in his cabin. The train stopped suddenly right after.
- All characters had hidden motives or plans involving Marcus.
- Nobody knows who exactly killed him, and everyone is trying to hide, investigate, or understand what happened.
- NPCs only know their own background, memories, and what they've seen or felt. They should never mention knowledge they don’t logically have.
- Avoid repeating murder or overly dramatic actions unless it's grounded in memory.
- Focus on subtle, realistic, psychological and investigative behavior.

Your task:
1. Describe what the NPC does based on their background, today's action, and recent memories.
2. Describe their inner thoughts, feelings, or suspicions in reaction to that event.

Format strictly:
Event: ...
Reaction: ...
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response.choices[0].message.content.strip()
    lines = content.split("\n")
    event = ""
    reaction = ""
    for line in lines:
        if line.lower().startswith("event:"):
            event = line.split(":", 1)[1].strip()
        elif line.lower().startswith("reaction:"):
            reaction = line.split(":", 1)[1].strip()
    return event, reaction


def generate_npc_exploration_reaction(npc, clue, owner=False):
    prompt = f"""
NPC: {npc.name}
Background: {' '.join(npc.background)}
Recent Memory: {' '.join([m['event'] for m in npc.memory[-3:]])}

Clue Discovered:
Name: {clue['name']}
Description: {clue['description']}
Location: {clue['location']}
"""

    if owner and clue.get("owner_memory"):
        prompt += f"""
This clue is directly related to the NPC. Their past memory: {clue['owner_memory']}
Generate a reaction as the NPC reconnects this clue with their past.
"""
    else:
        prompt += "Generate a reaction to this clue from the NPC's perspective.\n"

    prompt += "Respond with only the reaction in a single sentence."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

def simplify_memory_with_gpt(event: str, reaction: str) -> (str, str):
    prompt = f"""
You are a story assistant. Please simplify the following event and reaction into one natural and concise sentence each, while preserving important details:

Event: {event}
Reaction: {reaction}

Return the result in the format:
Event: <simplified event>
Reaction: <simplified reaction>
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6
    )

    content = response.choices[0].message.content
    simplified_event = event
    simplified_reaction = reaction

    try:
        for line in content.splitlines():
            if line.startswith("Event:"):
                simplified_event = line.replace("Event:", "").strip()
            elif line.startswith("Reaction:"):
                simplified_reaction = line.replace("Reaction:", "").strip()
    except Exception as e:
        print(f"[!] GPT parsing failed, using original text: {e}")

    return simplified_event, simplified_reaction

def generate_dialogue_between(npc1, npc2):
    memory1 = '\n'.join([f"- {m['event']}" for m in npc1.memory[-5:]])
    memory2 = '\n'.join([f"- {m['event']}" for m in npc2.memory[-5:]])

    prompt = f"""
NPC1: {npc1.name}
Background: {' '.join(npc1.background)}

NPC2: {npc2.name}
Background: {' '.join(npc2.background)}

Recent Memory of {npc1.name}:
{memory1}

Recent Memory of {npc2.name}:
{memory2}

They meet in the train corridor and start a conversation based on what they’ve recently experienced.
Write a natural and tense short dialogue (3~5 turns each), showing suspicion, alliance or tension.

Format:
{npc1.name}: ...
{npc2.name}: ...
...
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return f"[Dialogue between {npc1.name} and {npc2.name}]\n" + response.choices[0].message.content.strip()


def generate_npc_choose_location(npc, options: list[str]):
    all_events = [m['event'] for m in npc.memory]
    all_reactions = [m['reaction'] for m in npc.memory]

    prompt = f"""
You are {npc.name}, a suspect on a train where a murder just happened.

- You must hide your own secrets while investigating others.
- You only know your own memories and background.
- Choose ONE place or object to explore next from the options below.
- Be subtle, strategic, and stay in character.

Recent memories:
{" | ".join(all_events)}

Recent thoughts:
{" | ".join(all_reactions)}

Options:
{', '.join(options)}

Format EXACTLY:
Choice: <your choice>
Reasoning: <brief why you choose this>
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=150
    )

    content = response.choices[0].message.content.strip()
    choice = ""
    reasoning = ""
    for line in content.split("\n"):
        if line.lower().startswith("choice:"):
            choice = line.split(":", 1)[1].strip()
        elif line.lower().startswith("reasoning:"):
            reasoning = line.split(":", 1)[1].strip()

    # 防止输出不在选项里的值
    if choice not in options:
        choice = options[0]

    return choice, reasoning