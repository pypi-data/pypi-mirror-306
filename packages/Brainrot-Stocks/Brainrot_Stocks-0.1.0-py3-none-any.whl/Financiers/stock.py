import pandas as pd
import requests
from dotenv import load_dotenv
import os
import random
from .quotes import quotes

load_dotenv()


class Stock:
    def __init__(self):
        self.api_key = os.getenv("ALPHAVANTAGE_API_KEY")

    # TODO: add optional argument for quarterly or annual
    def get_earnings(self, symbol_string):
        """
        Retrieves the annual and quarterly earnings (EPS) for the company of interest
        Arguments:
        symbol_string: a string representing the ticker of your choice. For example: symbol=IBM.

        Returns:
        a custom pandas DataFrame BrainrotDataFrame containing a random brainrot quote and a DataFrame with two columns 'date' and 'reportedEPS'
        """
        url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={symbol_string}&apikey={self.api_key}"

        response = requests.get(url)
        data = response.json()

        annualEarnings = pd.DataFrame(
            data["annualEarnings"]
        )  # convert 'annualEarnings' from json (list of dictionaries orignally) into DataFrame
        annualEarnings = annualEarnings[
            ["fiscalDateEnding", "reportedEPS"]
        ]  # select only two columns, fiscalDateEnding and reportedEPS from annualEarnings df
        annualEarnings.columns = [
            "date",
            "reportedEPS",
        ]  # rename the columns for beter readability
        annualEarnings["type"] = (
            "Annual"  # added this to differentiate between quarterly earnings below vvvv
        )

        # and just do the same thing above for below for quarterly earnings cuz the API call happens to return both
        quarterlyEarnings = pd.DataFrame(data["quarterlyEarnings"])
        quarterlyEarnings = quarterlyEarnings[["fiscalDateEnding", "reportedEPS"]]
        quarterlyEarnings.columns = ["date", "reportedEPS"]
        quarterlyEarnings["type"] = "Quarterly"

        earnings_df = pd.concat(
            [annualEarnings, quarterlyEarnings], ignore_index=True
        )  # concat (combine) annual and quarterly earnings into a single df (dataframe)

        earnings_df = earnings_df.sort_values(by="date", ascending=False).reset_index(
            drop=True
        )  # sort df by date (otherwise it wasn't sorted)
        brainrot = random.choice(quotes).replace(
            "{stock}", symbol_string
        )  # get brainrot
        # return the dataframe with brainrot
        return BrainrotDataFrame(brainrot, earnings_df)

    def forecast_prices(self, symbol_string, days=30):
        """
        Forecasts stock prices using a simple model.
        Arguments:
        symbol_string: stock ticker.
        days: how far into the future to forecast (default: 30 days).

        Returns:
        A DataFrame with forecasted dates and predicted prices.
            """
        price_data = self.get_price_data(symbol_string).df
        # Placeholder for ARIMA or similar forecasting model
        forecasted_prices = [random.uniform(100, 150) for _ in range(days)]  # Mock data
        forecast_df = pd.DataFrame({
            'date': pd.date_range(start=price_data['date'].max(), periods=days + 1, freq='D')[1:],
            'predicted_price': forecasted_prices
        })

        brainrot = f"{days}-day forecast for {symbol_string}. Is this sigma behavior?"
        return BrainrotDataFrame(brainrot, forecast_df)
    
    def company_overview(self,symbol_string):
        """
        Provides general company overview
        Arguments:
        symbol_string: stock ticker.

        Returns:
        Returns a Company object with relevant information.
        """
        if not symbol_string:
            print("Error: No symbol provided.")
            return None
        
        url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol_string}&apikey={self.api_key}"
        
        try: 
            response = requests.get(url)
            data = response.json()

            #exception handling
            if not data or "Symbol" not in data:
                print(f"Error: No data found for symbol '{symbol_string}'. Please check if the symbol is correct.")
                return None
        
            companyObj = Company(data)
            
            brainrot = random.choice(quotes).replace(
                "{stock}", symbol_string
            ) 
            
            # return the Company object with brainrot
            return BrainrotWrapper(brainrot, companyObj)
        
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to AlphaVantage API. Check your network connection.")
        except requests.exceptions.Timeout:
            print("Error: The request to AlphaVantage API timed out.")
        except requests.exceptions.RequestException as req_err:
            print(f"An error occurred: {req_err}")
        except ValueError:
            print("Error: Received invalid JSON response from AlphaVantage API.")
        return None
    
class Company:
    def __init__(self, CompanyJsonObj):
        self.symbol = CompanyJsonObj['Symbol']
        self.name = CompanyJsonObj['Name']
        self.description = CompanyJsonObj['Description']
        self.CIK = CompanyJsonObj['CIK']
        self.country = CompanyJsonObj['Country']
        self.sector = CompanyJsonObj['Sector']
        self.industry = CompanyJsonObj['Industry']
        

    def __str__(self):
        return (
            f"Company Information:\n"
            f"Symbol: {self.symbol}\n"
            f"Name: {self.name}\n"
            f"Description: {self.description}\n"
            f"CIK: {self.CIK}\n"
            f"Country: {self.country}\n"
            f"Sector: {self.sector}\n"
            f"Industry: {self.industry}"
        )
        
class BrainrotDataFrame:
    """
    A custom DataFrame wrapper class that adds brainrot quote above the DataFrame output
    """
    def __init__(self, quote, df):
        self.quote = quote
        self.df = df

    def __str__(self):
        return f"{self.quote}\n\n{self.df}"  # have it so the brainrot appears, newline, then the dataframe

    def __repr__(self):
        return self.__str__()

class BrainrotWrapper:
    """
    A custom wrapper class that adds brainrot quote above the original output
    """
    def __init__(self, quote, object):
        self.quote = quote
        self.object = object

    def __str__(self):
        return f"{self.quote}\n\n{self.object}"  # have it so the brainrot appears, newline, then the dataframe

    def __repr__(self):
        return self.__str__()
    

print("Script started.")
print("Processing complete.")

