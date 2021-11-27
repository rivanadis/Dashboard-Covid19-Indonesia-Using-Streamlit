from json import load
from os import name
import pandas as pd
import numpy as np
import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objs as go

# LOAD DATA
@st.cache(ttl=60*60*24)
def load_data(url):
    respon_data = requests.get(url).json()
    return respon_data

@st.cache(ttl=60*60*24)
def load_data_perprovinsi(prov):
    respon_data_prov = requests.get(f"https://data.covid19.go.id/public/api/prov_detail_{prov}.json").json()
    return respon_data_prov

st.set_page_config(page_title="Data Covid-19 Per Provinsi", layout="wide")

st.title('Data COVID-19 Per Provinsi di Indonesia')


# Ambil data nama Provinsi
alamat = "https://data.covid19.go.id/public/api/prov_list.json"
daftar_prov_raw = load_data(alamat)
daftar_prov_df = pd.DataFrame(daftar_prov_raw['list_data'])
daftar_prov = daftar_prov_df['key'].values

# Olah data untuk mengambil data sesuai Provinsi
list_prov = pd.DataFrame({'provinsi':daftar_prov,'links':daftar_prov})
list_prov['links'] = list_prov['links'].map(lambda x: x.replace(" ","_"))
prov_selectbox = st.sidebar.selectbox(
                "Pilih Provinsi",list(daftar_prov)
)

# Memanggil data per provinsi melalui API
select_prov = list_prov[list_prov['provinsi']==prov_selectbox]['links'].item()
data_prov_raw  = load_data_perprovinsi(select_prov)

data_prov = pd.DataFrame(data_prov_raw['list_perkembangan'])

data_prov_rapi = (data_prov.drop(columns=[item for item in data_prov.columns 
                                               if item.startswith('AKUMULASI') 
                                                  or item.startswith('DIRAWAT')])
                           .rename(columns=str.lower)
                           .rename(columns={'kasus': 'kasus_baru'})
                  )
data_prov_rapi['tanggal'] = pd.to_datetime(data_prov_rapi['tanggal']*1e6, unit='ns')

# Chart
bar_kasus_baru = px.bar(data_prov_rapi.tail(30), y='kasus_baru', x='tanggal', labels={'tanggal':'Tanggal','kasus_baru':'Jumlah Kasus'}, color='kasus_baru')
# bar_kasus_baru = go.Figure(data=go.Bar(
#                 x= data_prov_rapi['tanggal'].tail(30),
#                 y= data_prov_rapi['kasus_baru'].tail(30),
#                 marker = dict(color='orange'),
#                 name='Kasus Harian'
#                     ))
bar_kasus_baru.update_layout(title={'text':'Kasus Baru per Hari','x':0.4,'y':0.95,'xanchor':'center','yanchor':'top',},
                            xaxis=dict(title='<b>Tanggal</b>',
                                color = 'white',
                                showline= True,
                                showgrid = False,
                                showticklabels=True,
                                linecolor='white',
                                linewidth=0.5,
                                ticks='outside',
                                tickfont=dict(family='Aerial',
                                                color ='white',
                                                size=12)),
                            yaxis=dict(title='<b>Kasus Harian</b>',
                                    color = 'white',
                                    showline= True,
                                    showgrid = True,
                                    showticklabels=True,
                                    linecolor='white',
                                    linewidth=1,
                                    ticks='outside',
                                    tickfont=dict(family='Aerial',
                                                    color ='white',
                                                    size=12)),
                            # paper_bgcolor= '#1f2c56',
                            # plot_bgcolor = '#1f2c56',
                            )

bar_sembuh = px.bar(data_prov_rapi, y='sembuh', x='tanggal', labels={'tanggal':'Tanggal','kasus_baru':'Jumlah Kasus'})
bar_sembuh.update_layout(title={'text':'Kasus Harian Sembuh','x':0.5})

bar_meninggal = px.bar(data_prov_rapi, y='meninggal', x='tanggal', labels={'tanggal':'Tanggal','kasus_baru':'Jumlah Kasus'})
bar_meninggal.update_layout(title={'text':'Kasus Harian Meninggal','x':0.5})





# LOKASI
res_lok = "https://data.covid19.go.id/public/api/prov.json"
lok = load_data(res_lok)
data_lok = pd.json_normalize(lok,['list_data']).to_dict()
df_lok = pd.DataFrame(data_lok)
df_lok.drop(labels=['jenis_kelamin','kelompok_umur'], axis=1, inplace=True)
df_lok.rename(columns={'lokasi.lat':'lat','lokasi.lon':'lon'},inplace=True)
lokasi = df_lok[df_lok['key']==prov_selectbox]
# lok_lon = df_lok[df_lok['key']==prov_selectbox]['lon'].item()
# lok_lat = df_lok[df_lok['key']==prov_selectbox]['lat'].item()

# TEXT
st.markdown(f"## {prov_selectbox}")
st.markdown("#### Last Updated: " + str(data_prov_rapi['tanggal'].iloc[-1].strftime('%d %B %Y')))

jumlah1, persensembuh, persenmati = st.columns(3)

with jumlah1:
    st.markdown("**Jumlah Total Kasus**")
    st.markdown(f"<h1 style='text-align: center; color: red;'>{data_prov_raw['kasus_total']:d}</h1>",unsafe_allow_html=True)
with persensembuh:
    st.markdown("**Persen Sembuh**")
    st.markdown(f"<h1 style='text-align: center; color: red;'>{data_prov_raw['sembuh_persen']:.2f}%</h1>",unsafe_allow_html=True)
with persenmati:
    st.markdown("**Persen Meninggal**")
    st.markdown(f"<h1 style='text-align: center; color: red;'>{data_prov_raw['meninggal_persen']:.2f}%</h1>",unsafe_allow_html=True)

st.markdown("<hr/>", unsafe_allow_html=True)





col1, col2, col3 = st.columns(3)

with col1:
    st.plotly_chart(bar_kasus_baru,use_container_width=True)
with col2:
    st.plotly_chart(bar_sembuh,use_container_width=True)
with col3:
    st.plotly_chart(bar_meninggal,use_container_width=True)

px.set_mapbox_access_token('pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw')
peta = px.scatter_mapbox(lokasi, lat='lat', lon='lon', hover_name='key', size='penambahan.positif', hover_data=['penambahan.positif', 'penambahan.sembuh','penambahan.meninggal'], 
                        color='penambahan.positif',zoom=8, height=800,color_discrete_sequence=['orange'],color_continuous_midpoint=50)
peta.update_layout( margin={"r":0,"l":0,"b":0}, title={'text':"Peta dan Penambahan Kasus",'x':0.5}, autosize=True)
st.plotly_chart(peta,use_container_width=True)