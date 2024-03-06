import base64
import io
import random
import pandas as pd
import streamlit as st
import os
import json
import datetime
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import webbrowser


def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), [' ', ' K', ' M', ' B', ' T'][magnitude])


def restrict_dataframe(df, start_range, end_range):
    df = df[(df['day'] >= pd.Timestamp(start_range)) & (df['day'] <= pd.Timestamp(end_range))]
    return df



def ajouter_espace_milliers(chaine):
    # Chercher la position du point décimal
    point_decimal = chaine.find('.')

    # Séparer la partie entière et décimale
    if point_decimal != -1:
        entier = chaine[:point_decimal]
        decimal = chaine[point_decimal:]
    else:
        entier = chaine
        decimal = ''

    # Ajouter un espace tous les trois caractères dans la partie entière
    entier = entier[::-1]  # Inverser la chaîne de caractères
    entier = ' '.join(entier[i:i + 3] for i in range(0, len(entier), 3))
    entier = entier[::-1]  # Inverser à nouveau la chaîne de caractères

    return entier + decimal  # Retourner le résultat sans l'unité de mesure


def restrict_all_dataframes(df):
    start_range = df['day'].min()
    end_range = df['day'].max()
    df = restrict_dataframe(df, start_range, end_range)
    df_sum_by_day = render_df_sum_by_day(df)

    return df, df_sum_by_day


def human_formatCO2(co2):
    num = float('{:.3g}'.format(co2))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), [' g', ' Kg', ' T'][magnitude])


def render_calendar(col, start_date, end_date):
    # Display a date input widget with a predefined date range
    selected_date_range = col.date_input("Filter the datas within this range:", [start_date, end_date],
                                         min_value=start_date, max_value=end_date)

    if selected_date_range:
        # If it's not empty, unpack it into start_range and end_range
        if isinstance(selected_date_range[0], datetime.date):
            # If it's a single date, set start_range and end_range to the same value
            start_range = selected_date_range[0]
            end_range = selected_date_range[0] if len(selected_date_range) == 1 else selected_date_range[1]
        else:
            # If it's a date range, unpack it into start_range and end_range
            start_range, end_range = selected_date_range

        return start_range, end_range
    else:
        col.warning("Please select a date range.")


def read_css_file(file_path):
    """Read the contents of a CSS file."""
    with open(file_path) as css_file:
        return css_file.read()

page_ouverte = False
def open_webpage():
    """Ouvre la page web dans un nouvel onglet."""
    global page_ouverte
    if not page_ouverte:
        webbrowser.open_new_tab("https://tree-nation.com/plant/myself")
        page_ouverte = True
def restrict_by_day(df,first_day,last_day):
    df = df[(df['day'] >= pd.Timestamp(first_day)) & (df['day'] <= pd.Timestamp(last_day))]
    return df


def convert_image_to_base64(image):
    """Convert an image file to a base64 encoded string."""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def display_image_in_sidebar(image_base64, width, margin_bottom):
    """Display an image in the Streamlit sidebar with custom dimensions."""
    st.sidebar.markdown(
        f'<img src="data:image/png;base64,{image_base64}" style="width:{width}px; margin-bottom:{margin_bottom}px" />',
        unsafe_allow_html=True,
    )


def add_carbon_intensity(df):
    intensity_dict = {"FR": 110, "ES": 240, "DE": 480}
    df["carbon_intensity"] = df["geo_country"].map(intensity_dict)
    return df


def restict_by_media_context(df, media_context):
    if media_context == "All":
        return df
    elif media_context == "Video":
        return df[df["media_type"] == "video"]
    elif media_context == "Banner":
        return df[df["media_type"] == "banner"]


# Create a dataframe with the sum of co2 per day
def render_df_sum_by_day(df):
    df_sum_by_day = df.groupby('day').sum(numeric_only=True)
    df_sum_by_day.reset_index(inplace=True)
    df_sum_by_day['day'] = pd.to_datetime(df_sum_by_day['day'], format='%Y-%m-%d')
    df_sum_by_day = df_sum_by_day.sort_values(by='day')
    df_sum_by_day["co2PerImp"] = df_sum_by_day["co2total"] / df_sum_by_day["imps"]
    df_sum_by_day["co2PerClick"] = df_sum_by_day["co2total"] / df_sum_by_day["clicks"]
    df_sum_by_day["co2Per$Spent"] = df_sum_by_day["co2total"] / df_sum_by_day["spend"]
    return df_sum_by_day


