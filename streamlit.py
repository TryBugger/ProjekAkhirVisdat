import fractions
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import seaborn as sns

# rc('font',**{'family':'sans-serif','sans-serif':['Lato']})

@st.cache_data
def load_rating_data(nrows=9999999):
    data = pd.read_csv("dataset/tourism_rating.csv", nrows=nrows)
    return data

@st.cache_data
def load_user_data(nrows=9999999):
    data = pd.read_csv("dataset/user.csv", nrows=nrows)
    return data

@st.cache_data
def load_destination_data(nrows=9999999):
    data = pd.read_csv("dataset/tourism_with_id.csv", nrows=nrows)
    return data

data_rating = load_rating_data()
data_user = load_user_data()
data_destination = load_destination_data()

### Judul Utama

st.title("Rekomendasi Tempat Wisata")
st.text("Dashboard ini akan menampilkan daftar wisata, wisata berdasarkan top rating, dan rating user untuk masing-masing kota")
st.markdown("""---""")

### Daftar Data Wisata

data_destination_simple = data_destination.loc[:, 'Place_Name':'Time_Minutes']
st.header("Daftar Data Wisata")
st.write(data_destination_simple)
st.markdown("""---""")

### Daftar Top 10 Wisata berdasarkan Rating
st.header("Daftar 10 Teratas dan 10 Terbawah Wisata Masing-Masing Kota Berdasarkan Rating")
# kota="Jakarta"
st.write('<style>div.row-widget.stRadio > div{flex-direction:row;justify-content: center;} </style>', unsafe_allow_html=True)
st.write('<style>div.st-bf{flex-direction:column;} div.st-ag{font-weight:bold;padding-left:2px;}</style>', unsafe_allow_html=True)
kota = st.radio(
    "Pilih Kota Destinasi Pariwisata",
    data_destination['City'].unique()
)

df_top10_pariwisata = data_destination[data_destination['City'] == kota].sort_values(by=['Rating'], ascending=False).reset_index(drop=True)

fig, ax = plt.subplots(1, 1, figsize=[20, 14])
green_gradient = np.linspace(0.4, 1, 10)[::-1]
red_gradient = np.linspace(0.4, 1, 10)

ax.bar(df_top10_pariwisata[:10]['Place_Name'], df_top10_pariwisata[:10]['Rating'], 
       color=plt.cm.Greens(green_gradient), label='_nolegend_')
ax.bar(df_top10_pariwisata[-10:]['Place_Name'], df_top10_pariwisata[-10:]['Rating'], 
       color=plt.cm.Reds(red_gradient), label='_nolegend_')
ax.axhline(df_top10_pariwisata['Rating'].mean(), color='dodgerblue',
           linewidth=5, label='Rata-rata')

ax.tick_params(axis='x', labelrotation = -90)
ax.set_ylabel('Rating', fontsize=24)
ax.set_xlabel('Nama Pariwisata', fontsize=24)
ax.set_title(f'Daftar Pariwisata Kota {kota} Berdasarkan Rating', fontsize=32)
ax.legend(fontsize=22, frameon=False)

st.pyplot(fig)
st.markdown("""---""")

### Daftar Persebaran Rating Pengunjung Masing-Masing Kota

st.header("Persebaran Rating Pengunjung Masing-Masing Kota")
st.subheader("Kota Jakarta")

data_destination_simple = data_destination.loc[:, 'Place_Id':'Time_Minutes']
# st.write(data_destination_simple[data_destination_simple['City'] == 'Jakarta'])

data_kota = data_destination_simple[data_destination_simple['City'] == 'Jakarta']
data_kota_rating = data_rating[data_rating['Place_Id'] & data_kota['Place_Id']]

fig, ax = plt.subplots(1, 1)

sns.countplot(data=data_kota_rating, 
              x='Place_Ratings',
              ax=ax)
ax.set_ylabel('Total Rating')
ax.set_xlabel('Rating Kota')
st.pyplot(fig)
st.markdown("""---""")


### Total Keseluruhan Rating Setiap Kota

st.header("Total Keseluruhan Rating Setiap Kota")

data_kota_total_rating = data_destination.loc[:, ['City', 'Rating']].groupby('City').sum().reset_index()

fig, ax = plt.subplots(1, 1, figsize=[8, 6])
colors = ['steelblue' if (city == 'Jakarta') else 'lightgrey' for city in data_kota_total_rating['City']]

sns.barplot(data=data_kota_total_rating,
            x='City', y='Rating', palette=colors, 
            ax=ax)
ax.set_title(f'Total Rating Setiap Kota', fontsize=18)
ax.set_ylabel('Total Rating', fontsize=14)
ax.set_xlabel('Nama Kota', fontsize=14)

st.pyplot(fig)
st.markdown("""---""")

### Rata-Rata Rating Tempat Wisata Berdasarkan Kategori

st.header("Total Rating Tempat Wisata Berdasarkan Kategori Wisata")

data_kategori_total_rating = data_destination.loc[:, ['Category', 'Rating']].groupby('Category').sum().sort_values(by='Rating', ascending=False).reset_index()
fig, ax = plt.subplots(1, 1, figsize=[12, 8])
colors = ['mediumseagreen'] + ['lightgrey']*(len(data_kategori_total_rating) - 2) + ['indianred']

sns.barplot(data=data_kategori_total_rating,
            x='Category', y='Rating', palette=colors, 
            ax=ax)
ax.set_title(f'Total Rating Kategori Wisata', fontsize=22)
ax.set_ylabel('Total Rating', fontsize=16)
ax.set_xlabel('Nama Kategori', fontsize=16)
st.pyplot(fig)
