import os
import json
from clue import Clue

def main():
    os.makedirs("clue_data", exist_ok=True)

    clues = [
        Clue(
            clue_id=1,
            name="Family Photo",
            description="A photo tucked in a wallet, showing a mother, an older brother(Ethan), and a younger sister.",
            location=["Train", "Carriage 10", "Room 2", "Wallet"],
            owner="Ethan",
            owner_memory="This photo reminds me of what I lost — my mother and sister."
        ),

        Clue(
            clue_id=2,
            name="Wanted Poster",
            description="A newspaper clipping showing a wanted notice for Marcus, 25, slim build, wearing a dark hoodie. Dated: November 13, 2007.",
            location=["Train", "Carriage 10", "Room 2", "Journal"],
            owner="Ethan",
            owner_memory="I've kept this for years. It's my only lead on Marcus — burned into my memory."
        ),

        Clue(
            clue_id=3,
            name="Charm Pendant",
            description="A small charm with a hidden note: 'Son... I'm watching over you. — Jan 19, 2008'.",
            location=["Train", "Carriage 10", "Room 2", "Ethan's Coat"],
            owner="Ethan",
            owner_memory="My mother gave me this charm when I was born. I kept it close — her last words still echo."
        )
        # 可以继续添加更多Clue实例
    ]

    clues_data = [clue.__dict__ for clue in clues]

    with open("clue_data/clues.json", "w", encoding="utf-8") as f:
        json.dump(clues_data, f, indent=4, ensure_ascii=False)

    print("All clues data saved to clue_data/clues.json")

if __name__ == "__main__":
    main()

