# Pymagotchi

![Workflow log](https://github.com/software-students-fall2024/3-python-package-book-of-amos-1/actions/workflows/event-logger.yml/badge.svg)

A Python-based virtual pet simulation package with customizable care and stats tracking.

## Features

- **Feed** your pet to keep it from getting hungry.
- **Play** with your pet to keep it happy.
- **Rest** your pet to give it energy.
- **Track** your pet's stats (hunger, happiness, energy, and health).
- **Time-based simulation**: Pet stats update over time, requiring regular care.

## Links
* PyPI page: https://pypi.org/project/pymagotchi
* GitHub repo: https://github.com/software-students-fall2024/3-python-package-book-of-amos-1

## Installation

Install pymagotchi via pip:

```bash
pip install pymagotchi
```

## Usage
Once installed, you can run pymagotchi from the terminal to start the game.
```bash
python -m pymagotchi
```
Alternatively, you can create and interact with your pymagotchi pet within your python code.
```python
from pymagotchi import Pet

# Create a new pet
my_pet = Pet.new_pet()

# Display the pet's stats
my_pet.status()

# Interact with the pet
my_pet.feed(amount=1)
my_pet.play(duration=5)
my_pet.sleep(duration=10)
my_pet.rename(new_name='new name')

# Display ascii representation of pet
my_pet.display()
```
## Documentation

Pet Class

*	Pet(name=None, timeframe=DEFAULT_TIMEFRAME, immortal=False): Initializes a pet with a name, timeframe (rate of stat depletion), and immortality setting.
*	feed(amount): Increases the pet’s food level by the specified amount.
*	play(duration): Increases the pet’s happiness by the specified duration.
*	sleep(duration): Increases the pet’s sleep level by the specified duration.
*	rename(new_name): Changes the pet’s name to new_name.
*	update_stats(): Updates the pet’s stats based on time elapsed.
*	display_art(): Shows the pet’s mood as ASCII art.

generate_name()

*	Generates and returns a random pet name.

For more details, you can view the [`__main__.py`](https://github.com/software-students-fall2024/3-python-package-book-of-amos-1/blob/pypi-uploading/pymagotchi/__main__.py) file, which contains the full example code.

## Pet Commands

* Feed
* Sleep
* Play
* Rename

## Requirements
Python 3.7 or higher.

## Contributing

To contribute to PyMagotchi:

1.	Clone the Repository: 
```bash
git clone https://github.com/software-students-fall2024/3-python-package-book-of-amos-1.git
cd 3-python-package-book-of-amos-1
```
2.	Set Up a Virtual Environment:
Use pipenv to set up the environment:
```bash
pipenv install --dev
pipenv shell
```
3.	Build and Test:
Run the following to build and test the package:
```bash
python -m build
pipenv run pytest
```

## Authors
Team : Book of Amos

* https://github.com/bairixie 
* https://github.com/dm6288
* https://github.com/naruminato1
* https://github.com/simesherbs

## Configuration and Setup Instructions
Run the Project

1.	Install Dependencies: 
```bash
pip install pymagotchi 
 ``` 
or clone the repository and set up the development environment as shown above.

2.	Run the Interactive Pet Simulation:
```bash
pymagotchi
```

## License
This project is licensed under the GNU General Public License. See the LICENSE file for details.