import os
import json
import requests
import folium
from geopy import distance
from flask import Flask

YM_TOKEN = os.getenv('YANDEX_MAP_TOKEN')

def get_my_position():
    return input('Где вы находитесь?')
    
def fetch_coordinates(YM_TOKEN, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": YM_TOKEN,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']
    if not found_places:
        return None
    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat

def find_distance_coffee(my_coords_reversed):
    with open("coffee.json", "r", encoding="CP1251") as my_file:
        coffee_json = my_file.read()
    coffee_lst = json.loads(coffee_json)
    new_coffee_lst = []
    for coffee in coffee_lst:
        coffee_name = coffee['Name']
        coffee_coords = coffee['geoData']['coordinates']
        coffee_coords_reversed = (coffee_coords[1], coffee_coords[0])
        dist = distance.distance(my_coords_reversed, coffee_coords_reversed).km
        dct = {
            'title': coffee_name, 
            'distance': dist,
            'latitude': coffee_coords_reversed[0],
            'longitude': coffee_coords_reversed[1]
        }
        new_coffee_lst.append(dct)
    return new_coffee_lst

def get_coffee_distance(nearest_coffee):
    return nearest_coffee['distance']
    
def get_markers(my_coords_reversed,next_five_coffee):
    m = folium.Map(location=[my_coords_reversed[0], my_coords_reversed[1]],
        zoom_start=14, tiles="Stamen Terrain")
    tooltip = "Click me!"
    folium.Marker(
        [my_coords_reversed[0], my_coords_reversed[1]], 
        popup="<i>Ваше местоположение</i>", 
        tooltip=tooltip, 
        icon=folium.Icon(color="green")
    ).add_to(m)
    for i, coffee in enumerate(next_five_coffee):
            folium.Marker(
                [coffee['latitude'], coffee['longitude']], 
                popup="<i>Coffee {}</i>".format(i + 1), 
                tooltip=tooltip
            ).add_to(m)   
    m.save("index.html")
    
def display_coffee():
    with open('index.html') as file:
      return file.read()

if __name__ == '__main__':
    my_position = get_my_position()
    my_coords = fetch_coordinates(YM_TOKEN, my_position)
    my_coords_reversed = my_coords[1], my_coords[0]
    new_coffee_lst = find_distance_coffee(my_coords_reversed)
    next_five_coffee = sorted(new_coffee_lst, key=get_coffee_distance)[:5]
    get_markers(my_coords_reversed, next_five_coffee)
    app = Flask(__name__)
    app.add_url_rule('/', 'show_my_coffee', display_coffee)
    app.run('0.0.0.0')
