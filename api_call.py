import json
import requests
import datetime

from requests import api
from class_definition import shooting_record
import class_definition
import pandas as pd
from data_fetch import api_request

# import plotly.plotly as plt
import plotly.graph_objects as plt_go
from plotly.offline import plot


from secrets import mapquest_api_key, mapbox_access_token

# returns None if nothing found, else return (lat, lng) in float
def find_lat_lng(address:str):
    base_url = "http://www.mapquestapi.com/geocoding/v1/address"
    params = {
        "key": mapquest_api_key,
        "location": address,
        "outFormat": "json"
    }

    result_json = json.loads(api_request(base_url, params))

    try:
        latlng = result_json["results"][0]["locations"][0]["latLng"]
        lat = float(latlng["lat"])
        lng = float(latlng["lng"])
        return (lat, lng)
    except:
        return None
        



# input a selected dataframe, show a plot
def plot_cases(df)->None:
    lat_list = []
    lng_list = []
    text_list = []
    center_lat = 0
    center_lng = 0

    for _index, row in df.iterrows():
        address = class_definition.address_to_search(row)
        api_result = find_lat_lng(address)
        if api_result == None:
            continue
        
        lat, lng = api_result
        lat_list.append(lat)
        lng_list.append(lng)
        text_list.append(str(row["Incident_Date"]))

        center_lat += lat
        center_lng += lng
    
    # define plotting data

    plot_data = [plt_go.Scattermapbox(
        lat = lat_list,
        lon = lng_list,
        mode = "markers",
        marker = plt_go.scattermapbox.Marker(
            size = 9,
            color = "red"
        ),
        text = text_list,
        hoverinfo = "text"
    )]

    center_lat = center_lat / len(lat_list)
    center_lng = center_lng / len(lng_list)

    layout = plt_go.Layout(
        autosize = True,
        hovermode = "closest",
        mapbox = plt_go.layout.Mapbox(
            accesstoken = mapbox_access_token,
            bearing = 0,
            center = plt_go.layout.mapbox.Center(
                lat = center_lat,
                lon = center_lng
            ),
            pitch = 0,
            zoom = 6
        )
    )

    fig = plt_go.Figure(data = plot_data, layout = layout)
    plot(fig, filename = "output_figure.html")
    return



