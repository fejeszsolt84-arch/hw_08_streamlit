import streamlit as st
import requests
import pandas as pd
from datetime import datetime

st.set_page_config(layout="wide")

API_KEY = st.secrets["openweathermap"]["api_key"]

BASE_URL = "https://api.openweathermap.org/data/2.5/"


def get_city_weather(city,API_KEY):
   
   city_url=BASE_URL + "weather"
   params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "hu"
        }
   
   response = requests.get(city_url, params=params)
   if response.status_code == 200:
    return response.json()
   else:
     return None

def get_forecast(city,API_KEY):
   forecast_url=BASE_URL + "forecast"

   params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "hu"
        }
   
   response = requests.get(forecast_url, params=params)
   
   if response.status_code == 200:
     return response.json()
   else:
     return None
   
st.title("Időjárás")

city = st.text_input("Melyik város érdekel?")

if city:
    if API_KEY:  
        city_weather=get_city_weather(city,API_KEY)
        

        if city_weather is not None:
           lat = city_weather['coord']['lat']
           lon = city_weather['coord']['lon']
           df_map = pd.DataFrame({'lat': [lat], 'lon': [lon]})
           st.map(df_map)
           st.subheader(f"{city} mostani időjárása")
           col1, col2, col3,col4,col5, col6 = st.columns(6)

           col1.metric("Jelenlegi hőfok:",f"{city_weather['main']['temp']} °C")
           col2.metric("Jelenlegi hőérzet:", f"{city_weather['main']['feels_like']} °C")
           col3.metric("Páratartalom:", f"{city_weather['main']['humidity']} %")
           col4.metric("Szélsebesség:", f"{city_weather['wind']['speed']} m/s")
           col5.metric("Felhőzet:", f"{city_weather['clouds']['all']} %")
           col6.metric("Időjárás", f"{city_weather['weather'][0]['description']} ")
           icon_code = city_weather['weather'][0]['icon']
           icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
           col6.image(icon_url, width=100)

        forecast_weather=get_forecast(city,API_KEY)
        df_forecast = pd.DataFrame({
                "Dátum": [item["dt_txt"] for item in forecast_weather["list"]],
                "Hőfok": [item["main"]["temp"] for item in forecast_weather["list"]],
                "Páratartalom": [item["main"]["humidity"] for item in forecast_weather["list"]],
                "Szélsebesség": [item["wind"]["speed"] for item in forecast_weather["list"]],
                "Felhőzet": [item["clouds"]["all"] for item in forecast_weather["list"]],
                "Időjárás": [item['weather'][0]['description'] for item in forecast_weather["list"]],
            })

        st.subheader("Előrejelzés")
        st.dataframe(df_forecast)

        st.subheader("Hőd és páratartalom diagram")
        diagram = ['Hőfok', 'Páratartalom',]

        st.line_chart(
        df_forecast, 
        x='Dátum', 
        y=diagram
        )
        st.subheader("Felhőzet")
        st.line_chart(
        df_forecast, 
        x='Dátum', 
        y='Felhőzet'
        )

        st.subheader("Szélsebesség")
        st.line_chart(
        df_forecast, 
        x='Dátum', 
        y='Szélsebesség'
        )
     
    
else:
   st.info("Add meg a várost")