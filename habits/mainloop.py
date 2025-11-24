#mainloop
from habits import Habit, save_habits_json, load_habits
import json

while True:
    task = input('what would you like me to do add/complete/note/show/delete/exit: ')
    
    if task == 'add':
        habit = input('What habit would like to add: ')
        h1 = Habit(habit)
        save_habits_json(h1, 'habit.json')
    
    if task == 'complete':
        habit_name = input('Which habit did you complete? ')
        habits = load_habits('habit.json')
        if habit_name in habits:
            h1 = Habit(habit_name)
            h1.count = habits[habit_name]['count']
            h1.last_done = habits[habit_name]['last_done']
            h1.note = habits[habit_name]['note']
            h1.complete()
            save_habits_json(h1, 'habit.json')
        else:
            print('Habit not found!')
    
    if task == 'note':
        habit_name = input('Which habit? ')
        habits = load_habits('habit.json')
        if habit_name in habits:
            h1 = Habit(habit_name)
            h1.count = habits[habit_name]['count']
            h1.last_done = habits[habit_name]['last_done']
            h1.note = habits[habit_name]['note']
            note = input('Add a note: ')
            h1.add_note(note)
            save_habits_json(h1, 'habit.json')
        else:
            print('Habit not found!')
    
    if task == 'show':
        print(load_habits('habit.json'))
    
    if task == 'delete':
        habit = input('What habit do you want to remove? ')
        habits = load_habits('habit.json')
        if habit in habits:
            del habits[habit]
            with open('habit.json', 'w') as f:
                json.dump(habits, f, indent=2)
            print(f'Habit "{habit}" deleted!')
        else:
            print('Habit not found!')
    
    if task == 'exit':
        break
