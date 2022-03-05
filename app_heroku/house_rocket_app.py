import geopandas
import streamlit as st
import pandas as pd
import numpy as np
import folium
import plotly.express as px
import plotly.graph_objects as go

from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from datetime import datetime

st.set_page_config(layout='wide')

@st.cache(allow_output_mutation=True)
# Function to read the dataset
def get_data(path):
    data = pd.read_csv(path)
    data['date'] = pd.to_datetime(data['date']).dt.date
    return data

@st.cache(allow_output_mutation=True)
def get_geofile(url):
 geofile = geopandas.read_file(url)
 return geofile

def set_feature(data):
    # add new features
    data['date'] = pd.to_datetime(data['date'])
    data['month'] = data['date'].dt.month
    data['year'] = data['date'].dt.year
    data['season'] = data['date'].apply(
        lambda x: 'Spring' if ((x >= pd.to_datetime('2014-03-20')) & (x < pd.to_datetime('2014-06-21'))) | (
                    (x >= pd.to_datetime('2015-03-20')) & (x < pd.to_datetime('2015-06-20'))) else
        'Summer' if (x >= pd.to_datetime('2014-06-21')) & (x < pd.to_datetime('2014-09-22')) else
        'Fall' if (x >= pd.to_datetime('2014-09-22')) & (x < pd.to_datetime('2014-12-21')) else
        'Winter'
        )
    data['old'] = data['yr_built'].apply(lambda x: '< 1955' if x < 1955 else
    '>= 1955')
    data['basement'] = data['sqft_basement'].apply(lambda x: 'Yes' if x != 0 else
    'No')
    data['is_waterfront'] = data['waterfront'].apply(lambda x: 'Yes' if x != 0 else
    'No')

    return data

def houses_with_status(data):
    df_price_median = data[['price', 'zipcode']].groupby('zipcode').median().reset_index()
    df_price_median = df_price_median.rename(columns={'price': 'median_price'})
    df1 = pd.merge(data, df_price_median, on='zipcode', how='inner')
    df1['status'] = 0
    for i in range(len(df1)):
        if (df1.loc[i, 'price'] < df1.loc[i, 'median_price']) & (df1.loc[i, 'condition'] >= 2):
            df1.loc[i, 'status'] = "buy"
        else:
            df1.loc[i, 'status'] = "do not buy"
    df_house_status = df1.copy()
    return df_house_status

def df_profit(data):

    df3 = houses_with_status(data)[houses_with_status(data)['status']=='buy'].copy().reset_index()
    df4 = df3[['price', 'zipcode', 'season']].groupby(['zipcode', 'season']).median().reset_index()
    df4.columns = ['zipcode', 'season', 'median_price_zipcode_season']

    # Creating Sale price Variable -----------
    df3['sale_price'] = 0

    for i in range(len(df3)):
        if df3.loc[i, 'price'] >= float(
                df4[(df4['zipcode'] == df3['zipcode'][i]) & (df4['season'] == df3['season'][i])][
                    'median_price_zipcode_season']):
            df3.loc[i, 'sale_price'] = 1.1 * df3['price'][i]
        else:
            df3.loc[i, 'sale_price'] = 1.3 * df3['price'][i]

    # Calculating the profit
    df3['profit'] = df3['sale_price'] - df3['price']

    return df3

def houses_to_buy_and_sell(data):
    df2 = houses_with_status(data)[['id', 'zipcode', 'price', 'median_price', 'condition', 'status']].copy()
    df2.columns = ['ID', 'Region', 'Price', 'Median Price', 'Condition', 'Status']
    df_to_buy = df2[df2['Status']=='buy'].copy()

    #
    # df3 = houses_with_status(data)[houses_with_status(data)['status']=='buy'].copy().reset_index()
    # df4 = df3[['price', 'zipcode', 'season']].groupby(['zipcode', 'season']).median().reset_index()
    # df4.columns = ['zipcode', 'season', 'median_price_zipcode_season']
    #
    # # Creating Sale price Variable -----------
    # df3['sale_price'] = 0
    #
    # for i in range(len(df3)):
    #     if df3.loc[i, 'price'] >= float(
    #             df4[(df4['zipcode'] == df3['zipcode'][i]) & (df4['season'] == df3['season'][i])][
    #                 'median_price_zipcode_season']):
    #         df3.loc[i, 'sale_price'] = 1.1 * df3['price'][i]
    #     else:
    #         df3.loc[i, 'sale_price'] = 1.3 * df3['price'][i]
    #
    # # Calculating the profit
    # df3['profit'] = df3['sale_price'] - df3['price']
    df3 = df_profit(data)
    df_to_sell = df3[['id', 'zipcode', 'season', 'median_price', 'price', 'sale_price', 'profit', 'condition']]
    df_to_sell.columns = ['ID', 'Region', 'Season', 'Median Price', 'Price', 'Sale Price', 'Profit', 'Condition']

    # Filtering the data
    st.sidebar.title('Filters for the dataframes')
    f_season = st.sidebar.multiselect('Select the season(s):',
                                       sorted(set(df_to_sell['Season'].unique())),
                                       default='Summer')


    f_zipcode = st.sidebar.multiselect('Enter zipcode',
                                       df_to_buy['Region'].unique(),
                                       default=df_to_buy['Region'].unique()[4])


