#habits.py - FIXED VERSION WITH DATE INPUT & DATA PRESERVATION
import json
from datetime import date, datetime

class Habit:
    def __init__(self, name, note="", count=0, last_done=None):
        """Initialize habit with optional existing data"""
        self.name = name
        self.count = count  # Now accepts existing count!
        self.last_done = last_done  # Now accepts existing date!
        self.note = note

    def complete(self, completion_date=None):
        """
        Mark habit as complete
        completion_date: str in 'YYYY-MM-DD' format, or None for today
        """
        self.count += 1
        
        if completion_date:
            # Validate date format
            try:
                datetime.strptime(completion_date, '%Y-%m-%d')
                self.last_done = completion_date
            except ValueError:
                print(f"Invalid date format! Using today's date.")
                self.last_done = str(date.today())
        else:
            self.last_done = str(date.today())
        
        print(f"✓ {self.name} completed! Total: {self.count} times, Last: {self.last_done}")

    def add_note(self, note):
        """Add or update a note for this habit"""
        self.note = note
        print(f"✓ Note for '{self.name}' updated.")

    def __str__(self):
        return f"{self.name}: {self.count} times | Last: {self.last_done} | Note: {self.note}"
    
    def to_dict(self):
        """Convert habit to dictionary for JSON storage"""
        return {
            'count': self.count,
            'last_done': self.last_done,
            'note': self.note
        }

    @classmethod
    def from_dict(cls, name, data):
        """Create Habit object from stored dictionary - PRESERVES ALL DATA"""
        return cls(
            name=name,
            count=data.get('count', 0),
            last_done=data.get('last_done', None),
            note=data.get('note', '')
        )


def save_habits_json(habit, filename):
    """Save a single habit to JSON file (preserves other habits)"""
    # Load existing habits
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    
    # Update/add this habit
    data[habit.name] = habit.to_dict()
    
    # Save back to file
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"💾 Saved '{habit.name}' to {filename}")


def load_habits(filename):
    """Load all habits from JSON file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def load_habit_object(habit_name, filename):
    """
    Load a specific habit as a Habit object
    Returns None if habit doesn't exist
    """
    habits = load_habits(filename)
    if habit_name in habits:
        return Habit.from_dict(habit_name, habits[habit_name])
    return None
