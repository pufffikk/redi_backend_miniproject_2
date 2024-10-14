# Redi Backend course Fall 2024 - Mini Project 2

Topic: Extending an stateless API, templating and testing.

The goal of this mini project is to integrate with some third party API's and
serving some static and dynamic websites (HTML) from the backend.

## External APIs

- basic info about countries: https://studies.cs.helsinki.fi/restcountries/
- weather API: https://open-meteo.com/en/docs

### Install packages

```console
$ pip install -r requirements.txt
```

### Run fast api

```console
$ fastapi run main.py
```

### Run tests

```console
$ pytest
```


## Further Ideas

- make sure the countries are displayed in sorted order (by name)
  - add population as a column in the table and add the option to sort by population

- add more unit tests (mock the calls to the external APIs), add some integration tests to the project (which call
the actual external APIs, these should probably be separated from your unit tests)

- Add some caching (save results in memory), retrieving all countries every time from external
  API is not optimal

- Add functionality for filtering countries, by region, by minimum temperature in the capital etc.

- add displaying historical or forecast weather data

- try adding information about flights / attractions about country / capital from third party APIs
  (most require an registration to get an api key)

- add some additional info about capitals from wikipedia (for example: https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts|info&titles=Helsinki&exintro=true&explaintext=true&inprop=url)
