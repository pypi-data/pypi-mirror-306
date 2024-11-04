import random
from funtasks.tasks import add_task, complete_task, random_task, random_daily_goal, tasks

def main():
    # Clear all tasks to start fresh
    tasks.clear()
    
    # 1. Add tasks
    print("\n### Adding Tasks ###")
    try:
        print(add_task("Do laundry", 3))
        print(add_task("Grocery shopping", 2))
        print(add_task("Walk the dog", 4))
    except ValueError as e:
        print(e)
    
    # Attempt to add a duplicate task
    try:
        print(add_task("Do laundry", 3))
    except ValueError as e:
        print(e)
    
    # 2. Complete a task
    print("\n### Completing Tasks ###")
    print(complete_task("Do laundry"))
    
    # Attempt to complete the same task again
    print(complete_task("Do laundry"))
    
    # Attempt to complete a non-existent task
    print(complete_task("Nonexistent Task"))
    
    # 3. Get a random task
    print("\n### Random Task ###")
    print(random_task())
    
    # Clear tasks and test random_task with no tasks
    tasks.clear()
    print(random_task())

    # Testing random_task with a single task
    tasks["Groceries"] = {"urgency": 3, "completed": False}
    print("(One Task) " + random_task())
    
    # 4. Set daily goals based on available time
    print("\n### Daily Goals ###")
    print(random_daily_goal(10))  # Quick task
    print(random_daily_goal(25))  # Moderate task
    print(random_daily_goal(60))  # Long task

if __name__ == "__main__":
    main()
