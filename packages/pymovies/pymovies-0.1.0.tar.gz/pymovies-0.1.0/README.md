# Python Package Exercise

An exercise to create a Python package, build it, test it, distribute it, and use it. See [instructions](./instructions.md) for details.

![example workflow](https://github.com/software-students-fall2024/3-python-package-three/actions/workflows/event-logger.yml/badge.svg)

## Teammates
[Fatima Villena](https://github.com/favils)

[Sandy Li](https://github.com/vernairesl)

[Safia Billah](https://github.com/safiabillah)

[May Zhou](https://github.com/zz4206)

## Description
[Link to Package](https://pypi.org/project/pymovies/0.0.9/)

## Installation

To install the `pymovies` package from PyPI, run the following command:

    ```bash
    pip install pymovies
    ```

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