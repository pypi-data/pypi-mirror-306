# Python Package Exercise

An exercise to create a Python package, build it, test it, distribute it, and use it. See [instructions](./instructions.md) for details.

## Team Members

- **Boming Zhang** (bz2196) [GitHub Profile](https://github.com/BomingZhang-coder)
- **Annabeth Gao** (mg6839) [GitHub Profile](https://github.com/bellinimoon)
- **Jack Zhang** (yz6973) [GitHub Profile](https://github.com/yz6973)

## Product Description

**Pytarot** is a lighthearted Python package designed to offer fun and whimsical insights into life’s mysteries. This package includes:
1. **Random Answers of Wisdom**: Provides insightful or humorous responses to user questions.
2. **Daily Action**: Randomly generate positive reminders and suggestions for the day.
3. **True Lover Generator**: Randomly generates a “true lover” profile for fun.
4. **Lucky Day Generator**: Suggests a lucky day in the current month for the user.

## System Setup and Environment Configuration Guide

### Prerequisites
- **Python** (version 3.6 or later)
- **pip** (Python package installer)
- **pipenv** (for managing virtual environments)

### Installation Steps
1. **Clone the Repository**:
   ```shell
   git clone https://github.com/yourusername/pytarot.git
   cd pytarot
   ```

2. **Set Up Virtual Environment with Pipenv**: Initialize a virtual environment and install dependencies in editable mode:

```shell
pipenv install -e .
```

3. **Activate the Virtual Environment**: Start the virtual environment created by `pipenv`:

```shell
pipenv shell
```

4. **Running the Package**  
You can run individual functions directly in the Python interactive shell or use the `main.py` script.

**Running Functions in Python Shell**  
Open the Python shell:

```shell
python
```

5. **Import and test the package functions**:

```python
from src.pytarot import get_answers_of_wisdom, get_lucky_day, get_true_lover

print(answersofwisdom.get_answers_of_wisdom())
print(luckyday.get_lucky_day())
print(truelover.get_true_lover())
print(positive_action.get_positive_message())
```

6. **Running `main.py`**  
Alternatively, you can execute the `main.py` file to run the package as a script:

```shell
python main.py
```

7. **Deactivate the Virtual Environment**  
When you’re done, exit the `pipenv` shell:

```shell
exit
```

8. **How to Run Unit Tests**  
Unit tests are located in the `test` directory and can be run using `pytest`.

**Install pytest** (if not already installed in the virtual environment):

```shell
pipenv install pytest
```

9. **Run Tests**: Run all tests from the main project directory:

```shell
python -m pytest
```

