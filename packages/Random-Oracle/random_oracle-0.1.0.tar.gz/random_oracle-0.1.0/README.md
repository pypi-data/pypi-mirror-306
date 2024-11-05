# Python Package Exercise

Built Oracle, a prophet that can do multiple things, including spit fortunes (fortune cookie),
output a random decision (8ball), give a quick, random mood (vibe check), and output a random 
pet (petting zoo). 

## Badge
![Python build & test](https://github.com/software-students-fall2024/3-python-package-burger-flippers/actions/workflows/event-logger.yml/badge.svg)

## [Link to Package Page](https://test.pypi.org/project/Oracle/0.1.0/)

## Team Members
[Christopher Li](https://github.com/christopherlii), [Julie Chen](https://github.com/Julie-Chen), [Maddy Li](https://github.com/maddy-li), [Aneri Shah](https://github.com/anerivs)

# Using Oracle in Your Project

## Installation

```bash
pip install oracle
```

## Usage

### Running the program

`python oracle/cli.py <function name> <argument(s)>`

### Fortune Cookie

**get_fortune(mood)→str:** accepts a mood and returns a random fortune fitting the corresponding mood

```python
from oracle.fortune_cookie import get_fortune

# Get a fortune based on mood
optimistic_fortune = get_fortune("optimistic")
realistic_fortune = get_fortune("realistic")
unfortunate_fortune = get_fortune("unfortunate")

print(optimistic_fortune)  # Outputs a random optimistic fortune
```

### Magic 8-Ball

**get_eight_ball(num)→str**: accepts a integer and returns the specified number of 8-ball predictions

```python
from oracle.eight_ball import get_eight_ball

# Get a single decision
decision = get_eight_ball(1)

# Get multiple decisions
decisions = get_eight_ball(3)

print(decisions)  # Outputs random decision(s)
```

### Vibe Check

**get_vibe_check(vibes)→str**: accepts a mood and returns a corresponding affirmation

```python
from oracle.vibe_check import get_vibe_check

# Check different vibes
good_vibe = get_vibe_check("good")
bad_vibe = get_vibe_check("bad")
random_vibe = get_vibe_check("random")

print(random_vibe)  # Outputs a random vibe
```

### Petting Zoo

**get_random_pet()→str**: when called, it returns a random ASCII animal

**get_pet(pet)→str**: accepts an animal name, and prints the corresponding ASCII animal if it exists.

```python
from oracle.petting_zoo import get_random_pet, get_pet

# Check different vibes
dog = get_pet("dog")
cat = get_pet("cat")
rabbit = get_pet("rabbit")
hamster = get_pet("hamster")
goat = get_pet("goat")
sheep = get_pet("sheep")
bird = get_pet("bird")
frog = get_pet("frog")
bear = get_pet("bear")
fox = get_pet("fox")

print(fox) #prints fox pet
print(get_random_pet())  # Outputs a random pet
```

## Example Code

See [example.py](https://github.com/software-students-fall2024/3-python-package-burger-flippers/blob/main/example.py) for sample code.

# Contributing to Oracle

### Setting Up Development Environment

1. Ensure you have python 3.11 or higher.
2. Fork and clone the repository:

```bash
git clone https://github.com/software-students-fall2024/3-python-package-burger-flippers
cd 3-python-package-burger-flippers
```

1. Install pipenv if you haven't already:

```bash
pip install pipenv
```

1. Create virtual environment and install dependencies:

```bash
pipenv install --dev
```

1. Activate the virtual environment:

```bash
pipenv shell
```

### Building the Package

Build the package locally:

```bash
python -m build
```

This will create both source distribution and wheel in the `dist/` directory.

### Running Tests

Run the test suite:

```bash
pipenv run pytest
```

### Development Workflow

1. Create a new branch for your feature (change feature-name to your liking):

```bash
git checkout -b feature-name
```

1. Create a new file for your new feature in the oracle folder for your new feature

```bash
touch oracle/new-feature.py
```

1. After coding the new feature, create a test file with corresponding test cases

```bash
touch tests/test-new-feature.py
```

1. Make your changes and write tests
2. Run tests to ensure everything works:

```bash
pipenv run pytest
```

1. Submit a pull request with your changes

## Notes

- No environment variables or database setup is required for this project
- No secret configuration files are needed
- The project uses standard Python packaging tools (setuptools)