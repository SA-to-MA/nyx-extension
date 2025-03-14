class StateNode:
    def __init__(self, state, parent=None, action=None):
        self.state = state  # The actual state object
        self.parent = parent  # Link to parent state (None for root)
        self.children = []  # List of child nodes
        self.action = action  # Action that led to this state

    def add_child(self, child_state, action):
        """Creates a new child node and adds it to the tree."""
        child_node = StateNode(child_state, parent=self, action=action)
        self.children.append(child_node)
        return child_node  # Return new node reference