class Task:
    id: int
    text = ""
    done = False

    def __init__(self, id, text, done):
        self.id = id
        self.text = text
        self.done = done

class User:
    id: int
    name: str = ""
    tasks: list[Task] = []

    def __init__(self, name, id):
        self.name = name
        self.id = id

    def from_dict(self, data: list[dict]):
        user_tasks = []
        for task in data:
            new_task = Task(task['id'], task['text'], task['done'])
            user_tasks.append(new_task)
        self.tasks = user_tasks