# Writing the tables on the dashboard --------
    df_to_buy_show = df_to_buy.loc[df_to_buy['Region'].isin(f_zipcode)]

    c1, c2 = st.columns((1, 1))
    c1.header('Suggestions to buy')
    c1.dataframe(df_to_buy_show, height=600)


    c2.header('Suggestions to sell')
    c2.dataframe(df_to_sell.loc[df_to_sell['Season'].isin(f_season)], height=600)

    return None

# Hypothesis -----------------
def tested_hypothesis(data):
    st.title('Hypotheses Tested')
    c1, c2 = st.columns((1, 1))
    c1.subheader('H1: Houses with waterfront are, on average, 30% more expensive.')
    # H1
    y0 = data[data['waterfront'] == 0]['price']
    y1 = data[data['waterfront'] == 1]['price']
    fig = go.Figure()
    fig.add_trace(go.Box(y=y0, name='Not Waterfront',
                         marker_color='indianred'))
    fig.add_trace(go.Box(y=y1, name='Waterfront',
                         marker_color='lightseagreen'))
    fig.update_layout(
        title="Prices per Waterfront",
        xaxis_title=" ",
        yaxis_title="Price"
    )
    c1.plotly_chart(fig, use_container_width=True)

    # H2
    c2.subheader('H2: Houses built before 1955, are 50% cheaper, on average.')
    y0 = data[data['old'] == '< 1955']['price']
    y1 = data[data['old'] != '< 1955']['price']

    fig = go.Figure()
    fig.add_trace(go.Box(y=y0, name='< 1955',
                         marker_color='indianred'))
    fig.add_trace(go.Box(y=y1, name='≥ 1955',
                         marker_color='lightseagreen'))
    fig.update_layout(
        title="Prices per Year built",
        xaxis_title="Year built",
        yaxis_title="Price"
    )
    c2.plotly_chart(fig, use_container_width=True)


    # H3
    c1, c2 = st.columns((1, 1))
    c1.subheader('H3: Houses without basement have total area (sqft_lot) 40% bigger than houses with basement.')
    data[['sqft_lot', 'basement']].groupby('basement').mean().reset_index()
    y0 = data[data['basement'] == 'Yes']['sqft_lot']
    y1 = data[data['basement'] == 'No']['sqft_lot']
    fig = go.Figure()
    fig.add_trace(go.Box(y=y0, name='Yes',
                         marker_color='indianred'))
    fig.add_trace(go.Box(y=y1, name='No',
                         marker_color='lightseagreen'))
    fig.update_layout(
        title="Area per Basement",
        xaxis_title="Basement",
        yaxis_title="Area (sqft)"
    )
    c1.plotly_chart(fig, use_container_width=True)

    # H4
    c2.subheader('H4: The YoY (Year Over Year) growth on houses price is 10%.')
    mean_price_2014 = data[data['year'] == 2014]['price'].mean()
    mean_price_2015 = data[data['year'] == 2015]['price'].mean()
    # Standard deviation
    std_price_2014 = data[data['year'] == 2014]['price'].std()
    std_price_2015 = data[data['year'] == 2015]['price'].std()
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name='2014',
        x=['Year'], y=[mean_price_2014],
        error_y=dict(type='data', array=[std_price_2014])
    ))
    fig.add_trace(go.Bar(
        name='2015',
        x=['Year'], y=[mean_price_2015],
        error_y=dict(type='data', array=[std_price_2015])
    ))
    fig.update_layout(barmode='group')
    c2.plotly_chart(fig, use_container_width=True)

    # H5
    c1, c2 = st.columns((1, 1))
    three_bathrooms_df = data[data['bathrooms'] == 3][['price', 'month']].groupby('month').mean().reset_index()
    fig = px.line(three_bathrooms_df, x='month', y='price')
    c1.subheader('H5: Houses with 3 bathrooms have a 15% MoM (Month over Month) price growth.')
    c1.plotly_chart(fig, use_container_width=True)

    # H6
    c2.subheader('H6: Houses are renovated, on average, after 30 years from the built year.')
    renovated_df = data[data['yr_renovated'] != 0].copy().reset_index()
    renovated_df['time_diff'] = renovated_df['yr_renovated'] - renovated_df['yr_built']
    fig = px.histogram(renovated_df, x="time_diff")
    c2.plotly_chart(fig, use_container_width=True)


    # H7
    c1, c2 = st.columns((1, 1))
    c1.subheader('H7: The YoY (Year over Year) area growth is - 5%, i. e., the house\'s size become smaller over year.')
    area_by_year_df = data[['yr_built', 'sqft_lot']].groupby('yr_built').mean().reset_index()
    fig = px.line(area_by_year_df, x='yr_built', y='sqft_lot')
    c1.plotly_chart(fig, use_container_width=True)

    # H8
    c2.subheader('H8: Houses are 20% cheaper on the winter.')
    fig = px.box(data, x="season", y="price")
    c2.plotly_chart(fig, use_container_width=True)

    # H9
    c1, c2 = st.columns((1, 1))
    c1.subheader('H9: In the summer the profit from sale is 35% bigger than the winter season.')
    fig = px.box(df_profit(data), x="season", y="profit")
    c1.plotly_chart(fig, use_container_width=True)

    # H10
    c2.subheader('H10: Houses with waterfront has an area 25% bigger than the houses without waterfront.')
    fig = px.box(data, x="waterfront", y="sqft_lot")
    c2.plotly_chart(fig, use_container_width=True)

    return None

