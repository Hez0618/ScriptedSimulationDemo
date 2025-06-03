import json
import os

os.makedirs("npc_data", exist_ok=True)

npc_profiles = [
    # NPC No.1 Ethan
    {
        "name": "Ethan",
        "age": 20,
        "background": [
            "I was born into a wealthy family in H city and lived in a luxurious villa on Taiping Mountain.",
            "My father passed away when I was young, leaving me to take care of my mother and younger sister, Annie.",
            "In 2007, my sister Annie was kidnapped and killed after the ransom was paid. My mother fell into depression and committed suicide in 2008.",
            "I was sent to an orphanage and became rebellious, eventually joining underground boxing at 15.",
            "By 19, I became the undefeated champion in H city's underground fight scene.",
            "In December 2016, I received a tip that the man I was looking for, Marcus, was involved in illegal activities on the Siberian railway."
        ],
        "memory": [
            {
                "id": 1,
                "day": 1,
                "time": "22:00",
                "event": "The train departs. I sit in my cabin (Car 10, Room 2), waiting for the attendant to check rooms.",
                "reaction": "I'm planning to steal her passenger log after she passes."
            },
            {
                "id": 2,
                "day": 1,
                "time": "22:50",
                "event": "The attendant reaches my car. She looks familiar. I quietly follow her to see where she goes.",
                "reaction": "Is she connected to Angel’s case?"
            },
            {
                "id": 3,
                "day": 1,
                "time": "23:15",
                "event": "She leaves the attendant's room in Car 9. I sneak in and grab the passenger log.",
                "reaction": "No one saw me. I need to find Marcus."
            },
            {
                "id": 4,
                "day": 1,
                "time": "23:30",
                "event": "After some searching, I find Marcus’s cabin and take a photo of his info. I ditch the log in Car 10.",
                "reaction": "It’s time. I can’t let him get away."
            },
            {
                "id": 5,
                "day": 1,
                "time": "00:05",
                "event": "With my knife ready, I sneak into Marcus’s room and stab him in the chest three times while he sleeps.",
                "reaction": "One for Angel, one for Mom, and one for myself."
            },
            {
                "id": 6,
                "day": 1,
                "time": "00:08",
                "event": "I go to the restroom and wash the blood from the knife.",
                "reaction": "Stay calm. No one saw me."
            },
            {
                "id": 7,
                "day": 1,
                "time": "00:10",
                "event": "I return to my cabin and hide the knife.",
                "reaction": "It’s over. I just need to act normal now."
            },
            {
                "id": 8,
                "day": 1,
                "time": "00:15",
                "event": "Suddenly, a loud crash—then the train comes to a halt.",
                "reaction": "What happened? Did someone find the body already?"
            }
        ]
    },
    # NPC No.2 Jax
    {
        "name": "Jax",
        "age": 27,
        "background": [
            "I grew up in a small village near Tieling.",
            "I dropped out of high school and became a street thug.",
            "I'm 27 now. Making money is my dream—but not dirty money.",
            "Six months ago, Marcus came to our village to buy rare herbs.",
            "I became his local guide and served him well.",
            "Two months ago, he invited me to work with him officially.",
            "I learned he’s using the railway to smuggle shady stuff.",
            "I hesitated, but his money was tempting.",
            "A week ago, he gave me two train tickets to Moscow.",
            "He refused to tell me what we’re transporting.",
            "I asked around—he’s hiding diamonds.",
            "There’s also a dangerous man on board—Uncle Li.",
            "I brought a disguise, tools, and my village’s sharpest sickle.",
            "I plan to kidnap Marcus and take the diamonds for myself."
    ],
        "memory": [
            {
                "entry_id": 1,
                "day": 1,
                "time": "22:00",
                "event": "I boarded the train with Marcus. He still didn't mention anything about the diamonds.",
                "reaction": "He's too cautious. He stayed in car 7, I stayed in car 9."
            },
            {
                "entry_id": 2,
                "day": 1,
                "time": "22:15",
                "event": "I left my room to check Marcus’s room and see if it was easy to access.",
                "reaction": "I needed to scout the area before acting."
            },
            {
                "entry_id": 3,
                "day": 1,
                "time": "22:18",
                "event": "Outside Marcus’s room, I saw a woman arguing with him.",
                "reaction": "Turns out she was 'Uncle Li'—they were fighting over territory and trust."
            },
            {
                "entry_id": 4,
                "day": 1,
                "time": "22:20",
                "event": "The woman left. Marcus saw me and pulled me into his room, furious.",
                "reaction": "He scolded me for sneaking around. I kept quiet."
            },
            {
                "entry_id": 5,
                "day": 1,
                "time": "22:30",
                "event": "Marcus said he wanted to rest, so I left and went to the dining car.",
                "reaction": "I ate a little, then set an alarm for 23:30 and went to sleep."
            },
            {
                "entry_id": 6,
                "day": 1,
                "time": "23:40",
                "event": "I woke up late. My stomach hurt—maybe the food was bad.",
                "reaction": "The plan was delayed, but I still had to act."
            },
            {
                "entry_id": 7,
                "day": 1,
                "time": "23:43",
                "event": "I brought my sickle and went to the restroom first.",
                "reaction": "Needed to prepare myself and check the corridor."
            },
            {
                "entry_id": 8,
                "day": 1,
                "time": "23:50",
                "event": "I sneaked into Marcus’s room. He looked asleep, so I took the diamonds.",
                "reaction": "He didn’t move at all... I grabbed them and ran."
            },
            {
                "entry_id": 9,
                "day": 1,
                "time": "23:54",
                "event": "I left the room quickly.",
                "reaction": "My heart was racing—I had the diamonds."
            },
            {
                "entry_id": 10,
                "day": 1,
                "time": "23:55",
                "event": "I bumped into the attendant Ou and the woman Lin.",
                "reaction": "I clutched the diamonds tightly and rushed off."
            },
            {
                "entry_id": 11,
                "day": 1,
                "time": "00:00",
                "event": "Back in my room, I realized my phone was missing.",
                "reaction": "Did I forget it? Or did someone take it?"
            },
            {
                "entry_id": 12,
                "day": 1,
                "time": "00:10",
                "event": "I stole a random passenger’s phone and texted my brother to pick me up.",
                "reaction": "Just then, a loud bang hit and I was thrown into the wall."
            },
            {
                "entry_id": 13,
                "day": 1,
                "time": "00:15",
                "event": "The train stopped. A broadcast said we were stuck and couldn’t move.",
                "reaction": "Perfect timing or bad luck?"
            }
        ]
    },
    # NPC No.3 Raven
    {
        "name": "Raven",
        "age": 18,
        "background":[
            "My name is Raven and I’ve lived on trains for as long as I can remember.",
            "I joined the Mafia when I was 18.",
            "I use the Trans-Siberian Railway to smuggle contraband—and I’ve never been caught.",
            "The Mafia boss trusts me and gives me all the manpower I need.",
            "Over the past ten years, I’ve taken full control of the Siberian route.",
            "Every shady deal on that line goes through me—no exceptions.",
            "No one knows what I really look like.",
            "I rent a private compartment and pose as a logistics company passenger.",
            "The police have tried to investigate me, but none of them made it back.",
            "People in the underworld call me 'Uncle Li'—they don’t know I’m a girl.",
            "Two years ago, a wealthy businessman named Marcus reached out through a middleman.",
            "He claimed to deal in herbs, but he’s involved in every dirty trade you can think of.",
            "I saw potential in him, so I agreed to work with him.",
            "He became one of my most reliable clients.",
            "He’s also one of the few who knows my true identity.",
            "Recently, My Mafia contact told me Zhen is trying to cut me out.",
            "He’s offering the Mafia direct deals behind my back.",
            "I was furious—this route is mine, and no one steals it from me.",
            "I found out Marcus is taking tonight’s train to Moscow with a load of smuggled diamonds.",
            "I arranged to meet him at 22:10 onboard.",
            "If he thinks he can betray me... he won’t make it to Moscow."
        ],
        "memory": [
            {
                "entry_id": 1,
                "day": 1,
                "time": "22:00",
                "event": "I boarded the train and finalized all preparations.",
                "reaction": "Everything was in place. I was ready for Marcus."
            },
            {
                "entry_id": 2,
                "day": 1,
                "time": "22:10",
                "event": "I arrived at car 7 to meet Marcus as planned. I asked if Marcus was trying to replace me.",
                "reaction": "He dodged the question. I’ve been on this train too long to fall for games. If he won’t talk, I’ll make sure he never speaks again."
            },
            {
                "entry_id": 3,
                "day": 1,
                "time": "22:20",
                "event": "I opened the door and saw a man across the hallway holding a phone, clearly panicked.",
                "reaction": "I think he was recording something. He may have seen too much. But before I could act, Marcus called him into the room. I waited by the door."
            },
            {
                "entry_id": 4,
                "day": 1,
                "time": "22:30",
                "event": "The unknown man left Marcus’s room.",
                "reaction": "I followed him quietly to learn more."
            },
            {
                "entry_id": 5,
                "day": 1,
                "time": "22:36",
                "event": "I confirmed his compartment was in car 9.",
                "reaction": "I decided to handle him later when the train was quiet."
            },
            {
                "entry_id": 6,
                "day": 1,
                "time": "22:40",
                "event": "I returned to my compartment in car 7.",
                "reaction": "I needed to wait until the time was right to move again."
            },
            {
                "entry_id": 7,
                "day": 1,
                "time": "23:45",
                "event": "I entered Marcus’s room. He was asleep on the bed.",
                "reaction": "Didn’t even need a gun. I took the fruit knife from the table and killed him. Clean, simple."
            },
            {
                "entry_id": 8,
                "day": 1,
                "time": "23:50",
                "event": "I went to the unknown man’s compartment in car 9 to eliminate him.",
                "reaction": "The room was empty. I searched his things and found his phone inside his coat."
            },
            {
                "entry_id": 9,
                "day": 1,
                "time": "23:55",
                "event": "On my way back to car 7, I saw the unknown man in the hallway. A train attendant was nearby.",
                "reaction": "To avoid exposure, I returned to my compartment and waited."
            },
            {
                "entry_id": 10,
                "day": 2,
                "time": "00:15",
                "event": "I heard a loud bang. The train suddenly stalled in the middle of nowhere.",
                "reaction": "Something was wrong. The situation was getting messy."
            }
        ]
    },
    # NPC No.4 Elena
    {
        "name": "Elena",
        "age": 20,
        "background": [
            "I grew up in a quiet town near H City, raised in a family that struggled to get by.",
            "In 2006, I was accepted into H City University to study fine arts.",
            "To help pay for tuition, I worked part-time as a nanny for a rich family on Taiping Mountain.",
            "My job was to care for their daughter Annie, a sweet and lively four-year-old.",
            "Her mother was kind to me and trusted me completely—she even gave me extra work to help with my fees.",
            "Annie had an older brother, Ethan, but he was always away at school—we rarely spoke.",
            "On November 11th, 2007, I overslept and arrived ten minutes late to pick up Annie from kindergarten.",
            "I saw a strange man carrying her into a car—I ran after them, but the car disappeared.",
            "We called the police. That afternoon, the kidnappers demanded 200 million in ransom.",
            "That evening, we followed every instruction and dropped the money at the meeting point.",
            "But no one came. At 11 p.m., police found Annie's body in a warehouse.",
            "I broke down. I blamed myself for everything—if only I hadn’t been late.",
            "The media and my classmates turned on me. Under pressure, I took a leave from school.",
            "Before I left, I drew the kidnapper’s face from memory for the police—it was all I could do.",
            "But the man vanished without a trace. No one ever found him.",
            "Five years ago, I came to Russia and became a train attendant on the Trans-Siberian Railway.",
            "I live quietly in a staff dormitory outside Moscow, hiding my grief and rage.",
            "In 2015, fate intervened—the man reappeared as a businessman named Marcus, boarding my train.",
            "He didn’t recognize me, but I recognized him. I started gathering his information in secret.",
            "On January 19th, 2017, at 22:00, I confirmed his cabin: Car 7. I work from Car 9.",
            "I’ve waited ten years for this moment. I won’t let Annie’s death go unpunished."
        ],
        "memory": [
            {
                "entry_id": 1,
                "day": 1,
                "time": "22:40",
                "event": "As a train attendant, I started checking tickets.",
                "reaction": "Focused and methodical, making sure everything was in order."
            },
            {
                "entry_id": 2,
                "day": 1,
                "time": "23:15",
                "event": "Finished checking all tickets.",
                "reaction": "Satisfied with the smooth progress."
            },
            {
                "entry_id": 3,
                "day": 1,
                "time": "23:20",
                "event": "Returned to the lounge and took out a syringe and sleeping pills prepared for an insomniac passenger.",
                "reaction": "Knowing Marcus’s preference for a certain drink, I injected the sleeping pills into his favorite beverage, then cleaned the syringe and put it away."
            },
            {
                "entry_id": 4,
                "day": 1,
                "time": "23:30",
                "event": "Placed the drugged drink on the dining car and went out to deliver it to Marcus.",
                "reaction": "Waiting patiently for the drug to take effect."
            },
            {
                "entry_id": 5,
                "day": 1,
                "time": "23:35",
                "event": "Returned to the lounge, took out the Swiss Army knife I had prepared, and hid it under the dining car.",
                "reaction": "Ready to act once Marcus falls asleep."
            },
            {
                "entry_id": 6,
                "day": 1,
                "time": "23:55",
                "event": "Pushed the cart towards Marcus’s cabin; feeling nervous, I walked quickly and encountered passengers Raven and Jax.",
                "reaction": "Lin returned to his cabin, Dong walked toward Car 9."
            },
            {
                "entry_id": 7,
                "day": 1,
                "time": "23:57",
                "event": "Reached Marcus’s cabin; he was lying still in bed.",
                "reaction": "In the darkness, I stabbed his heart with the knife, then quickly left."
            },
            {
                "entry_id": 8,
                "day": 1,
                "time": "00:00",
                "event": "Returned to my lounge to calm myself down.",
                "reaction": "Trying to steady my nerves after what I just did."
            },
            {
                "entry_id": 9,
                "day": 1,
                "time": "00:15",
                "event": "The train stalled in the middle of nowhere.",
                "reaction": "Unexpected and ominous."
            }

        ]
    },
    # NPC No.5 Ivan
    {
        "name": "Ivan",
        "age": 50,
        "background": [
	        "I am Ivan, an experienced driver and mechanic from a small village near H city.",
	        "I speak many languages and have driven long routes all over.",
	        "In 2002, at 25, I moved to H city and started washing cars.",
	        "I met Jia, who helped me get a job as a driver for the wealthy Ethan's family.",
	        "I mainly drove their son to school and sometimes looked after their daughter Annie.",
	        "I trusted Jia and told him about the family's schedule.",
	        "In 2007, Annie was kidnapped and later killed despite ransom being paid.",
	        "I was shocked to see Jia was behind it all.",
	        "Guilt-ridden, I quit my job and left H city.",
	        "For years, I lived full of shame and hatred.",
	        "In 2016, I spotted Jia, now called Marcus, rich from herbs.",
	        "I found he frequently traveled the Trans-Siberian Railway.",
	        "In 2017, I came to Russia determined to end this.",
	        "I bought a knife and prepared to confront him on the train."
        ],
        "memory": [
            {
                "entry_id": 1,
                "day": 1,
                "time": "21:45",
                "event": "I boarded the train, staying in car 12.",
                "reaction": "Calm and prepared for the journey ahead."
            },
            {
                "entry_id": 2,
                "day": 1,
                "time": "22:00",
                "event": "The train departed. I was in my room organizing my luggage. I didn’t know which car Marcus was in, but from previous intel, he was likely in a luxury compartment.",
                "reaction": "Slightly anxious but focused on the plan."
            },
            {
                "entry_id": 3,
                "day": 1,
                "time": "23:35",
                "event": "I began moving through the cars. The corridors were crowded, slowing me down.",
                "reaction": "Frustrated by the slow progress but kept moving."
            },
            {
                "entry_id": 4,
                "day": 1,
                "time": "23:40",
                "event": "Still no sign of Marcus’s compartment. Passing car 10, I found a railway document on the floor containing the passenger list. I picked it up and hurried back to my room to examine it.",
                "reaction": "Surprised and hopeful to find useful information."
            },
            {
                "entry_id": 5,
                "day": 1,
                "time": "23:50",
                "event": "Back in my room, I carefully checked the passenger list and found Marcus’s compartment number. I planned to act after midnight.",
                "reaction": "Determined and ready to move forward."
            },
            {
                "entry_id": 6,
                "day": 1,
                "time": "00:10",
                "event": "I quietly pushed open Marcus’s door with a knife in hand. As the train passed a small station, a flash of light revealed bloodstains on the sheets. I stabbed him once more in anger, dropped the knife, and quickly left.",
                "reaction": "Angry and relieved at finally confronting him."
            },
            {
                "entry_id": 7,
                "day": 1,
                "time": "00:15",
                "event": "A loud bang was heard; the train came to a halt.",
                "reaction": "Tense and alert, knowing something serious had happened."
            }
        ]
    }
]

for npc in npc_profiles:
    with open(f"npc_data/{npc['name'].lower()}.json", "w", encoding="utf-8") as f:
        json.dump(npc, f, indent=4, ensure_ascii=False)