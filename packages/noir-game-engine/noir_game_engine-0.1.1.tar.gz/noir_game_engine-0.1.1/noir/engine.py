class Node:
    def __init__(self, description, options=None):
        self.description = description
        self.options = options if options else {}

class NoirEngine:
    def __init__(self):
        self.nodes = {}
        self.current_node = "start"

    def add_node(self, name, description, options=None):
        self.nodes[name] = Node(description, options)

    def run(self):
        while True:
            node = self.nodes[self.current_node]
            self.current_node = self._prompt_user(node)

    def _prompt_user(self, node):
        print(node.description)
        if node.options:
            for i, option in enumerate(node.options):
                print(f"{i + 1}. {option}")
            choice = input("Choose an option: ")
            return node.options[list(node.options.keys())[int(choice) - 1]]
        return "end"