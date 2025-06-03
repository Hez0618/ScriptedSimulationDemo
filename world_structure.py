from typing import Optional, Dict
import json

class WorldNode:
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.children: Dict[str, 'WorldNode'] = {}
        self.clue = None
        self.description = description

    def add_child(self, child_name: str, description: str = "") -> 'WorldNode':
        if child_name not in self.children:
            self.children[child_name] = WorldNode(child_name, description)
        return self.children[child_name]

    def find_node_by_path(self, path: list[str]) -> Optional['WorldNode']:
        if not path:
            return self
        first, *rest = path
        child = self.children.get(first)
        if not child:
            print(f"[DEBUG] Path not found at: {first}")
            print(f"[DEBUG] Available children at this level: {list(self.children.keys())}")
            return None
        return child.find_node_by_path(rest)

    def get_all_clues(self) -> list[dict]:
        clues = []
        if self.clue:
            clues.append(self.clue)
        for child in self.children.values():
            clues.extend(child.get_all_clues())
        return clues

    def __repr__(self, level=0):
        indent = "  " * level
        s = f"{indent}- {self.name}"
        if self.description:
            s += f" ({self.description})"
        if self.clue:
            s += f" [Clue: {self.clue['name']}]"
        for child in self.children.values():
            s += "\n" + child.__repr__(level + 1)
        return s


def create_world_from_clues(file_path: str) -> WorldNode:
    with open(file_path, 'r', encoding='utf-8') as f:
        clues = json.load(f)

    root = WorldNode("Train")

    for clue in clues:
        path = clue['location']
        node = root
        for p in path[1:]:
            node = node.add_child(p)
        node.clue = clue

    return root


def add_non_clue_node(root: WorldNode, path: list[str], node_name: str, description: str = ""):
    parent_node = root.find_node_by_path(path[1:])
    if parent_node is None:
        raise ValueError(f"路径{' -> '.join(path)}未找到，无法添加节点。")
    parent_node.add_child(node_name, description)

def ensure_path(root: WorldNode, path: list[str]):
    node = root
    for p in path[1:]:  # skip "Train"
        node = node.add_child(p)

def add_non_clue_nodes_batch(root: WorldNode, nodes: list[dict]):
    """
    nodes is a list of dictionaries, each containing:
    {
        "path": [...],          # Parent node path, e.g. ["Train", "Carriage 9", "Room 5"]
        "node_name": "Desk",    # Name of the new node
        "description": "Description text"  # Optional description
    }
    """
    for node_info in nodes:
        path = node_info["path"]
        name = node_info["name"]
        desc = node_info.get("description", "")
        ensure_path(root, path)
        try:
            add_non_clue_node(root, path, name, desc)
        except ValueError as e:
            print(f"fail to add node: {e}")

def get_train_room_structure(root: WorldNode) -> str:
    """
    返回火车的整体结构（只展示车厢和房间，不包含物品）
    """
    def helper(node: WorldNode, level=0):
        indent = "  " * level
        lines = [f"{indent}- {node.name}"]
        # 只往下展示两层结构：Carriage -> Rooms
        if level < 2:
            for child in node.children.values():
                lines.extend(helper(child, level + 1))
        return lines

    return "\n".join(helper(root))


def get_room_explorables(root: WorldNode, path: list[str]) -> str:
    """
    Return the list of explorable items directly under the specified path (room),
    showing only the immediate children without revealing any clue information.
    """
    node = root.find_node_by_path(path[1:])  # skip "Train"
    if not node:
        return "The room does not exist."

    if not node.children:
        return "There doesn't seem to be anything here."

    lines = [f"You have entered {' -> '.join(path)}. The items you can explore here are:"]
    for child in node.children.values():
        line = f"- {child.name}"
        if child.description:
            line += f" ({child.description})"
        lines.append(line)
    return "\n".join(lines)

def check_for_clue(root: WorldNode, path: list[str]) -> Optional[dict]:
    """
    判断指定路径物品是否包含线索，返回线索字典或 None
    """
    node = root.find_node_by_path(path[1:])
    if node and node.clue:
        return node.clue
    return None

def initialize_world(clue_file_path: str) -> WorldNode:
    """
    初始化世界结构，加载线索数据并添加无线索节点，返回根节点WorldNode。
    """
    world = create_world_from_clues(clue_file_path)

    nodes_to_add = [
        {
            "path": ["Train", "Carriage 9", "Room 5"],
            "name": "Desk",
            "description": "A wooden desk with a few scratch marks."
        }
    ]

    add_non_clue_nodes_batch(world, nodes_to_add)

    return world