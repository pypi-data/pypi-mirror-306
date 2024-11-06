import pytest
import re
from funtasks.tasks import add_task, complete_task, random_task, random_daily_goal, tasks

class Tests:
##############################
#add task tests

#TEST 1
    def test_add_task(self):
        tasks.clear()
        result=add_task("Do laundry", 3)
        assert result=="Task 'Do laundry' added with urgency 3."
        assert tasks["Do laundry"]["urgency"]==3
        assert tasks["Do laundry"]["completed"]==False

    #TEST 2
    def test_add_duplicate_task(self):
        tasks.clear()
        add_task("Grocery shopping", 3)
        with pytest.raises(ValueError) as exc_info:
            add_task("Grocery shopping", 3)
        assert str(exc_info.value)=="Task 'Grocery shopping' already exists."

    #TEST 3
    def test_add_new_category_task(self):
        tasks.clear()
        result=add_task("Walk the dog", 4)
        assert result=="Task 'Walk the dog' added with urgency 4."
        assert "Walk the dog" in tasks
        assert tasks["Walk the dog"]["urgency"]==4
        assert tasks["Walk the dog"]["completed"]==False    

    ##############################
    #complete task tests

    #TEST 1
    def test_complete_incomplete(self):
        """Test completing an existing, incomplete task."""
        tasks["Incomplete Task"] = {"urgency": 3, "completed": False}
        result = complete_task("Incomplete Task")
        assert result == "Task 'Incomplete Task' completed!"

    #TEST 2
    def test_complete_completed(self):
        """Test attempting to complete an already completed task."""
        tasks["Completed Task"] = {"urgency": 3, "completed": True}
        result = complete_task("Completed Task")
        assert result == "Task 'Completed Task' already completed."

    #TEST 3
    def test_complete_nonexist(self):
        """Test attempting to complete a non-existent task."""
        result = complete_task("Nonexistent Task")
        assert result == "Task 'Nonexistent Task' not found."
        
    ##############################
    #random task tests
        
    #TEST 1
    def test_random_task_no_tasks(self):
        tasks.clear()
        result = random_task()
        assert result == "No tasks available."

    #TEST 2
    def test_random_task_one_task(self):
        tasks.clear()
        tasks["Single Task"] = {"urgency": 2, "completed": False}
        result = random_task()
        assert result == "Random task: Single Task with urgency 2"

    #TEST 3
    def test_random_task_multiple_tasks(self):
        tasks.clear()
        tasks["Task 1"] = {"urgency": 2, "completed": False}
        tasks["Task 2"] = {"urgency": 4, "completed": False}
        tasks["Task 3"] = {"urgency": 5, "completed": False}
        result = random_task()
        assert re.match(r"Random task: .* with urgency \d", result)
        task_name = result.split(": ")[1].split(" with urgency")[0]
        assert task_name in tasks


        
    ##############################
    #daily goal task tests
        
    #TEST 1
    def test_random_daily_goal_quick(self):
        result=random_daily_goal(10)
        assert re.match(r"Quick task: .*!",result)

    #TEST 2
    def test_random_daily_goal_moderate(self):
        result=random_daily_goal(25)
        assert re.match(r"Moderate task: .*!",result)

    #TEST 3
    def test_random_daily_goal_long(self):
        result=random_daily_goal(60)
        assert re.match(r"Long task: .*!",result)
    ##############################