"""
habits.py - Complete Habit Tracker Implementation
Meets all OOFPP assignment requirements
"""

import json
from datetime import datetime, date, timedelta
from typing import List, Dict, Optional


class Habit:
    """
    Represents a single habit with tracking capabilities.
    
    Attributes:
        name (str): Name of the habit
        description (str): Description of what the habit entails
        periodicity (str): 'daily' or 'weekly'
        created_date (str): ISO format date when habit was created
        completions (list): List of completion dates in ISO format
    """
    
    def __init__(self, name: str, description: str = "", periodicity: str = "daily"):
        """
        Initialize a new habit.
        
        Args:
            name: Name of the habit
            description: What the habit is about
            periodicity: 'daily' or 'weekly'
        """
        self.name = name
        self.description = description
        self.periodicity = periodicity.lower()
        self.created_date = str(date.today())
        self.completions = []  # List of completion dates
        
        if self.periodicity not in ['daily', 'weekly']:
            raise ValueError("Periodicity must be 'daily' or 'weekly'")
    
    def complete(self, completion_date: Optional[str] = None):
        """
        Mark habit as complete for a specific date.
        
        Args:
            completion_date: Date in 'YYYY-MM-DD' format, or None for today
        """
        if completion_date is None:
            completion_date = str(date.today())
        else:
            # Validate date format
            try:
                datetime.strptime(completion_date, '%Y-%m-%d')
            except ValueError:
                print(f"❌ Invalid date format! Use YYYY-MM-DD")
                return
        
        # Avoid duplicate completions on same date
        if completion_date not in self.completions:
            self.completions.append(completion_date)
            self.completions.sort()  # Keep chronological order
            print(f"✓ '{self.name}' completed on {completion_date}")
        else:
            print(f"⚠️  '{self.name}' already completed on {completion_date}")
    
    def get_current_streak(self) -> int:
        """
        Calculate current streak (consecutive periods without breaking).
        
        Returns:
            Number of consecutive periods maintained
        """
        if not self.completions:
            return 0
        
        # Sort completions
        sorted_completions = sorted(self.completions)
        last_completion = datetime.strptime(sorted_completions[-1], '%Y-%m-%d').date()
        
        # Check if habit is currently active
        today = date.today()
        if self.periodicity == 'daily':
            max_gap = timedelta(days=1)
        else:  # weekly
            max_gap = timedelta(days=7)
        
        # If last completion is too old, streak is broken
        if today - last_completion > max_gap:
            return 0
        
        # Count backwards to find streak
        streak = 1
        for i in range(len(sorted_completions) - 2, -1, -1):
            current = datetime.strptime(sorted_completions[i], '%Y-%m-%d').date()
            next_completion = datetime.strptime(sorted_completions[i + 1], '%Y-%m-%d').date()
            
            gap = next_completion - current
            if self.periodicity == 'daily':
                if gap <= timedelta(days=1):
                    streak += 1
                else:
                    break
            else:  # weekly
                if gap <= timedelta(days=7):
                    streak += 1
                else:
                    break
        
        return streak
    
    def get_longest_streak(self) -> int:
        """
        Calculate the longest streak ever achieved for this habit.
        
        Returns:
            Maximum number of consecutive periods
        """
        if not self.completions:
            return 0
        
        sorted_completions = sorted(self.completions)
        max_streak = 1
        current_streak = 1
        
        for i in range(1, len(sorted_completions)):
            current = datetime.strptime(sorted_completions[i - 1], '%Y-%m-%d').date()
            next_completion = datetime.strptime(sorted_completions[i], '%Y-%m-%d').date()
            
            gap = next_completion - current
            if self.periodicity == 'daily':
                if gap <= timedelta(days=1):
                    current_streak += 1
                else:
                    current_streak = 1
            else:  # weekly
                if gap <= timedelta(days=7):
                    current_streak += 1
                else:
                    current_streak = 1
            
            max_streak = max(max_streak, current_streak)
        
        return max_streak
    
    def to_dict(self) -> Dict:
        """Convert habit to dictionary for JSON storage."""
        return {
            'name': self.name,
            'description': self.description,
            'periodicity': self.periodicity,
            'created_date': self.created_date,
            'completions': self.completions
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Habit':
        """
        Create Habit object from dictionary.
        
        Args:
            data: Dictionary with habit data
            
        Returns:
            Habit object with all data preserved
        """
        habit = cls(
            name=data['name'],
            description=data.get('description', ''),
            periodicity=data.get('periodicity', 'daily')
        )
        habit.created_date = data.get('created_date', str(date.today()))
        habit.completions = data.get('completions', [])
        return habit
    
    def __str__(self) -> str:
        """String representation of habit."""
        streak = self.get_current_streak()
        return (f"📌 {self.name} ({self.periodicity})\n"
                f"   Created: {self.created_date}\n"
                f"   Completions: {len(self.completions)}\n"
                f"   Current Streak: {streak}\n"
                f"   Description: {self.description}")


# ============================================================================
# STORAGE FUNCTIONS
# ============================================================================

def save_habits(habits: List[Habit], filename: str = 'habits_data.json'):
    """
    Save all habits to JSON file.
    
    Args:
        habits: List of Habit objects
        filename: Name of JSON file
    """
    data = {habit.name: habit.to_dict() for habit in habits}
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"💾 Saved {len(habits)} habits to {filename}")


