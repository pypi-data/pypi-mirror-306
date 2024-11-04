![Build & Test](https://github.com/software-students-fall2024/3-python-package-financeeers/actions/workflows/python-package.yml/badge.svg)

# Brainrot-Stocks


An exercise to create a Python package, build it, test it, distribute it, and use it. See [instructions](./instructions.md) for details.

This package was created by generally following the [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/) with the addition of some pipenv setup to manage [virtual environments](https://packaging.python.org/en/latest/tutorials/managing-dependencies/).

## Project Description

**Brainrot-Stocks** is a Python package designed for handling financial data. It includes modules for managing stock quotes, performing various operations on financial data, and engaging learning experiences.

## Link to Package on PYPI

https://pypi.org/project/Brainrot-Stocks/#description

## Team members

|Reyhan Abdul Quayum|Rashed Alneyadi|Sia Chen|Yu Zhang|Chloe Han|
|:--:|:--:|:--:|:--:|:--:|
|<a href='https://github.com/reyhanquayum'><img src='https://avatars.githubusercontent.com/u/115737572?v=4' width='40px'/></a>|<a href='https://github.com/brshood'><img src='https://avatars.githubusercontent.com/u/133962779?v=4' width='40px'/></a>|<a href='https://github.com/MambiChen'><img src='https://avatars.githubusercontent.com/u/122314736?v=4' width='40px'/></a>|<a href='https://github.com/yz7669'><img src='https://avatars.githubusercontent.com/u/180553323?v=4' width='40px'/></a>|<a href='https://github.com/jh7316'><img src='https://avatars.githubusercontent.com/u/95545960?s=88&v=4' width='40px'/></a>|


## Project Structure


- **src/Financiers**  
  Contains the main modules:
  - `quotes.py`: Handles operations related to stock quotes.
  - `stock.py`: Manages stock data and related functionality.
  
- **tests**  
  Contains test files for validating the code.
  - `test_stock.py`: Tests the `stock.py` module.

## How to install and use this package
Prerequisites: have latest versions of pip and python installed on your environment.

1. Navigate to your project directory.
Create a virtual environment using `pipenv`, and install the latest version of the package with the following command:
 
```bash
pip install pipenv
pipenv install Brainrot-Stocks
```
And before moving onto the next step, activate the virtual environment: 

```bash
pipenv shell
```

2. Import the package using the following command inside the file:
```python
from Financiers.stock import Stock
```
Then, create an instance of Stock class:

```python
stock = Stock()
```

And you're ready to go!
Refer to this [example file](https://github.com/software-students-fall2024/3-python-package-financeeers/blob/main/example_usage.py) to see the example usage of package functions inside the code.

3. Run the program (replace <example_file> with your actual file name):
```bash
python <example_file>.py
```

## Contribute to the project
Prerequisites: have latest versions of pip and python installed on your environment.

### Environment Setup

1. Clone the repository:
  ```bash
  git clone https://github.com/software-students-fall2024/3-python-package-financeeers.git
  cd 3-python-package-financeeers
```

2. Install pipenv:

If `pipenv` has not been installed, install using the following command:
```bash
pip install pipenv
```

3. Create and Activate virtual environment:
```bash
pipenv install
pipenv shell
```

4. Add .env file:
create `.env` file in the root directory of the project, and add the following content:
```python
ALPHAVANTAGE_API_KEY = <api_key>
```
Replace <api_key> with the actual api key, which will be delivered to the admins via discord.

### Make contribution
1. Modify & Run the file:

Make changes you want to make, and run the files. For example, if you want to run stock.py, run the following command:
```bash
python src/Financiers/stock.py
```

### Test & Build
Make sure you are in the virtual environment by running the following command:
```bash
pipenv shell
```
1. Test

Run all unit tests with the following command:
```bash
pytest
```

2. Build

Build the package using the following command:
```bash
python -m build
```
Then, the artifacts will be produced at  `dist/`.

If you want to exit the virtual environment, use this comand:
```bash
exit
```
