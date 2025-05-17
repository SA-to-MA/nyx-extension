class Agent:
    def __init__(self, _name, _actions):
        self.actions = _actions
        self.name = _name

    def add_action(self, _action):
        self.actions.append(_action)

    def get_next_action(self):
        if self.actions:
            return self.actions.pop(0)
        return "Done"

    def execute(self, _action, objects, screen):
        pass