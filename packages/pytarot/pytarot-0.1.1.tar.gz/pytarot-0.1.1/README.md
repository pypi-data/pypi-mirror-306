[![Build and Test](https://github.com/software-students-fall2024/3-python-package-itsover/actions/workflows/build-test.yml/badge.svg?branch=main)](https://github.com/software-students-fall2024/3-python-package-itsover/actions/workflows/build-test.yml)
[![log github events](https://github.com/software-students-fall2024/3-python-package-itsover/actions/workflows/event-logger.yml/badge.svg?branch=main)](https://github.com/software-students-fall2024/3-python-package-itsover/actions/workflows/event-logger.yml)

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

## A link to the Pytarot package on PyPI: https://pypi.org/project/pytarot/0.1.0/

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
   from pytarot import get_answers_of_wisdom, get_lucky_day, get_true_lover, get_positive_action

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

## Contributing to Pytarot

We welcome contributions from developers who want to improve Pytarot! Please follow the steps below to set up your development environment.

### Setting Up the Development Environment

1. **Fork the Repository**: First, fork the repository to your GitHub account.

2. **Clone Your Fork**:
   ```shell
   git clone https://github.com/yourusername/pytarot.git
   cd pytarot
   ```
3. **Set Up a Virtual Environment with Pipenv**: Install all dependencies in editable mode:

   ```shell
   pipenv install -e .
   ```

4. **Activate the Virtual Environment**:

   ```shell
   pipenv shell
   ```

5. **Install Development Dependencies**: If there are additional tools like `pytest` for testing, make sure they’re installed:

   ```shell
   pipenv install --dev
   ```

6. **Building and Testing**:To ensure your changes work as expected, please follow these steps:

   **Run Unit Tests**: Make sure all tests pass before submitting a pull request.

   ```shell
   python -m pytest
   ```
   
   **Make Your Changes**: Implement new features or bug fixes in your development branch.

   **Commit and Push Changes**: Use meaningful commit messages.

   ```shell
   git add .
   git commit -m "Description of changes"
   git push origin branch-name
   ```

   **Submit a Pull Request**: Open a pull request on the main repository for review.