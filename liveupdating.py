from logging import PlaceHolder
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
import requests
import time


placeholder = st.empty()
grafik = st.empty()
counter_list = []

def update_layout():
    url = "https://data-live.flightradar24.com/zones/fcgi/feed.js?faa=1\
           &mlat=1&flarm=1&adsb=1&gnd=1&air=1&vehicles=1&estimated=1&stats=1"
    # A fake header is necessary to access the site:
    res = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    data = res.json()
    counter = 0
    for element in data["stats"]["total"]:
        counter += data["stats"]["total"][element]
    counter_list.append(counter)
    return placeholder.write('Active flights worldwide: {}'.format(counter))

# Menggunakan Plotly Express

def graph_line():
    fig = px.line(x=list(range(len(counter_list))), y= counter_list)
    return grafik.plotly_chart(fig)

# Menggunakan Plotly Graph Obj

# def graph_line():
#     fig = go.Figure(
#         data = [go.Scatter(
#         x = list(range(len(counter_list))),
#         y = counter_list,
#         mode='lines+markers'
#         )])
#     return grafik.plotly_chart(fig)

with st.container():
    st.markdown("# Live Updating Active Flights Worldwide")

with st.container():
    while True:
        update_layout()
        # st.write(counter_list)
        graph_line()
        time.sleep(6)