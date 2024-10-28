import requests
from fastapi import FastAPI, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from pydantic import BaseModel
from functools import lru_cache


templates = Jinja2Templates(directory="templates")

COUNTRIES_API = "https://studies.cs.helsinki.fi/restcountries/api/"
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
SUCCESS_STATUS = 200
app = FastAPI()


class CountryData(BaseModel):
    name: str
    capital: str
    region: str
    population: int
    lat: float
    lng: float


class WeatherData(BaseModel):
    temperature: float
    wind_speed: float


@lru_cache(maxsize=100)
def get_countries_from_external_api():
    return requests.get(COUNTRIES_API + "all")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


@app.get("/api/countries", response_model=list[CountryData])
async def list_countries(request: Request, sort_by: str = "name", order: str = "asc"):
    response = get_countries_from_external_api()
    if response.status_code != SUCCESS_STATUS:
        raise HTTPException(status_code=500, detail="Error retrieving country list")
    countries = [
        CountryData(name=c["name"]["common"],
                    capital=c.get("capital", ["N/A"])[0],
                    region=c["region"],
                    population=c["population"],
                    lat=c["latlng"][0],
                    lng=c["latlng"][1]) for c in
        response.json()
    ]

    reverse = True if order == "desc" else False
    countries = sorted(countries, key=lambda x: getattr(x, sort_by), reverse=reverse)

    return templates.TemplateResponse(request, "countries.html",
                                      {"countries": countries,
                                       "sort_by": sort_by,
                                       "order": order})


@app.get("/api/countries/{capital}/weather")
async def weather_in_capital(request: Request, capital: str, country:str, lat: float, lng: float):
    response = requests.get(f"{OPEN_METEO_URL}?latitude={lat}&longitude={lng}&current_weather=true")
    if response.status_code != SUCCESS_STATUS:
        raise HTTPException(status_code=500,detail="Error retrieving data")
    weather_data = response.json()
    return templates.TemplateResponse(request, "weather.html", {
        "country": country,
        "capital": capital,
        "weather":
            {
                "temperature": weather_data["current_weather"]["temperature"],
                "wind_speed": weather_data["current_weather"]["windspeed"]
            }
    })
