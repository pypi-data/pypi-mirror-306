import pytest
import pandas as pd
from src.Financiers.stock import Stock, Company, BrainrotDataFrame, BrainrotWrapper
from datetime import datetime, timedelta

class MockResponse:
    def __init__(self, status_code, json={}):
        self.status_code = status_code
        self.result_json = json
    def json(self):
        return self.result_json

class Tests:
    
    def test_sanity_check(self):
        """
        Test debugging... making sure that we can run a simple test that always passes.
        From the main project directory, run the `python -m pytest -s` command to run all tests with print statements (-s) if u include them
        """
        expected = True
        actual = True
        assert actual == expected, "Expected True to be True!"
        
    def test_get_earnings(self):
        print("\n Testing get_earnings() with IBM")
        stock = Stock()
        earnings = stock.get_earnings("IBM")
        
        # assert df has correct columns
        expected_columns = ['date', 'reportedEPS', 'type']
        assert list(earnings.df.columns) == expected_columns, "DataFrame columns do not match expected columns"
        
        # checkign df is not empty
        assert not earnings.df.empty, "Earnings DataFrame is empty, but it was expected to contain data"

    # def test_forecast_prices(self, monkeypatch):
    #     print("\nTesting forecast_prices() with mock data")

    #     # Mock get_price_data to return sample historical data
    #     def mock_get_price_data(symbol_string):
    #         mock_price_data = pd.DataFrame({
    #             'date': pd.date_range(start="2023-01-01", periods=10, freq="D"),
    #             'price': [100.0 + i for i in range(10)]  # increasing mock prices
    #         })
    #         return BrainrotDataFrame("Mock data", mock_price_data)
        
    #     # Apply monkeypatch to replace get_price_data method
    #     stock = Stock()
    #     monkeypatch.setattr(stock, "get_price_data", mock_get_price_data)

    #     # Act: Call the forecast_prices function
    #     days_to_forecast = 5
    #     forecast = stock.forecast_prices("IBM", days=days_to_forecast)

    #     # Assert: Check if the returned BrainrotDataFrame has expected structure
    #     assert forecast.df is not None, "Forecast DataFrame should not be None"
    #     assert 'date' in forecast.df.columns, "'date' column missing from forecast DataFrame"
    #     assert 'predicted_price' in forecast.df.columns, "'predicted_price' column missing from forecast DataFrame"
        
    #     # Check if the correct number of forecasted rows is generated
    #     assert len(forecast.df) == days_to_forecast, f"Expected {days_to_forecast} rows in forecast DataFrame, but got {len(forecast.df)}"
        
    #     # Validate that forecasted dates start the day after the latest historical date
    #     expected_start_date = mock_get_price_data("IBM").df['date'].max() + timedelta(days=1)
    #     actual_start_date = forecast.df['date'].min()
    #     assert actual_start_date == expected_start_date, f"Expected start date {expected_start_date}, but got {actual_start_date}"

    #     # Verify that all predicted prices are within the mocked range (100, 150)
    #     assert forecast.df['predicted_price'].between(100, 150).all(), "Predicted prices are not within the expected range (100, 150)"
        
    ## company_overview ##
    # Test 1: No symbol provided
    def test_company_overview_no_symbol(self, capsys):
        stock = Stock()
        result = stock.company_overview("")
        assert result is None, "Expected None when no symbol is provided."
        captured = capsys.readouterr()
        assert "Error: No symbol provided." in captured.out, "Expected appropriate error message printed."

    # Test 2: Invalid symbol (symbol with no data)
    def test_company_overview_invalid_symbol(self,capsys,monkeypatch):
        test_symbol = 'INVALID_SYMBOL'
        def mock_get(url):
            return MockResponse(200)
        
        monkeypatch.setattr("requests.get", mock_get)
        
        stock = Stock()
        result = stock.company_overview(test_symbol)
        
        assert result is None, "Expected None when an invalid symbol is provided."
        
        captured = capsys.readouterr()
        assert f"Error: No data found for symbol '{test_symbol}'. Please check if the symbol is correct." in captured.out, "Expected appropriate error message printed."

    # Test 3: Valid symbol with successful response
    def test_company_overview_valid_symbol(self,monkeypatch):
        test_symbol = "AAPL"
        SAMPLE_OVERVIEW_JSON = {
                        "Symbol": "AAPL",
                        "Name": "Apple Inc.",
                        "Description": "Apple designs and sells electronics and software.",
                        "CIK": "51140",
                        "Country": "USA",
                        "Sector": "Technology",
                        "Industry": "Consumer Electronics"
                    }
        def mock_get(url):
            return MockResponse(200, SAMPLE_OVERVIEW_JSON)

        monkeypatch.setattr("requests.get", mock_get)
        
        # Mock random.choice
        monkeypatch.setattr("random.choice", lambda _: "Invest in {stock}? Fam, that’s more sus than Freddy Fazbear at 3 AM 💀💀💀.")
        
        stock = Stock()
        result = stock.company_overview(test_symbol)
        
        assert isinstance(result, BrainrotWrapper), "Expected BrainrotWrapper object."
        assert result.quote == f"Invest in {test_symbol}? Fam, that’s more sus than Freddy Fazbear at 3 AM 💀💀💀.", "Brainrot quote did not match."
        assert isinstance(result.object, Company), "Expected a Company object in BrainrotWrapper."
        assert result.object.symbol == SAMPLE_OVERVIEW_JSON["Symbol"]
        assert result.object.name == SAMPLE_OVERVIEW_JSON["Name"]
        assert result.object.description == SAMPLE_OVERVIEW_JSON["Description"]
        assert result.object.CIK == SAMPLE_OVERVIEW_JSON["CIK"]
        assert result.object.country == SAMPLE_OVERVIEW_JSON["Country"]
        assert result.object.sector == SAMPLE_OVERVIEW_JSON["Sector"]
        assert result.object.industry == SAMPLE_OVERVIEW_JSON["Industry"]