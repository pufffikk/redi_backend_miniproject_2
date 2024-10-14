from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests

app = FastAPI()

# External API URLs
RESTCOUNTRIES_URL = "https://studies.cs.helsinki.fi/restcountries/api/"
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

# Jinja2 templates location
templates = Jinja2Templates(directory="templates")

# Models
class Country(BaseModel):
    name: str
    capital: str
    region: str

class WeatherInfo(BaseModel):
    temperature: float
    wind_speed: float

# Routes

# Root URL
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

# GET /api/countries
@app.get("/api/countries", response_model=list[Country])
def get_countries(request: Request):
    response = requests.get(RESTCOUNTRIES_URL + "all")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetching country data")
    countries_data = response.json()
    countries = [
        Country(name=c["name"]["common"], capital=c.get("capital", ["N/A"])[0], region=c["region"]) for c in countries_data
    ]
    # Render the HTML template with countries data
    return templates.TemplateResponse(request, "countries.html", {"countries": countries})

# GET /api/countries/{name}/capital/weather
@app.get("/api/countries/{name}/capital/weather", response_model=WeatherInfo)
def get_country_weather(request: Request, name: str):
    response = requests.get(RESTCOUNTRIES_URL + "name/" + name)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetching country data")
    country_data = response.json()
    lat, lon = country_data["capitalInfo"]["latlng"]
    capital = country_data["capital"][0]
    response = requests.get(
        f"{OPEN_METEO_URL}?latitude={lat}&longitude={lon}&current_weather=true"
    )
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Error fetching weather data")
    weather_data = response.json()["current_weather"]
    return templates.TemplateResponse(request, "weather.html", {
        "capital": capital,
        "country_name": name,
        "weather": {
            "temperature": weather_data["temperature"],
            "wind_speed": weather_data["windspeed"]
        }
    })
