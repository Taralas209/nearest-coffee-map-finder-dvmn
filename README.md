# Nearest Coffee Finder

This Python application uses the Yandex Maps Geocoding API to find the nearest coffee places to the user's location. It generates an interactive map with markers for the user's location and the closest coffee spots.

## Getting Started

To use this code, clone the repository to your local machine. 

```git clone https://github.com/<your-github-username>/coffee-locator.git```

```cd coffee-locator```

## Prerequisites
Before you continue, ensure you have met the following requirements:

You have installed Python 3.8 or later.
You have a Yandex Maps API token. If not, you can get it here.
You have the requests, folium, geopy and flask Python packages installed. If not, you can install them using pip:

```pip install requests folium geopy flask```

## How to Use
You should save your Yandex Maps API token to an environment variable YANDEX_MAP_TOKEN:

```export YANDEX_MAP_TOKEN=<your-yandex-map-token>```

You can then run the script with:

```python coffee_locator.py```

The application will ask you for your current location.
After entering your location, it will create a map with the nearest coffee spots marked on it and save it as index.html.
It will then start a Flask server at http://0.0.0.0:5000, where you can see the generated map.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.

## Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
