# Funky Fortune

This package is designed for those who enjoy divination and fortune telling. Tools include a magic eight ball, fortune cookies, zodiac fortunes, and more!

## Installation/Usage

You can install this package using a virtual environment of your choice.

Using venv:
```
pip install funky-fortune
```
Using pipenv:
```
pipenv shell
pipenv install funky-fortune
```

Then, import the package in your program:
```
import funky_fortune.main as ff
```

### The functions currently implemented are listed below:

`zodiac_fortune(zodiac_sign)`

Takes a str as an argument, returns a str. If the string passed in corresponds to a zodiac sign, the fortune returned will be unique to that sign.

`lucky_number(name)`

Takes a str as an argument, returns an int. If the same name is passed in, the lucky number will stay the same.

`fortune_cookie(lucky=False)`

Returns a string. If the lucky parameter is passed in, the resulting fortune will be extra lucky!

`magic_8ball(question)`

Takes a str as an argument, returns a str. The magic eight ball will repeat the question, and return a random answer.

Here is an example of these functions being used: [Example Code](https://github.com/software-students-fall2024/3-python-package-bug-creator-v3/blob/main/example.py)
## Open Source Contributions:

If you want to add to this package, fork this repository: [Github Link](https://github.com/software-students-fall2024/3-python-package-bug-creator-v3/tree/main)

Then, set up the virtual environment using pipenv and install dependencies:

```
pipenv shell
pipenv install
```
Then, you are free to make changes to the package. Functions are found in the `main.py` folder of the `funky_fortune` directory.

Once done, run tests with the simple command `pytest`. Additionally, you can add tests of your own under the `tests` directory.

You can also build the package by running `python -m build` in the home directory to see if the package works as intended. Artifacts should be found in the newly created `dist/` folder.

If you are happy with your changes, you can commit them and send a pull request!

## Contributors:

[**Bowen Ma**](https://github.com/mabowen1013)

[**Hanlin He**](https://github.com/Alpha-He)

[**Junqi Zhao**](https://github.com/JunqiZhao888)

[**Andrew Qin**](https://github.com/Andrewqin1)
