import random
import os
import json
from memory import add_memory_entry, MemoryEntry, save_npc_memory
from world_structure import WorldNode
from generate_chatgpt import (
    generate_npc_daily_plan_with_schedule_and_time,
    generate_npc_action_reaction,
    generate_npc_exploration_reaction,
    generate_dialogue_between,
    simplify_memory_with_gpt,
    generate_npc_choose_location)


def generate_random_times(n, start_hour=6, end_hour=22):
    times = set()
    while len(times) < n:
        hour = random.randint(start_hour, end_hour)
        minute = random.randint(0, 59)
        times.add(f"{hour:02d}:{minute:02d}")
    return sorted(times)


def initialize_npc_memory(npc, npc_data_folder="npc_data", memory_folder="memory_data"):

    mem_path = os.path.join(memory_folder, f"{npc.name}.json")
    if os.path.exists(mem_path):
        print(f"[init] Memory file exists for {npc.name}, skipping initialization.")
        return

    npc_file = os.path.join(npc_data_folder, f"{npc.name}.json")
    if not os.path.exists(npc_file):
        print(f"[init] NPC data file not found for {npc.name} at {npc_file}")
        return

    with open(npc_file, "r", encoding="utf-8") as f:
        npc_data = json.load(f)

    initial_memory = npc_data.get("memory", [])

    memory_list = []
    for i, mem in enumerate(initial_memory):
        entry = MemoryEntry(
            entry_id=mem.get("id", i + 1),
            day=mem.get("day", 0),
            time=mem.get("time", "00:00"),
            event=mem.get("event", ""),
            reaction=mem.get("reaction", "")
        )
        memory_list.append(entry)

    save_npc_memory(npc.name, memory_list, folder=memory_folder)
    print(f"[init] Initialized memory for {npc.name} with {len(memory_list)} entries.")

def simulate_day(day: int, npcs: list, world) -> list[dict]:
    logs = []
    all_clues = world.get_all_clues()
    # 先记录一天开始的事件
    for npc in npcs:
        logs.append({
            "npc": npc.name,
            "time": "start",
            "event": "Start day",
            "reaction": ""
        })

        if len(npcs) >= 2 and random.random() < 0.2:  # 50% 概率触发
            npc1, npc2 = random.sample(npcs, 2)
            dialogue_time = generate_random_times(1)[0]  # 生成随机对话时间
            dialogue = generate_dialogue_between(npc1, npc2)
            logs.append({
                "npc": f"{npc1.name} & {npc2.name}",
                "time": dialogue_time,
                "event": "Dialogue",
                "reaction": dialogue
            })

            lines = dialogue.splitlines()
            for line in lines:
                if not line.strip():
                    continue
                if line.startswith(f"{npc1.name}:"):
                    content = line[len(npc1.name) + 1:].strip()
                    # 简化对话文本
                    event_simplified, reaction_simplified = simplify_memory_with_gpt(f"Spoke to {npc2.name}", content)
                    add_memory_entry(npc1.name, day, "dialogue", event_simplified, reaction_simplified)
                elif line.startswith(f"{npc2.name}:"):
                    content = line[len(npc2.name) + 1:].strip()
                    event_simplified, reaction_simplified = simplify_memory_with_gpt(f"Spoke to {npc1.name}", content)
                    add_memory_entry(npc2.name, day, "dialogue", event_simplified, reaction_simplified)

    for npc in npcs:
        num_actions = random.randint(2, 4)  # 每人每天活动数
        time_slots = generate_random_times(num_actions)

        plan = generate_npc_daily_plan_with_schedule_and_time(npc)
        for action, action_time in zip(plan, time_slots):
            # 行动本体
            event, reaction = generate_npc_action_reaction(npc, action)
            logs.append({
                "npc": npc.name,
                "time": action_time,
                "event": event,
                "reaction": reaction
            })

            npc.memory.append({
                "id": len(npc.memory) + 1,
                "day": day,
                "time": action_time,
                "event": event,
                "reaction": reaction
            })

            add_memory_entry(
                name=npc.name,
                day=day,
                time=action_time,
                raw_event=event,
                raw_reaction=reaction
            )


            # Exploration Ver 1.1
            carriages = list(world.children.keys())
            chosen_carriage, reasoning_carriage = generate_npc_choose_location(npc, carriages)
            print(f"[DEBUG] {npc.name} chose carriage: {chosen_carriage} Reasoning: {reasoning_carriage}")

            rooms = list(world.children[chosen_carriage].children.keys())
            chosen_room, reasoning_room = generate_npc_choose_location(npc, rooms)
            print(f"[DEBUG] {npc.name} chose room: {chosen_room} Reasoning: {reasoning_room}")

            explorables = list(world.children[chosen_carriage].children[chosen_room].children.keys())
            chosen_explorable, reasoning_explorable = generate_npc_choose_location(npc, explorables)
            print(f"[DEBUG] {npc.name} chose explorables: {chosen_explorable} Reasoning: {reasoning_explorable}")

            selected_node = world.find_node_by_path([chosen_carriage, chosen_room, chosen_explorable])
            clue = selected_node.clue
            explore_time = f"{action_time} + exploration"
            if clue:
                is_owner = clue.get("owner") == npc.name
                reaction = generate_npc_exploration_reaction(npc, clue, owner=is_owner)

                logs.append({
                    "npc": npc.name,
                    "time": explore_time,
                    "event": f"Explored {' -> '.join(['Train', chosen_carriage, chosen_room, chosen_explorable])} and found clue: {clue['name']}",
                    "reaction": reaction,
                    "location_path": [chosen_carriage, chosen_room, chosen_explorable],
                    "reasoning": {
                        "carriage": reasoning_carriage,
                        "room": reasoning_room,
                        "explorable": reasoning_explorable
                    }
                })

                npc.memory.append({
                    "id": len(npc.memory) + 1,
                    "day": day,
                    "time": explore_time,
                    "event": f"Explored {' -> '.join(['Train', chosen_carriage, chosen_room, chosen_explorable])} and found clue: {clue['name']}",
                    "reaction": reaction
                })

                add_memory_entry(
                    name=npc.name,
                    day=day,
                    time=explore_time,
                    raw_event=f"Explored {chosen_explorable} and found clue: {clue['name']}",
                    raw_reaction=reaction
                )

            else:
            #TODO
                print("!!!!!!!!!!!!!!!!")
                print(selected_node.name)
                print(selected_node.description)

            # 探索部分
            """
            if all_clues:
                clue = random.choice(all_clues)
                is_owner = clue.get("owner") == npc.name
                reaction = generate_npc_exploration_reaction(npc, clue, owner=is_owner)

                explore_time = f"{action_time} + exploration"
                logs.append({
                    "npc": npc.name,
                    "time": explore_time,
                    "event": f"Explored {clue.get('location', 'unknown location')} and found clue: {clue['name']}",
                    "reaction": reaction
                })

                npc.memory.append({
                    "id": len(npc.memory) + 1,
                    "day": day,
                    "time": explore_time,
                    "event": f"Explored {clue.get('location', 'unknown location')} and found clue: {clue['name']}",
                    "reaction": reaction
                })

                add_memory_entry(
                    name=npc.name,
                    day=day,
                    time=explore_time,
                    raw_event="default event",
                    raw_reaction=reaction
                )
            """
    return logs