def map_function(data, geofile):
    data = houses_with_status(data).copy()
    data_map = data[data['status'] == 'buy'].copy()

    st.sidebar.title('Filters for the map')
    # filters ---------------------
    f_watefront = st.sidebar.checkbox('Only Houses with Waterfront')
    f_bathrooms = st.sidebar.selectbox('Max Number of bathrooms',
                                       sorted(set(data_map['bathrooms'].unique())),
                                       index=3)
    f_bedrooms = st.sidebar.selectbox('Max Number of bedrooms',
                                      sorted(set(data_map['bedrooms'].unique())),
                                      index=2)

    f_price = st.sidebar.slider(
        label='Price',
        min_value=int(data_map['price'].min()),
        max_value=int(data_map['price'].max()),
        value=int(data_map['price'].mean())

    )

    st.sidebar.markdown('For more information about the analysis performed, you can access this [GitHub Repository](https://github.com/edneide/house_rocket_insight_project)')

    if f_watefront:
        df_map = data_map[(data_map['price'] <= f_price) &
                      (data_map['bathrooms'] == f_bathrooms) &
                      (data_map['bedrooms'] == f_bedrooms) &
                      (data_map['is_waterfront'] == 'Yes')].reset_index()
    else:
        df_map = data_map[(data_map['price'] <= f_price) &
                      (data_map['bathrooms'] == f_bathrooms) &
                      (data_map['bedrooms'] == f_bedrooms) &
                      (data_map['is_waterfront'] == 'No')].reset_index()

    geofile = geofile[geofile['ZIP'].isin(df_map['zipcode'].tolist())]

    st.title('Map')
    my_map = folium.Map(location=[df_map['lat'].mean(), df_map['long'].mean()],
                        default_zoom_start=15)

    marker_cluster = MarkerCluster().add_to(my_map)
    for name, row in df_map.iterrows():
        folium.Marker([row['lat'], row['long']],
                      popup='Sold U${0} on: {1}. Features: {2} bedrooms, {3} bathrooms, condition: {4}, zipcode: {5}'.format(
                          row['price'],
                          row['date'],
                          row['bedrooms'],
                          row['bathrooms'],
                          row['condition'],
                          row['zipcode'])).add_to(marker_cluster)



    folium_static(my_map)
    return None

st.title('Welcome to the House Rocket Dashboard')

if __name__ == "__main__":

    # ETL

    # ===========
    # Extraction
    # ===========
    path = 'kc_house_data.csv'
    url = 'https://opendata.arcgis.com/datasets/83fc2e72903343aabff6de8cb445b81c_2.geojson'

    data = get_data(path)
    geofile = get_geofile(url)

    # ===============
    # Transformation
    # ===============
    data = set_feature(data)

    # ===========
    # Loading
    # ===========
    houses_with_status(data)

    houses_to_buy_and_sell(data)

    tested_hypothesis(data)

    map_function(data, geofile)
