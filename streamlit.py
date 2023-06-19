import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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
kota="Jakarta"
st.header("Daftar 10 Teratas dan 10 Terbawah Wisata Masing-Masing Kota Berdasarkan Rating")
st.subheader(kota)

# data_top_rating_kota = data_destination_simple.loc[data_destination_simple['City'] == kota].sort_values(by=['Rating'], ascending=False).reset_index().head(10)
df_top10_pariwisata = data_destination[data_destination['City'] == kota].sort_values(by=['Rating'], ascending=False).reset_index(drop=True)
df_top10_pariwisata = pd.concat([df_top10_pariwisata.head(10), df_top10_pariwisata.tail(10)])

fig, ax = plt.subplots(1, 1, figsize=[14, 8])
green_gradient = np.linspace(0.4, 1, 10)[::-1]
red_gradient = np.linspace(0.4, 1, 10)

ax.bar(df_top10_pariwisata.loc[:10, 'Place_Name'], df_top10_pariwisata.loc[:10, 'Rating'], 
       color=plt.cm.Greens(green_gradient))
ax.bar(df_top10_pariwisata.loc[10:, 'Place_Name'], df_top10_pariwisata.loc[10:, 'Rating'], 
       color=plt.cm.Reds(red_gradient))
ax.tick_params(axis='x', labelrotation = -90)
ax.set_ylabel('Rating', fontsize=18)
ax.set_xlabel('Nama Pariwisata', fontsize=18)
ax.set_title('Daftar Pariwisata Berdasarkan Rating', fontsize=28)

st.pyplot(fig)
st.markdown("""---""")

### Daftar Data Wisata

st.header("Visualisasi Rating Pengunjung Masing-Masing Kota")
st.subheader("Persebaran Rating Kota Jakarta")

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

st.header("Total Keseluruhan Rating Antar Kota")

data_rating_antar_kota = data_destination_simple[['City', 'Rating']].groupby('City').sum()
# st.write(data_rating_antar_kota)

fig, ax = plt.subplots(1, 1)

data_rating_antar_kota.plot(kind='bar', title='Total Rating Antar Kota',
                            ylabel='Total Rating', xlabel='Kota Wisata', figsize=[10, 6],
                            ax=ax)
st.pyplot(fig)

# st.text('Rata-rata Rating Antar Kota')
# st.write(data_rating_antar_kota)

# fig, ax = plt.subplots(1, 1)

# data_rating_antar_kota.plot(kind='bar', title='Rata-Rata Rating Antar Kota',
#                             ylabel='Rata-rata Rating', xlabel='Kota Wisata', figsize=[10, 6],
#                             ax=ax)
# st.pyplot(fig)
st.markdown("""---""")

st.header("Rata-rata Tempat Wisata Berdasarkan Kategori Wisata")

data_rating_kategori = data_destination_simple[['Category', 'Rating']].groupby('Category').mean().sort_values(by=['Rating'], ascending=False)

fig, ax = plt.subplots(1, 1)

data_rating_kategori.plot(kind='bar', title='Total Rating Antar Kota',
                          ylabel='Rata-rata Rating', xlabel='Kategori Tempat Wisata', figsize=[10, 6],
                          ax=ax)
st.pyplot(fig)
