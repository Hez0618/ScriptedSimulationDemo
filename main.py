import os
import json
from npc import NPC
from world_structure import initialize_world, get_train_room_structure
from simulator import simulate_day, initialize_npc_memory

def load_all_npcs(npc_folder="npc_data"):
    npcs = []
    for filename in os.listdir(npc_folder):
        if filename.endswith(".json"):
            with open(os.path.join(npc_folder, filename), "r", encoding="utf-8") as f:
                data = json.load(f)
            npc = NPC(
                name=data.get("name", ""),
                age=data.get("age", 0),
                background=data.get("background", []),
                memory=data.get("memory", [])
            )
            npcs.append(npc)
    return npcs


def print_pretty_logs(day, logs):
    print(f"\n===== 🗓️ Day {day} Logs =====\n")
    for log in logs:
        npc = log["npc"]
        time = log["time"]
        event = log["event"]
        reaction = log["reaction"]

        print(f"🕒 {time} | 👤 {npc}")
        print(f"📝 Event: {event}")
        if reaction.strip():
            print(f"💭 Reaction: {reaction}")
        print("-" * 60)


if __name__ == "__main__":
    # 1. Load world
    world = initialize_world("clue_data/clues.json")
    print(get_train_room_structure(world))
    # 2. Load NPCs’s memory and initialize
    npcs = load_all_npcs()

    for npc in npcs:
       initialize_npc_memory(npc)


        # 3. Simulate
    total_days = 3  # 你想模拟的总天数

    for day in range(2, total_days + 1):
        logs = simulate_day(day, npcs, world)
        print_pretty_logs(day, logs)