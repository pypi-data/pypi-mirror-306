from InquirerPy import prompt

class Node:
    def __init__(self, prompt_text, options):
        self.prompt_text = prompt_text
        self.options = options

    def display(self):
        choices = [{'name': option['text'], 'value': option['outcome']} for option in self.options]
        question = {
            'type': 'list',
            'name': 'choice',
            'message': self.prompt_text,
            'choices': choices
        }
        answer = prompt([question])
        return answer['choice']

class NoirEngine:
    def __init__(self):
        self.nodes = {}
        self.variables = {}
        self.current_node = None

    def add_node(self, node_id, node):
        self.nodes[node_id] = node

    def set_start(self, node_id):
        self.current_node = node_id

    def run(self):
        while self.current_node:
            node = self.nodes[self.current_node]
            self.current_node = node.display()