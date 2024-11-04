![Python build & test](https://github.com/software-students-fall2024/3-python-package-java_and_the_scripts_/actions/workflows/build.yaml/badge.svg)


# Python Package Exercise
**Funtasks: A Task Management Package** 

This package was created by generally following the [Packaging Python Projects](https://packaging.python.org/tutorials/packaging-projects/) guide, with the addition of `pipenv` for virtual environment management. 

## Overview
Funtasks is a simple and efficient task management package designed to help you add, complete, and randomly select tasks. It includes features for adding tasks with urgency levels, marking tasks as complete, and generating random tasks or daily goals based on your available time. 


## How to install and use this package

1. Make sure you have `pipenv` installed. You can install it using `pip3`:
    ```bash
    pip3 install pipenv

2. To install the package, use `pip3` because this package requires Python 3:
    ```bash
    pip3 install funtasks==0.1.11

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
```exit```

Additionally, we have provided an example script that you can run directly:

1. Create an activate ```pipenv``` virtual environment as before.
2. Run the package directly from the command line: ```python3 -m funtasks```. This should directly run the code in the ```__main__.py```.
3. Exit the virtual environment:
```exit```

## How to run unit tests
We've included 3 unit tests for each function in our ```funtasks`` package. To run these tests:

1. Install pytest in a virtual environment
2. Now, you can run the tests from the main project directory: ```python3 -m pytest```
3. All tests should pass to ensure that the production code is behaving correctly
