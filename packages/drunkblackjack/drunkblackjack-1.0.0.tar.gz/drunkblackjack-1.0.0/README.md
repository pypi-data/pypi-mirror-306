[![CI / CD](https://github.com/software-students-fall2024/3-python-package-swe-switching-with-econ/actions/workflows/build.yml/badge.svg)](https://github.com/software-students-fall2024/3-python-package-swe-switching-with-econ/actions/workflows/build.yml)

# Drunk Blackjack

## Overview

A lighthearted blackjack python package that gives you the option to get "drunk" and see how it affects your play, as well as get commentary on your actions and get good or bad advice on gambling. Warning: don't drink like this in real life!

## PyPI Link

## How to Play Blackjack
The goal of blackjack is to beat the dealer by getting a card total as close to 21 as possible without going over. You can "hit" to get another card or "stand" to keep your current cards as is. Whoever is closest to 21 wins, but if you get over 21, you bust and lose. 

## Installation

## Usage
### Import the package

```python
from drunkblackjack import module
```

### Functions

#### Function 1: Start the game
`start_game(bet_amount)`

Start a game of blackjack, which will be played on the command line. Takes an amount to bet as an argument.

Example:
```python
module.start_game(100)
```

#### Function 2: Take shots
`take_shots(number_of_shots)`

Take some shots, specifying the number as an argument.  The more shots you take, the drunker you get, and if you get too drunk, your blackjack gameplay will be affected. Returns a message about how drunk you are.

Example:
```python
print(module.take_shots(5))
```

#### Function 3: Get advice
`get_advice(advice_type)`

Get advice on gambling. Takes 'good' or 'bad' as an argument, for good or bad advice respectively.

Example:
```python
print(module.get_advice('bad'))
```

#### Function 4: Get commentary
`get_commentary(action)`

Get commentary on various blackjack actions ('hit', 'stand', or 'bust'). Changes depending on how drunk you are.

Example:
```python
print(module.get_commentary('hit'))
```

See the [example program](https://github.com/software-students-fall2024/3-python-package-swe-switching-with-econ/blob/main/example_program.py) for more.

## Contribution Instructions

1. Clone the repo
```
git clone https://github.com/software-students-fall2024/3-python-package-swe-switching-with-econ.git
```

2. Install and activate `pipenv`
```bash
pip install pipenv
pipenv shell
```

3. Build the project

```
python -m build
```

4. Test with `pytest`
```
pytest
```

## Configuring and Running

## Team

- [Terry](https://github.com/cao-exe)
- [William](https://github.com/FriedBananaBan)
- [Leanne](https://github.com/leannelu)
- [Sam](https://github.com/stango1234556)
