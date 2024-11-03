![Riddle Handler](https://github.com/software-students-fall2024/3-python-package-codecrafter/actions/workflows/riddle_package.yml/badge.svg)
## Riddle Handler

## Overview

**Riddle Handler** is a lighthearted Python package designed to bring a bit of joy and levity to developers' lives. It provides an interactive experience where users can generate riddles of varying difficulties and topics, check answers, submit new riddles, and receive hints. The package is built following rigorous software engineering practices, ensuring quality and reliability.
## PyPI Link
[Riddle Handler](https://pypi.org/project/riddle-handler/1.0.3/)

## Installation

Install the package via pip:

```bash
pip install riddle-handler==1.0.3
```

## Usage

### Importing the Package

```
import riddle_handler
```

### Functions and Examples

#### Function 1: `generate_riddle(difficulty: int) -> str`

Generates a random riddle based on the specified difficulty level.

- **Parameters:**
  - `difficulty` (int): The difficulty level of the riddle (1 to 4).

- **Returns:**
  - A string containing the riddle's question.

- **Example:**

  ```python
  import riddle_handler

  # Generate a riddle of difficulty level 2
  riddle = riddle_handler.generate_riddle(2)
  print(f"Here's your riddle: {riddle}")
  ```

#### Function 2: `check_answer(riddle_id: int, answer: str) -> str`

Checks if the provided answer to the riddle is correct.

- **Parameters:**
  - `riddle_id` (int): The ID of the riddle.
  - `answer` (str): The user's answer to the riddle.

- **Returns:**
  - A string indicating whether the answer is correct or incorrect.

- **Example:**

  ```python
  import riddle_handler

  # Check the answer to a riddle with ID 5
  result = riddle_handler.check_answer(5, 'shadow')
  print(result)  # Outputs: "Correct answer!" or "Incorrect answer. Try again!"
  ```

#### Function 3: `submit_riddle(riddle: dict) -> str`

Allows users to submit their own riddles to the library.

- **Parameters:**
  - `riddle` (dict): A dictionary containing the riddle's details.

    - `question` (str): The riddle's question.
    - `answer` (list): A list of acceptable answers.
    - `hint` (str): A hint for the riddle.
    - `difficulty` (int): Difficulty level (1 to 4).
    - `topic` (str): The topic of the riddle.

- **Returns:**
  - A string indicating success or an error message.

- **Example:**

  ```python
  import riddle_handler

  # Define your custom riddle
  my_riddle = {
        "question": "I can move, yet I stay in one place; People use me to send messages, but I'm nowhere to be seen; Anytime, anywhere, you can call for me, and I'll always be there. What am I?",
        "answer": ["sound"],
        "hint": "You can hear me but cannot see me.",
        "difficulty": 3,
        "topic": "Communication"
  }

  # Submit the riddle
  response = riddle_handler.submit_riddle(my_riddle)
  print(response)  # Outputs: "Riddle submitted successfully!"
  ```

#### Function 4: `provide_hint(riddle_id: int) -> str`

Provides a hint for the specified riddle.

- **Parameters:**
  - `riddle_id` (int): The ID of the riddle.

- **Returns:**
  - A string containing the hint or an error message.

- **Example:**

  ```python
  import riddle_handler

  # Get a hint for a riddle
  hint = riddle_handler.provide_hint(5)
  print(hint)  # Outputs the hint for the riddle
  ```


_**For more examples, check out** [this example program](https://github.com/software-students-fall2024/3-python-package-codecrafter/blob/main/example_program.py)._

## Contributing

### Setting Up the Development Environment

1. **Clone the repository:**

   ```bash
   git clone https://github.com/software-students-fall2024/3-python-package-codecrafter
   ```

2. **Install `pipenv`:**

If you haven’t installed `pipenv` yet, use the following command:

```bash
pip install pipenv
```

3. **Set Up the Virtual Environment:**

To create a virtual environment and install dependencies using the `Pipfile`, run:

```bash
pipenv install
```

This command will read the `Pipfile` and create a virtual environment with all the specified dependencies.

If you only want to create the environment without installing dependencies, you can use:

```bash
pipenv install --ignore-pipfile
```

4. **Activate the Virtual Environment:**

To activate the virtual environment, use:

```bash
pipenv shell
```

This command works on both Mac and Windows, as `pipenv` will automatically locate and activate the correct environment.

5. **Install Additional Dependencies(If Needed):**

If you need to add more dependencies later, you can use the following commands:

- For production dependencies:

  ```bash
  pipenv install <package-name>
  ```

- For development dependencies (e.g., testing or debugging tools):

  ```bash
  pipenv install --dev <package-name>
  ```

6. **Exit the Virtual Environment:**

To exit the virtual environment, simply type:

```bash
exit
```

Or press `Ctrl + D`.

7. **Remove the Virtual Environmen:**

If you need to delete the virtual environment, use:

```bash
pipenv --rm
```

This will remove the virtual environment associated with the `Pipfile`.


### Building and Testing

- **Run Tests:**

  We use `pytest` for testing.

  ```bash
  pytest
  ```

- **Build Package:**

  Use `build` to create the package artifacts.
  
  For Mac:


  ```bash
  python3 -m build
  ```

  For Windows:


  ```bash
  python -m build
  ```

- **Upload to PyPI (For maintainers):**

  Use `twine` to upload the package.

  ```bash
  twine upload dist/*
  ```

  Note that API key should only be acquired by contacting administrators

### Git Workflow

All code changes must be done in feature branches and not directly in the `main` branch.

To merge code from a feature branch into `main`:

1. **Create a pull request** from the feature branch to `main`.
2. **Request a code review** from a team member.
3. **Review and approve** the code after ensuring all tests pass.
4. **Merge the pull request** into `main`.
5. **Delete the feature branch**.

**Note:** Regularly merge feature branches to avoid merge conflicts.

## Contributors

- [Alex](https://github.com/alexyujiuqiao)
- [Haoyi](https://github.com/hw2782)
- [Keven](https://github.com/BlackCloud-K)
- [Nicole](https://github.com/niki531)

## Instructions for Running the Project

### For Developers

1. **Ensure Python 3.11 or higher is installed** on your system.

2. **Clone the repository and set up the environment** as described in the [Contributing](#contributing) section.

3. **Run the example program:**
  
  For Mac:

   ```bash
   python3 example_program.py
   ```

  For Windows:

   ```bash
   python example_program.py
   ```

### For Users

1. **Install the package via pip:**

   ```bash
   install riddle-handler==1.0.3
   ```

2. **Use the package in your Python scripts** as shown in the [Usage](#usage) examples.

## Configuration and Setup

### Environment Variables

No environment variables are required for basic usage.

### Importing Starter Data

**The package uses a `riddleLibrary.json` file to store riddles. Ensure that this file is in the root directory of your project. You can use our library from [this link](https://github.com/software-students-fall2024/3-python-package-codecrafter/blob/main/riddleLibrary.json) or you can build your own by creating a `riddleLibrary.json` file.**

## Update Log
v1.0.3
Bug Fix: Resolved an issue where the package has no attribute.

v1.0.2
Bug Fix: Resolved an issue where the package appeared empty after installation.
Documentation: Updated README with clearer instructions and added installation and usage details specific to Windows.
Compatibility: Added a method for Windows users to ensure compatibility.

v1.0.1
Updated Package Structure: Reorganized the package structure to follow best practices for module organization, enhancing maintainability and usability.
Bug Fixes: Resolved several issues related to imports and file path references, improving the stability and reliability of the package.

v1.0.0
Initial Release: Launched the riddle_handler package, offering core functionalities for managing and interacting with a JSON-based riddle library. This includes generating riddles, checking answers, providing hints, and submitting new riddles.


