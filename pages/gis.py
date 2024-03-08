import plotly.express as px
import json
import requests
import streamlit as st
from data import*

url = "https://data.humdata.org/dataset/e66dbc70-17fe-4230-b9d6-855d192fc05c/resource/51939d78-35aa-4591-9831-11e61e555130/download/kenya.geojson"  

response = requests.get(url)
if response.status_code == 200:
    data = response.json()
    
else:
    print("Failed to fetch data from the URL. Status code")

cases = px.choropleth_mapbox(data_frame=state_total,
                             geojson=data,
                             featureidkey="properties.NAME",
                             locations="Location",
                             color_continuous_scale="Viridis", 
                             range_color=(0,3000), 
                             mapbox_style="carto-positron", 
                             zoom=3, 
                             center={"lat": 37.0902, "lon": -95.7129}, 
                             opacity=0.5, 
                             color='Cases', 
                             labels={'Cases':'Cases Recorded'})

vac = px.choropleth_mapbox(data_frame=state_vac,
                           geojson=data,
                           featureidkey="properties.NAME",
                           locations="Reporting Jurisdictions",
                           color_continuous_scale="Viridis", 
                           range_color=(300,100000), 
                           mapbox_style="carto-positron", 
                           zoom=3, 
                           center={"lat": 37.0902, "lon": -95.7129}, 
                           opacity=0.5, 
                           color='Total', 
                           labels={'Total':'Vaccines Administered'})
vac.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

def drawCaseMap():
    st.plotly_chart(cases, use_container_width=False)

def drawVacMap():
    st.plotly_chart(vac, use_container_width=False)
