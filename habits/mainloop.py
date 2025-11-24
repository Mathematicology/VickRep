#mainloop.py - FIXED VERSION
from habits import Habit, save_habits_json, load_habits, load_habit_object
import json

print("=" * 50)
print("🎯 HABIT TRACKER")
print("=" * 50)

while True:
    print("\n📋 Commands: add | complete | note | show | delete | exit")
    task = input('➤ What would you like to do? ').strip().lower()
    
    if task == 'add':
        habit = input('📝 Habit name: ').strip()
        if habit:
            h1 = Habit(habit)
            save_habits_json(h1, 'habit.json')
        else:
            print("❌ Habit name cannot be empty!")
    
    elif task == 'complete':
        habit_name = input('✓ Which habit did you complete? ').strip()
        
        # Load the habit with ALL its data preserved
        h1 = load_habit_object(habit_name, 'habit.json')
        
        if h1:
            # Ask if they want to specify a date
            date_choice = input('📅 Complete for today? (y/n): ').strip().lower()
            
            if date_choice == 'y':
                h1.complete()  # Uses today's date
            else:
                custom_date = input('📅 Enter date (YYYY-MM-DD): ').strip()
                h1.complete(custom_date)  # Uses custom date
            
            save_habits_json(h1, 'habit.json')
        else:
            print(f"❌ Habit '{habit_name}' not found!")
    
    elif task == 'note':
        habit_name = input('📌 Which habit? ').strip()
        
        # Load the habit with ALL its data preserved
        h1 = load_habit_object(habit_name, 'habit.json')
        
        if h1:
            note = input('✏️  Add a note: ').strip()
            h1.add_note(note)
            save_habits_json(h1, 'habit.json')
        else:
            print(f"❌ Habit '{habit_name}' not found!")
    
    elif task == 'show':
        habits = load_habits('habit.json')
        if habits:
            print("\n" + "=" * 50)
            print("📊 YOUR HABITS")
            print("=" * 50)
            for name, data in habits.items():
                h = Habit.from_dict(name, data)
                print(f"\n🔹 {h}")
            print("=" * 50)
        else:
            print("📭 No habits tracked yet!")
    
    elif task == 'delete':
        habit = input('🗑️  Which habit to remove? ').strip()
        habits = load_habits('habit.json')
        
        if habit in habits:
            confirm = input(f'⚠️  Delete "{habit}"? (y/n): ').strip().lower()
            if confirm == 'y':
                del habits[habit]
                with open('habit.json', 'w') as f:
                    json.dump(habits, f, indent=2)
                print(f'✓ Habit "{habit}" deleted!')
        else:
            print(f"❌ Habit '{habit}' not found!")
    
    elif task == 'exit':
        print("👋 Goodbye! Keep building those habits!")
        break
    
    else:
        print("❌ Invalid command! Try: add, complete, note, show, delete, or exit")
