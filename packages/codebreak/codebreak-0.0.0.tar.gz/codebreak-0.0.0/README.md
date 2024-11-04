# Python Package Exercise

An exercise to create a Python package, build it, test it, distribute it, and use it. See [instructions](./instructions.md) for details.

[![.github/workflows/ci.yml](https://github.com/software-students-fall2024/3-python-package-the-fixers/actions/workflows/ci.yml/badge.svg)](https://github.com/software-students-fall2024/3-python-package-the-fixers/actions/workflows/ci.yml)

## Project Description

Our python package returns different recommendations for stretches and exercises for coders who want to take a break after coding for a period of time. The function mental_exercises takes ‘focus’, ‘creativity’, or ‘mindfulness’ as an argument and outputs a corresponding quote. The function stretches takes integer values ranging from 1 to 15 as an argument and outputs a stretch that takes the given number of minutes to complete. The eye_exercises function takes an integer value that equals 10, 20 or 60 and outputs an eye exercise that takes 10, 20, or 60 seconds to complete. The physical_exercises function takes in user input of their preferred physical exercise (ex. Running or strength), asks them for their preferred degree of intensity for the exercise, and then finally asks the user for the preferred time interval between each exercise. From then on the user will get a reminder to do their preferred physical exercise once their preferred time interval is up.  The purpose of our functions is to promote regular wellness breaks that help reduce physical and mental strain. Each function offers tailored suggestions for brief activities—such as stretching, eye exercises, movement, and mental exercises—that encourage a balanced, healthy routine throughout the day, especially for individuals with sedentary or screen-heavy tasks.

## PyPI Website 
https://pypi.org/project/codebreak/0.1/

## Developer Instructions 
how a developer who wants to import your project into their own code can do so - include documentation and code examples for all functions in your package and a link to an example Python program that uses each of them.

Step 1: Install the Package
To use codebreak in your project, first install it from PyPI. In your terminal or command prompt, type:
```
pip install codebreak
```

Step 2: Import and Use the Package
After installation, you can import CodeBreak modules and functions directly into your Python code. Below is a description of each function and class in the package, along with usage examples.

Function Documentation and Examples
1. Eye Exercise (eye_exercise function)
Provides a quick eye exercise suggestion based on the specified duration in seconds.

Function: eye_exercise(duration: int) -> str
Parameters:
duration (int): The duration for the exercise (options: 10, 20, or 60 seconds)
Returns: A string describing an eye exercise suggestion for the specified duration.
Example Usage:

```
from codebreak.eye_exercises import eye_exercise

# Get a 10-second eye exercise suggestion
print(eye_exercise(10))
```

2. Mental Exercise (mental_exercise function)
Provides a mental exercise suggestion based on the type of break desired.

Function: mental_exercise(break_type: str) -> str
Parameters:
break_type (str): The type of mental break (options: 'focus', 'creativity', 'mindfulness')
Returns: A string describing a mental exercise suggestion for the specified type.
Example Usage:
```
from codebreak.mental_exercises import mental_exercise

# Get a mental exercise suggestion for creativity
print(mental_exercise("creativity"))
```
3. Physical Exercise (Exercise class)
The Exercise class provides instructions for a physical exercise, allowing different intensity levels.

Class: Exercise
Methods:
get_name(): Returns the exercise name as a string.
output(intensity: str): Prints instructions for the exercise based on the specified intensity ('low', 'medium', or 'high').
Example Usage:

```
from codebreak.physical_exercise import Exercise

# Create an instance of the Exercise class for jogging
jogging = Exercise("Jogging", "5 minutes", "10 minutes", "15 minutes", "Cardio")

# Print a high-intensity exercise suggestion
jogging.output("high")
```

4. Stretch Exercise (stretch_exercise function)
Suggests a stretch exercise based on the available time in minutes.

Function: stretch_exercise(minutes: int) -> str
Parameters:
minutes (int): Available time for stretching (between 1 and 15 minutes)
Returns: A string describing a stretching exercise suggestion for the specified duration.
Example Usage:
```
from codebreak.stretches import stretch_exercise

# Get a 5-minute stretching exercise suggestion
print(stretch_exercise(5))
```
Step 3: Example Program
To see all functions in action, try running the [example program] (https://github.com/software-students-fall2024/3-python-package-the-fixers/blob/main/example_program.py) on GitHub. This example demonstrates each function in the package and shows how to use them in a Python script.

Here’s an overview of the example_program.py file:

```
from codebreak.eye_exercises import eye_exercise
from codebreak.mental_exercises import mental_exercise
from codebreak.physical_exercise import Exercise
from codebreak.stretches import stretch_exercise

# Example usage of eye exercise function
print("Eye Exercise:", eye_exercise(10))

# Example usage of mental exercise function
print("Mental Exercise:", mental_exercise("creativity"))

# Example usage of Exercise class
jogging = Exercise("Jogging", "5 minutes", "10 minutes", "15 minutes", "Cardio")
jogging.output("medium")

# Example usage of stretch exercise function
print("Stretch Exercise:", stretch_exercise(8))
```

## Developer Contributions
how a developer who wants to contribute to your project can set up the virtual environment, install dependencies, and build and test your package for themselves.
###Fork and Clone the Repository

Fork the repository on github. The repository can be cloned with the command 
git clone https://github.com/software-students-fall2024/3-python-package-the-fixers.git

### Setting up a virtual environment 
The virtual environment pipenv can be installed with the command
``` 
pip install pipenv
``` 

To activate the environment, run
``` 
pipenv shell
``` 

### Installing dependencies

To install pytest, run the commands
``` 
pipenv install pytest
``` 
``` 
pipenv install random
``` 

In the pipenv environment, run to install all dependencies. The Pipfile can alternatively used.
``` 
pipenv install -r requirements.txt
``` 

### Build the package 
If you haven’t already installed build then run the command
``` 
pip install build 
``` 
To build the package run the command 
``` 
python -m build
``` 
Make changes on the local repository on a new branch using the command
``` 
git checkout -b feature/your-feature-name
``` 
Stage changes, commit the changes, and push the changes to the forked repository on Github. It is important to note that to prevent merge conflicts, git pull is always recommended before pushing any changes. 
``` 
git add .
git commit -m "Add description of your changes"
git push origin branch-name
``` 
Go to the forked repository on GitHub and create a pull request for the branch that was just pushed. Select ‘Compare & pull request.’ and submit the pull request to the original repository. 

## Teammates 
[Nick Burwell](https://github.com/nickburwell)
[Finn Eskeland](https://github.com/finn1003)
[Jessie Kim](https://github.com/jessiekim0)
[Dasha Miroshnichenko](https://github.com/dm5198)

## Configuration 
instructions for how to configure and run all parts of your project for any developer on any platform - these instructions must work!
Mac
Windows
Linux 

Prerequisites
Python: Ensure you have Python 3.8 or higher installed. You can check your Python version with:
```
python --version
```
or, on some systems:

```
python3 --version
```
Mac: Install Python via Homebrew:

```
brew install python
```
Windows: Download Python from python.org and follow the installation instructions. Make sure to check "Add Python to PATH" during installation.

Linux: Python is often pre-installed. If not, install it via the package manager:
```
sudo apt update
sudo apt install python3
```
Git: Install Git to clone the repository.

Mac: Install via Homebrew:
```
brew install git
```
Windows: Download from git-scm.com and follow the installer instructions.
Linux: Install via your package manager:

```
sudo apt install git
```
pipenv: Install pipenv to manage dependencies.

```
pip install pipenv
```

Step 1: Clone the Repository
In your terminal or command prompt, clone the repository:
```
git clone https://github.com/your-username/3-python-package-the-fixers.git
cd 3-python-package-the-fixers
```
Replace your-username with your actual GitHub username.

Step 2: Set Up Virtual Environment and Install Dependencies
Create and activate a virtual environment using pipenv:

```
pipenv install --dev
```
This will install the required packages from the Pipfile.

Activate the virtual environment:
```
pipenv shell
```
Note: If you encounter issues with pipenv, you can alternatively create a virtual environment manually and install dependencies from requirements.txt (if you generate it) or directly from Pipfile requirements.

Step 3: Run the Project
With the virtual environment activated, you can now run the project.

Running the example program:
```
python example_program.py
```
This program demonstrates how to use each function in the CodeBreak package.

Running the package interactively: You can also open a Python interpreter and import the package to explore it interactively:
```
>>> from codebreak.eye_exercises import eye_exercise
>>> print(eye_exercise(10))
```
Step 4: Run Tests
The CodeBreak project uses pytest for testing. To run all tests, ensure you’re in the project’s root directory, then run:
```
pytest
```
If everything is set up correctly, you should see output indicating that all tests have passed.

Platform-Specific Notes
Mac
Ensure Homebrew is installed to easily install Python and Git. Use brew install package_name for installing dependencies.
Activate virtual environments with source venv/bin/activate if using a manual virtual environment setup.
Windows
Use pipenv shell to activate the pipenv environment.
If you encounter issues with pipenv, run python -m venv venv and activate the environment using .\venv\Scripts\activate.
You may need to install the python command alias for compatibility with some scripts.
Linux
Most Linux distributions come with Python pre-installed.
Use sudo apt install package_name (Debian-based) or sudo yum install package_name (Red Hat-based) to install Git, Python, or other dependencies.
Troubleshooting
Virtual Environment Issues: If you encounter issues with pipenv, try updating it or using a manual virtual environment as described above.

Dependency Issues: Ensure all dependencies are installed. If there’s an issue, try reinstalling with:
```
pipenv install --dev
```
Environment Variables: Missing environment variables may cause runtime errors. Double-check that your .env file is correctly set up.

## Other
instructions for how to set up any environment variables and import any starter data into the database, as necessary, for the system to operate correctly when run.
if there are any "secret" configuration files, such as .env or similar files, that are not included in the version control repository, exact instructions for how to create them and what their contents should be must be supplied to the course admins by the due date.
