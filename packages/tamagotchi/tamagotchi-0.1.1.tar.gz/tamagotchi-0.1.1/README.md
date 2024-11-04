![workflow](https://github.com/software-students-fall2024/3-python-package-macaron-for-three/actions/workflows/event-logger.yml/badge.svg)
![workflow](https://github.com/software-students-fall2024/3-python-package-macaron-for-three/actions/workflows/python-package.yml/badge.svg)

# Tamagotchi

## Description

**Tamagotchi** is a Python package where you care for your pixelated pet in pure text form while you code! This package allows users to care for an ASCII-rendered pet by feeding, patting, and customizing its environment. This project includes modules for user interaction, ASCII art conversion, and an engaging game interface.

Find us on PyPI [here](https://pypi.org/project/tamagotchi/).

## Usage

### Importing the Tamagotchi Class

To use the Tamagotchi class

`from tamagotchi import Tamagotchi`

### Class Initialization

`tamagotchi = Tamagotchi()`

Creates a new Tamagotchi instance with default attributes, including a blank name, a white background, and a default food item (apple).

### Methods

**#### `run_game()`**

The primary method to initialize and run the Tamagotchi game. This method launches the tkinter interface to input the pet's name and start interactions.

`tamagotchi.run_game()`

---

#### **`get_pet(number)`**

Retrieves an ASCII representation of a specific pet based on the input number. This function reads from a text file, which should be named `tama-<number>.txt`.

* **Parameters:**
  * `number` (*int* ): Identifier for the pet image file.
* **Returns** : ASCII string of the pet image or`None` if not found.

`tamagotchi.getpet(1)`

---

#### `get_ascii_art(image_path, scale=0.1, character_map=G_SCALE_1)`

Converts an image into ASCII art based on grayscale values.

* **Parameters:**
  * `image_path` (*str* ): Path to the image file.
  * `scale` (*float* ): Scale factor for resizing the image.
  * `character_map` (*str* ): Characters to map grayscale values for ASCII art.
* **Returns** : ASCII art string or`None` if image not found.

`ascii_art = tamagotchi.get_ascii_art("path/to/image.jpg")`

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

`tamagotchi.change_background_color("lightblue")`

---

#### `feed(food)`

Simulates feeding the Tamagotchi with a specified food item.

* **Parameters:**
  * `food` (*str*): Name of the food.

`tamagotchi.feed("banana")`

---

#### `pat(times)`

Simulates patting the pet a specified number of times.

* **Parameters:**
  * `times` (*int*): Number of pats.

`tamagotchi.pat(3)`

---

### Example

Find an example project that shows how to use each function [here]().

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

// to build:
pip install build
python -m build

// install built package for testing
pip install dist/*.whl 

// to test
pytest

```

## To Use and Run

```
pip install tamagotchi
tamagotchi
```

***Note:** to upload an image, make sure your file is in the same directory you install this package in.*

## Teammates

[Hang Yin](https://github.com/Popilopi168)

[Sahar Bueno-Abdala](https://github.com/saharbueno)

[Jessica Xu](https://github.com/Jessicakk0711)
