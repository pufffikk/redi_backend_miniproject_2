import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app


# Initialize TestClient
client = TestClient(app)


# 1. Test for /api/countries route
def test_get_countries():
    # Mock response for the RESTCOUNTRIES API
    mock_countries_data = [
        {"name": {"common": "Finland"}, "capital": ["Helsinki"], "region": "Europe",
         "population": 5, "latlng": [29.37, 47.97]},
        {"name": {"common": "Kenya"}, "capital": ["Nairobi"], "region": "Africa",
         "population": 5, "latlng": [29.37, 47.97]},
    ]
    with patch("main.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_countries_data

        response = client.get("/api/countries")

        assert response.status_code == 200
        assert "Finland" in response.text
        assert "Nairobi" in response.text  # Check if 'Nairobi' appears in the response


# Test for /api/countries/{name}/capital/weather route
def test_get_country_weather():
    # Write your test logic here
    mock_weather_data = [
        {"current_weather": {"temperature": 13.1, "windspeed": 13.1}}
    ]
    with patch("main.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_weather_data

        response = client.get("/api/countries/Dublin/weather")

        assert response.status_code == 200
        assert "Finland" in response.text
        assert "Nairobi" in response.text
    pass

# Test case for country not found (404 error handling)
def test_country_not_found():
    # Write your test logic here
    pass


## Try writing some integration tests, where the actual third party APIs are called

# Test case for handling errors from the RESTCOUNTRIES API
def test_restcountries_api_error():
    # Write your test logic here
    pass

# Test case for handling errors from the Open Meteo API
def test_open_meteo_api_error():
    # Write your test logic here
    pass
