![workflow](https://github.com/software-students-fall2024/3-python-package-macaron-for-three/actions/workflows/event-logger.yml/badge.svg)
![workflow](https://github.com/software-students-fall2024/3-python-package-macaron-for-three/actions/workflows/python-package.yml/badge.svg)

# Tamagotchi

## Description

**Tamagotchi** is a Python package where you care for your pixelated pet in pure text form while you code! This package allows users to care for an ASCII-rendered pet by feeding, patting, and customizing its environment. This project includes modules for user interaction, ASCII art conversion, and an engaging game interface.

Find us on PyPI [here](https://pypi.org/project/tamagotchi/).

## Usage

### Importing the Tamagotchi Class

To use the Tamagotchi class

`from tamagotchi import tamagotchi`

### Class Initialization

`tamagotchi_pet = tamagotchi.tamagotchi()`

Creates a new Tamagotchi instance with default attributes, including a blank name, a white background, and a default food item (apple).

### Methods

#### **`run_game()`**

The primary method to initialize and run the Tamagotchi game. This method launches the tkinter interface to input the pet's name and start interactions.

`tamagotchi_pet.run_game()`

---

#### **`get_pet(number)`**

Retrieves an ASCII representation of a specific pet based on the input number. This function reads from a text file, which should be named `tama-<number>.txt`.

* **Parameters:**
  * `number` (*int* ): Identifier for the pet image file.
* **Returns** : ASCII string of the pet image or`None` if not found.

`tamagotchi_pet.getpet(1)`

---

#### `get_ascii_art(image_path, scale=0.1, character_map=G_SCALE_1)`

Converts an image into ASCII art based on grayscale values.

* **Parameters:**
  * `image_path` (*str* ): Path to the image file.
  * `scale` (*float* ): Scale factor for resizing the image.
  * `character_map` (*str* ): Characters to map grayscale values for ASCII art.
* **Returns** : ASCII art string or`None` if image not found.

`ascii_art = tamagotchi_pet.get_ascii_art("path/to/image.jpg")`

---

#### `start_game()`

Internal function that initializes the game window once the pet name is entered. Should not be called directly but is used in run_game().

---

#### `game_window()`

Internal function to create the main game window where the pet is displayed. Not typically called directly.

---

#### `change_background_color(color)`

Changes the background color of the pet display.

* **Parameters:**
  * `color` (*str*): Background color (e.g., "blue").

`tamagotchi_pet.change_background_color("lightblue")`

---

#### `feed(food)`

Simulates feeding the Tamagotchi with a specified food item.

* **Parameters:**
  * `food` (*str*): Name of the food.

`tamagotchi_pet.feed("banana")`

---

#### `pat(times)`

Simulates patting the pet a specified number of times.

* **Parameters:**
  * `times` (*int*): Number of pats.

`tamagotchi_pet.pat(3)`

---

### Example

```
from tamagotchi import tamagotchi 

tamagotchi_game = tamagotchi.Tamagotchi()
tamagotchi_game.name = 'Fluffy'
print(tamagotchi_game.getpet(1))

# make sure you have a file called input_image.png in the same directory, or make sure you give a correct image path for this function to work

print(tamagotchi_game.get_ascii_art("input_image.png", scale=0.1, character_map=tamagotchi.Tamagotchi.G_SCALE_1))
tamagotchi_game.ascii_art_label = tamagotchi_game.getpet(11)
tamagotchi_game.feed("banana")
tamagotchi_game.change_background_color("blue")
tamagotchi_game.run_game()
```

## Contributing

### Installation

```
pip install pipenv
git clone https://github.com/software-students-fall2024/3-python-package-macaron-for-three.git
cd 3-python-package-macaron-for-three
pipenv install --dev
pipenv shell
pipenv install -e .
python -m pip install --upgrade pip setuptools wheel

# to build:
pip install build
python -m build

# install built package for testing
pip install dist/*.whl 

# to test
pytest

```

## To Use and Run

```
pip install tamagotchi==0.1.2
tamagotchi
```

***Note:** to upload an image, make sure your file is in the same directory you install this package in.*

## Teammates

[Hang Yin](https://github.com/Popilopi168)

[Sahar Bueno-Abdala](https://github.com/saharbueno)

[Jessica Xu](https://github.com/Jessicakk0711)
