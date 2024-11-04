![Python build & test](https://github.com/software-students-fall2024/3-python-package-java_and_the_scripts_/actions/workflows/build.yaml/badge.svg)


# Python Package Exercise
**Funtasks: A Task Management Package** 

This package was created by generally following the [Packaging Python Projects](https://packaging.python.org/tutorials/packaging-projects/) guide, with the addition of `pipenv` for virtual environment management. 

## Overview
Funtasks is a simple and fun task management package designed to help you add, complete, and randomly select tasks. It includes features for adding tasks with urgency levels, marking tasks as complete, and generating random tasks or daily goals based on your available time. 

## Team members

[Natalie Ovcarov](https://github.com/nataliovcharov)

[Jun Li](https://github.com/jljune9li )

[Daniel Brito](https://github.com/danny031103 )

[Alvaro Martinez](https://github.com/AlvaroMartinezM)

## Link to our package on PyPI
[PyPI package Link](https://pypi.org/project/funtasks/)

## How to install and use this package

1. Make sure you have `pipenv` installed. You can install it using `pip3`:
    ```bash
    pip3 install pipenv

2. To install the package, use `pip3` because this package requires Python 3:
    ```bash
    pip3 install funtasks

3. Activate the virtual environment: 
    ```bash
    pipenv shell

4. Create a Python program file that imports the package and uses it, e.g. 
    ```bash
    from funtasks.tasks import add_task, complete_task, random_task, random_daily_goal, tasks

This approach lets you directly use ```add_task```, ```complete_task```, ```random_task```, and ```random_daily_goal```

5. Run the program:
    ```bash
    python3 your_program_filename.py

6. Exit the virtual environment:
    ```bash
    exit

Additionally, we have provided an example script that you can run directly:

1. Create an activate ```pipenv``` virtual environment as before.
2. Run the package directly from the command line: ```python3 -m funtasks```. This should directly run the code in the ```__main__.py```.
3. Exit the virtual environment:
```exit```

## How to run unit tests
We've included 3 unit tests for each function in our ```funtasks``` package. To run these tests:

1. Install pytest in a virtual environment
2. Now, you can run the tests from the main project directory: ```python3 -m pytest```
3. All tests should pass to ensure that the production code is behaving correctly

## Usage
### How to import funtasks
```bash
from funtasks.tasks import add_task, complete_task, random_task,random_daily_goal, tasks
```
    

### Functions Overview

- **add_task(task_name: str, urgency: int) -> str**

    - Description: Adds a new task to the list with a specified urgency level.
    Parameters:
    - task_name: The name of the task to add.
    - urgency: An integer representing the urgency level (1–5, with 5 being the most urgent).
    - Returns: A confirmation message upon successful addition.
    - Raises: ValueError if the task already exists.

- Example: 
```bash
add_task(“Do laundry”, 3)
```
- **complete_task(task_name: str) -> str**

    - Description: Marks a task as completed.
    - Parameters:
    - task_name: The name of the task to complete.
    - Returns: A confirmation message or a message indicating the task doesn't exist.

- Example: 
```bash
complete_task("Do laundry")
```
- **random_task() -> str**

    - Description: Retrieves a random task from the list.
    - Returns: The name of a random task or a message indicating there are no tasks.

- Example: 
```bash
random_task()
```
- **random_daily_goal(available_time: int) -> str**

    - Description: Suggests a task based on the available time.
    Parameters:
    - available_time: Time available in minutes (used to determine task urgency).
    - Returns: A task that fits the time constraint or a message indicating no tasks are suitable.

- Example: 
```bash
random_daily_goal(25)
```

## How to contribute to Funtasks

***Prerequisites***: Make sure you have Python 3.9 or higher installed. You can check your version by running:
```bash
python3 --version
```

1. Clone the repository: 
    ```bash
    git clone https://github.com/software-students-fall2024/3-python-package-java_and_the_scripts_.git

2. Enter the directory:
    ```bash
    cd  3-python-package-java_and_the_scripts_

3. Set up a virtual environment using ```pipenv```: If ```pipenv``` has not been installed, install using ```pip3 install pipenv```. Now, run the following command to install all dependencies that we've included in the provided ```Pipfile```: 
    ```bash
    pipenv install --dev

4. Activate the virtual environment:
    ```bash
    pipenv shell

5. Modify and Run the file: Make the changes you need to the project, and run the main program to test. 
    ```bash
    python -m funtasks
If you want to run another specific file (like tasks.py), you can run it as follows:
    ```bash
    python src/funtasks/tasks.py

6. To run tests: Now, you can also run the unit tests we've provided in the package using ```pytest```. Again, make sure ```pytest``` is installed in the virtual envrionment.
    ```bash
    pipenv run pytest

7. Build the package:
    ```bash
    python3 -m build

8. Exit the virtual environment: Once you're done working with the project, you can deactivate the virtual environment with:
    ```bash
    exit