def get_deals_list(df):
    deals_list = df['line_item'].unique()
    deals_list = ["All"] + list(deals_list)
    return deals_list


# TODO implémenter ceci dans la selection des deals

def get_each_country_co2(df):
    df_country_co2 = df.groupby('geo_country').sum(numeric_only=True)
    df_country_co2.reset_index(inplace=True)
    df_country_co2 = df_country_co2.sort_values(by='co2total', ascending=False)
    # TODO apply to all country & return dict
    print(df_country_co2.columns)
    return df_country_co2


def restrict_by_deal(df, deal_name):
    if deal_name == 'All':
        return df
    else:
        df = df[df['line_item'] == deal_name]
        # restrict the df.csv on only the last week
        today = datetime.datetime.today()
        last_week = today - datetime.timedelta(days=7)
    return df


def get_brands_list(df):
    brands_list = get_unique_values(df, 'brand_name')
    # sort to alphabetical order
    sorted_list = sorted(list(brands_list))
    return ["All"] + sorted_list


def restrict_by_brand(df, brand_name):
    if brand_name == "All":
        return df
    if brand_name == "Demo Brand":
        return df
    else:
        df = df[df['brand_name'] == brand_name]
    return df


def get_unique_values(df, column):
    return df[column].unique()


def ifBannerOnly(df):
    st.write(" ")
    st.write(" ")
    dfBanner = df[df['size'] != '1x1']
    dfBanner = dfBanner.groupby('size').sum(numeric_only=True) / 1000
    dfBanner = dfBanner.reset_index()
    dfBanner = dfBanner.rename(columns={'size': 'Banner Size'})
    dfBanner = dfBanner.rename(columns={'co2total': 'CO2e'})
    dfBanner["gCO2e Per 1000 Impressions"] = dfBanner["CO2e"] / dfBanner["imps"]
    dfBanner["gCO2e Per 1000$ Spent"] = dfBanner["CO2e"] / dfBanner["spend"]
    dfBanner = dfBanner.round(3)
    dfBanner = dfBanner.sort_values(by=['CO2e'], ascending=False)
    dfBanner['CO2e'] = dfBanner['CO2e'].apply(lambda x: f"{x} Kg" if x >= 1 else f"{x * 1000} g")
    dfBanner = dfBanner[
        ['Banner Size', 'CO2e', 'gCO2e Per 1000 Impressions', 'gCO2e Per 1000 Views', 'gCO2e Per 1000$ Spent']]
    dfBanner = dfBanner.reset_index()
    dfBanner.drop(['index'], axis=1, inplace=True)
    st.dataframe(dfBanner)


def if_video_only(df):
    st.write(' ')
    st.write(' ')
    st.write(" ")
    col1, col3 = st.columns([1, 1.7])
    col1.write("##### Per Media Type (Impressions %)")
    # create a pie chart depending on the media type df.csv["media_type"]
    fig = go.Figure(go.Pie(labels=df["media_type"], values=df["imps"]))
    # Set layout options
    fig.update_layout(
        font=dict(size=14),
        width=340,
        height=340, margin=dict(l=0, r=0, t=25, b=0)
    )
    col1.plotly_chart(fig, config={"displayModeBar": False}, use_container_width=True)
    col3.write("##### Per Context (KgCO2e)")
    df_video = df.groupby('video_context').sum(numeric_only=True) / 1000
    df_grouped = df_video.round(2).reset_index().sort_values(by='co2total',
                                                             ascending=False)

    fig = px.bar(df_grouped,
                 x='co2total',
                 y='video_context',
                 orientation='h',
                 text='co2total', labels={"video_context": "Video Context", "co2total": "KgCO2e"})

    fig.update_traces(texttemplate='%{text:.3s}', textposition='inside')
    fig.update_layout(
        font=dict(size=14),
        width=400,
        height=400,
        margin=dict(l=0, r=0, t=0, b=0),
        yaxis=dict(autorange="reversed")
    )

    col3.plotly_chart(fig, config={"displayModeBar": False}, use_container_width=True)


