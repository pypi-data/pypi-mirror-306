![Build & Test](https://github.com/software-students-fall2024/3-python-package-financeeers/actions/workflows/python-package.yml/badge.svg)

# Brainrot-Stocks


An exercise to create a Python package, build it, test it, distribute it, and use it. See [instructions](./instructions.md) for details.

This package was created by generally following the [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/) with the addition of some pipenv setup to manage [virtual environments](https://packaging.python.org/en/latest/tutorials/managing-dependencies/).

## Project Description

Finance is boring and you hate crunching numbers all day? No problem, **Brainrot-Stocks** is a Python package designed for handling financial data while keeping you entertained with a constant stream of brainrot. It includes modules for managing stock quotes, performing various operations on financial data, and engaging learning experiences. Powered by [AlphaVantage API.](https://www.alphavantage.co/documentation/) 

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

## Usage
See the example usage Python program to see all the functions in action [here.](https://github.com/software-students-fall2023/3-python-package-exercise-team1-pt3/blob/main/example-program.py)

### Stock Class
   ```python
    from Financiers.stock import Stock
    stock = Stock()
   ```
  *  **Description:** The Financiers module contains a class called ```Stock``` that contains functions which access data from [AlphaVantage's API](https://www.alphavantage.co/documentation/) for your Python programs. To do this, import ```Stock``` and create an instance of it.
#### 1. `get_market_mood()`
   ```python
   stock = Stock()
   mood = stock.get_market_mood()
   ```
   - **Description:** Provides a random statement about the current stock market’s vibe, referencing top gainers and losers.

#### 2. `get_earnings(symbol_string, annual=True, numDays=5)`
   ```python
   earnings_df = stock.get_earnings("AAPL", annual=True, numDays=5)
   ```
   - **Arguments:**
     - `symbol_string` (str): Ticker symbol of the stock (e.g., `"AAPL"`).
     - `annual` (bool): If `True`, retrieves annual earnings; if `False`, retrieves quarterly earnings.
     - `numDays` (int): Number of recent entries to return.
   - **Returns:** `BrainrotDataFrame` with a random brainrot quote and a DataFrame of earnings data.

#### 3. `get_price_data(symbol_string)`
   ```python
   price_data = stock.get_price_data("AAPL")
   ```
   - **Arguments:**
     - `symbol_string` (str): Ticker symbol of the stock.
   - **Returns:** `BrainrotDataFrame` with the stock's historical price data.

#### 4. `forecast_prices(symbol_string, days=30)`
   ```python
   forecast_df = stock.forecast_prices("AAPL", days=30)
   ```
   - **Arguments:**
     - `symbol_string` (str): Ticker symbol of the stock.
     - `days` (int): Number of future days to forecast.
   - **Returns:** `BrainrotDataFrame` with forecasted dates and predicted prices.

#### 5. `company_overview(symbol_string)`
   ```python
   overview = stock.company_overview("AAPL")
   ```
   - **Arguments:**
     - `symbol_string` (str): Ticker symbol of the company.
   - **Returns:** `BrainrotWrapper` with a `Company` object containing information about the company.

#### 6. `plot_top_movers(symbols)`
   ```python
   top_movers_df = stock.plot_top_movers(["AAPL", "GOOGL", "TSLA"])
   ```
   - **Arguments:**
     - `symbols` (list): List of stock ticker symbols.
   - **Returns:** `BrainrotDataFrame` with information on the top gainer and loser from the provided symbols. Generates plots for visual analysis.

#### 7. `project_future_estimates(symbols, days=30, pattern="neutral")`
   ```python
   estimates_df = stock.project_future_estimates(["AAPL", "GOOGL"], days=30, pattern="bullish")
   ```
   - **Arguments:**
     - `symbols` (list): List of stock ticker symbols.
     - `days` (int): Number of days to forecast.
     - `pattern` (str): Trend pattern (`"bullish"`, `"bearish"`, or `"neutral"`).
   - **Returns:** `BrainrotDataFrame` with forecasted prices for each symbol in the list.

#### 8. `calculate_atr(data, window=14)`
   ```python
   atr = stock.calculate_atr(data, window=14)
   ```
   - **Arguments:**
     - `data` (DataFrame): DataFrame containing columns `'high'`, `'low'`, and `'close'`.
     - `window` (int): Period to calculate the Average True Range (default is 14).
   - **Returns:** `pd.Series` with ATR values.

---

### Company Class

#### 1. `forecast_by_date_range(date_range="last_month", days_to_forecast=30, model_type="linear", confidence_level=0.95, frequency="daily", return_format="dataframe")`
   ```python
   forecast = company.forecast_by_date_range(date_range="last_year", days_to_forecast=30, model_type="random_walk")
   ```
   - **Arguments:**
     - `date_range` (str): Specifies the historical range for data (`"last_day"`, `"last_month"`, `"last_year"`).
     - `days_to_forecast` (int): Number of days to forecast.
     - `model_type` (str): Forecasting model (`"linear"`, `"random_walk"`).
     - `confidence_level` (float): Confidence level for forecast intervals.
     - `frequency` (str): Frequency of forecasted data (`"daily"`, `"weekly"`, `"monthly"`).
     - `return_format` (str): Format of the return data (`"dataframe"`, `"json"`).
   - **Returns:** `BrainrotDataFrame` or JSON with forecasted dates, prices, and confidence intervals (if applicable).

### BrainrotDataFrame and BrainrotWrapper Classes

These classes are designed to wrap data in a custom way, displaying both the data and a randomly selected "brainrot" quote for humorous effect. Each can be instantiated directly or will be returned by functions within the `Stock` and `Company` classes.


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