def load_habits(filename: str = 'habits_data.json') -> List[Habit]:
    """
    Load all habits from JSON file.
    
    Args:
        filename: Name of JSON file
        
    Returns:
        List of Habit objects
    """
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        habits = [Habit.from_dict(habit_data) for habit_data in data.values()]
        return habits
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def load_predefined_habits(filename: str = 'habits_data.json') -> List[Habit]:
    """
    Create 5 predefined habits with 4 weeks of test data.
    This serves as test fixtures for the application.
    
    Returns:
        List of 5 Habit objects with sample data
    """
    habits = []
    
    # Calculate dates for 4 weeks of data
    today = date.today()
    
    # Habit 1: Daily - Exercise (high compliance)
    exercise = Habit("Exercise", "30 minutes of physical activity", "daily")
    exercise.created_date = str(today - timedelta(days=28))
    for i in range(28):
        if i % 7 not in [6]:  # Miss one day per week (Sunday)
            exercise.completions.append(str(today - timedelta(days=28-i)))
    habits.append(exercise)
    
    # Habit 2: Daily - Read (medium compliance)
    read = Habit("Read", "Read for 20 minutes", "daily")
    read.created_date = str(today - timedelta(days=28))
    for i in range(28):
        if i % 3 != 0:  # Miss every 3rd day
            read.completions.append(str(today - timedelta(days=28-i)))
    habits.append(read)
    
    # Habit 3: Daily - Meditate (recent start, good streak)
    meditate = Habit("Meditate", "10 minutes mindfulness", "daily")
    meditate.created_date = str(today - timedelta(days=14))
    for i in range(14):
        meditate.completions.append(str(today - timedelta(days=14-i)))
    habits.append(meditate)
    
    # Habit 4: Weekly - Grocery Shopping (perfect compliance)
    grocery = Habit("Grocery Shopping", "Weekly grocery run", "weekly")
    grocery.created_date = str(today - timedelta(days=28))
    for i in range(4):  # 4 weeks
        grocery.completions.append(str(today - timedelta(days=28-i*7)))
    habits.append(grocery)
    
    # Habit 5: Weekly - Clean Apartment (some misses)
    clean = Habit("Clean Apartment", "Deep clean living space", "weekly")
    clean.created_date = str(today - timedelta(days=28))
    for i in [0, 1, 3]:  # Missed week 2
        clean.completions.append(str(today - timedelta(days=28-i*7)))
    habits.append(clean)
    
    # Save to file
    save_habits(habits, filename)
    print(f"✅ Created 5 predefined habits with 4 weeks of test data")
    
    return habits


# ============================================================================
# ANALYTICS MODULE - FUNCTIONAL PROGRAMMING PARADIGM
# ============================================================================

def get_all_habits(habits: List[Habit]) -> List[str]:
    """
    Return list of all tracked habit names.
    
    Args:
        habits: List of Habit objects
        
    Returns:
        List of habit names
    """
    return list(map(lambda h: h.name, habits))


def get_habits_by_periodicity(habits: List[Habit], periodicity: str) -> List[str]:
    """
    Return habits with specified periodicity.
    
    Args:
        habits: List of Habit objects
        periodicity: 'daily' or 'weekly'
        
    Returns:
        List of habit names matching periodicity
    """
    return list(map(
        lambda h: h.name,
        filter(lambda h: h.periodicity == periodicity.lower(), habits)
    ))


def get_longest_streak_all(habits: List[Habit]) -> tuple:
    """
    Find the longest streak across all habits.
    
    Args:
        habits: List of Habit objects
        
    Returns:
        Tuple of (habit_name, streak_length)
    """
    if not habits:
        return ("None", 0)
    
    streaks = list(map(lambda h: (h.name, h.get_longest_streak()), habits))
    return max(streaks, key=lambda x: x[1])


def get_longest_streak_for_habit(habits: List[Habit], habit_name: str) -> int:
    """
    Get longest streak for a specific habit.
    
    Args:
        habits: List of Habit objects
        habit_name: Name of the habit
        
    Returns:
        Longest streak count, or 0 if not found
    """
    matching_habits = list(filter(lambda h: h.name == habit_name, habits))
    if not matching_habits:
        return 0
    return matching_habits[0].get_longest_streak()


def get_struggle_habits(habits: List[Habit], min_completions: int = 5) -> List[str]:
    """
    Find habits with low completion rates (struggling habits).
    
    Args:
        habits: List of Habit objects
        min_completions: Minimum expected completions
        
    Returns:
        List of habit names with low completion rates
    """
    return list(map(
        lambda h: h.name,
        filter(lambda h: len(h.completions) < min_completions, habits)
    ))


def get_completion_summary(habits: List[Habit]) -> Dict[str, int]:
    """
    Get summary of total completions per habit.
    
    Args:
        habits: List of Habit objects
        
    Returns:
        Dictionary mapping habit names to completion counts
    """
    from functools import reduce
    
    return reduce(
        lambda acc, h: {**acc, h.name: len(h.completions)},
        habits,
        {}
    )