def both_context(df, dfVideo, dfBanner):
    st.write(' ')
    st.write(' ')
    st.write(" ")
    col1, col2 = st.columns([1, 2])
    col1.write("##### Per Media Type (Impressions %)")
    # create a pie chart depending on the media type df.csv["media_type"]
    fig = go.Figure(go.Pie(labels=df["media_type"], values=df["imps"]))
    # Set layout options
    fig.update_layout(
        font=dict(size=14),
        width=340,
        height=340, margin=dict(l=0, r=0, t=25, b=0)
    )
    col1.plotly_chart(fig, config={"displayModeBar": False}, use_container_width=True)
    col2.write("##### Per  Video Context")
    col2.dataframe(dfVideo, height=210, use_container_width=True)
    col2.write('##### Per Banner Size')
    col2.dataframe(dfBanner, height=210, use_container_width=True)


def per_media_context(df):
    dfVideo = df[df['media_type'] == 'video']
    dfBanner = df[df['media_type'] == 'banner']
    dfVideo.to_csv('dfVideo.csv')
    dfVideo = dfVideo.groupby('video_context').sum(numeric_only=True)
    dfBanner = dfBanner.groupby('size').sum(numeric_only=True)
    dfVideo = dfVideo.reset_index()
    dfBanner = dfBanner.reset_index()
    dfVideo = dfVideo.rename(columns={'video_context': 'Video Context'})
    dfBanner = dfBanner.rename(columns={'size': 'Banner Size'})
    dfVideo = dfVideo.rename(columns={'co2total': 'CO2e'})
    dfBanner = dfBanner.rename(columns={'co2total': 'CO2e'})
    dfVideo["gCO2e Per 1K Impressions"] = dfVideo["CO2e"] / dfVideo["imps"]
    dfBanner["gCO2e Per 1K Impressions"] = dfBanner["CO2e"] / dfBanner["imps"]
    dfVideo["gCO2e Per 1K$ Spent"] = dfVideo["CO2e"] / dfVideo["spend"]
    dfBanner["gCO2e Per 1K$ Spent"] = dfBanner["CO2e"] / dfBanner["spend"]
    dfVideo = dfVideo.round(2)
    dfBanner = dfBanner.round(2)
    dfVideo = dfVideo.sort_values(by=['CO2e'], ascending=False)
    dfBanner = dfBanner.sort_values(by=['CO2e'], ascending=False)
    dfVideo['CO2e'] = dfVideo['CO2e'].apply(human_formatCO2)
    dfBanner['CO2e'] = dfBanner['CO2e'].apply(human_formatCO2)
    dfVideo = dfVideo.rename(columns={'imps': 'Impressions'})
    dfBanner = dfBanner.rename(columns={'imps': 'Impressions'})
    dfVideo = dfVideo.rename(columns={'spend': '$ Spent'})
    dfBanner = dfBanner.rename(columns={'spend': '$ Spent'})

    dfVideo = dfVideo[
        ['Video Context', 'CO2e', 'Impressions', '$ Spent', 'gCO2e Per 1K Impressions', 'gCO2e Per 1K Views',
         'gCO2e Per 1K$ Spent']]
    dfBanner = dfBanner[
        ['Banner Size', 'CO2e', 'Impressions', '$ Spent', 'gCO2e Per 1K Impressions', 'gCO2e Per 1K Views',
         'gCO2e Per 1K$ Spent']]
    dfVideo = dfVideo.reset_index()
    dfBanner = dfBanner.reset_index()
    dfVideo.drop(['index'], axis=1, inplace=True)
    dfBanner.drop(['index'], axis=1, inplace=True)
    return dfVideo, dfBanner



def load_df():
    df = pd.read_csv("sfr.csv")
    df['day'] = pd.to_datetime(df['day'], format='%Y-%m-%d')
    first_day = df['day'].min()
    last_day = df['day'].max()
    return df, first_day, last_day
