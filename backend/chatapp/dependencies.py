import json


class Getdb:
    def __init__(self) -> None:
        self.file_name = 'my_db.json'
        self.data = {}
    
    def write_data(self, data):
        with open(self.file_name, "w", encoding='utf-8') as f:
            json.dump(data, f)
        self.data = data

    def read_data(self):
        try:
            with open(self.file_name, "r", encoding='utf-8') as f:
                self.data = json.load(f)
            return self.data
        except FileNotFoundError:
            self.data = {}
            return {}

