# Welcome to PyMovies!

![example workflow](https://github.com/software-students-fall2024/3-python-package-three/actions/workflows/event-logger.yml/badge.svg)

## Authors
[Fatima Villena](https://github.com/favils)

[Safia Billah](https://github.com/safiabillah)

[Sandy Li](https://github.com/vernairesl)

[May Zhou](https://github.com/zz4206)

## Description
[Link to Package](https://pypi.org/project/pymovies)

## Installation

To install the `pymovies` package from PyPI, run the following command in your terminal.  (NOTE: pip and python must be installed):

    ```bash
    pip install pymovies
    ```

To run the package:
    ```base
    python -m pymovies
    ```

The terminal will instruct you from there!

You are able to run four functions:
- list all movies
- get a random quote
- get the quote of the day
- get a quote from a particular movie!

## Run Tests
1. **Clone the repository**

2. **Make sure pipenv installed:**
    ```bash
    pip install pipenv
    ```

3. **Activate the virtual environment:**
    ```bash
    pipenv shell
    pipenv install --dev
    ```

4. **Run Tests:**
    ```bash
    python -m pytest tests/TESTFILENAMEHERE.py
    ```