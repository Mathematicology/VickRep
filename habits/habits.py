#habits.py - FIXED VERSION
import json
from datetime import date

class Habit:
    def __init__(self, name, note=""):
        self.name = name
        self.count = 0
        self.last_done = None
        self.note = note

    def complete(self):
        self.count += 1
        self.last_done = str(date.today())
        print(f"{self.name} updated! Total count: {self.count}")

    def add_note(self, note):
        self.note = note
        print(f"Note for {self.name} updated.")

    def __str__(self):
        return f"{self.name}: Done {self.count} times, Last done {self.last_done}, Note: {self.note}"
    
    def to_dict(self):
        return {
            'count': self.count,
            'last_done': self.last_done,
            'note': self.note
        }

def save_habits_json(habit, filename):
    # Load existing habits first (THIS IS THE FIX!)
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    
    # Add/update this habit
    data[habit.name] = habit.to_dict()
    
    # Save everything back
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def load_habits(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}