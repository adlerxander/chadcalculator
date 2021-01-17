from typing import Optional


class Node:
    left: Optional[str]
    right: Optional[str]
    data: str

    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data
