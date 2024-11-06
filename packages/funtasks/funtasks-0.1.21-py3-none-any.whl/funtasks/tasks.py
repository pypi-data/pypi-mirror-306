import random

tasks={
    "Finish SWE project": {"urgency": 5, "completed": False},
    "Take out the trash": {"urgency": 1, "completed": False},
    "Finish personal project": {"urgency": 4, "completed": False},
    "Call a friend": {"urgency": 3, "completed": False},
    "Grocery shopping": {"urgency": 3, "completed": False},
    "Water the plants": {"urgency": 1, "completed": False},
    "Go for a run": {"urgency": 3, "completed": False},
    "Read a book": {"urgency": 2, "completed": False},
    "Complete a coding challenge": {"urgency": 2, "completed": False},
    "Plan a weekend getaway": {"urgency": 2, "completed": False},
    "Clean your room": {"urgency": 5, "completed": False},
    "Do laundry": {"urgency": 1, "completed": False},
    "Cook dinner": {"urgency": 3, "completed": False},
    "Take a nap": {"urgency": 1, "completed": False},
    "Watch a movie": {"urgency": 2, "completed": False},
    "Learn a new recipe": {"urgency": 3, "completed": False},
    "Do a puzzle": {"urgency": 2, "completed": False},
    "Write a blog post": {"urgency": 4, "completed": False},
}

#add task
def add_task(task_name:str,task_urgency:int):
    if task_name in tasks:
        raise ValueError(f"Task '{task_name}' already exists.")
    else:
        tasks[task_name]={"urgency": task_urgency, "completed": False}
        return f"Task '{task_name}' added with urgency {task_urgency}."

#complete task
def complete_task(task_name:str):
    if task_name not in tasks:
        return f"Task '{task_name}' not found."
    elif task_name in tasks and not tasks[task_name]["completed"]:
        tasks[task_name]["completed"]=True
        return f"Task '{task_name}' completed!"
    else:
        return f"Task '{task_name}' already completed."

#random task
def random_task():
    if not tasks:
        return "No tasks available."
    else:
        task=random.choice(list(tasks.keys()))
        return f"Random task: {task} with urgency {tasks[task]['urgency']}"

#daily goal
def random_daily_goal(daily_goal_time:int):
    sub15tasks=["Take a quick walk","Take a shower","Have a glass of water","Do a handstand","Meditate for 15 minutes","Watch 10 tiktoks"]
    sub30tasks=["Read a chapter of a book","Run 3 miles","Clean dishes","Write a blog post","Do a 30 minute workout","Watch a show"]
    longtasks=["Run a marathon","Travel to Australia","Write a book","Adopt a dog","Watch a movie","Learn a new language"]
    if daily_goal_time<=15:
        task=random.choice(sub15tasks)
        return f"Quick task: {task}!"
    elif daily_goal_time<=30:
        task=random.choice(sub30tasks)
        return f"Moderate task: {task}!"
    else:
        task=random.choice(longtasks)
        return f"Long task: {task}!"