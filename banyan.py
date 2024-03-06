########### Imports
from datetime import timedelta
import emoji
import streamlit
from PIL import Image
from functions import *

########### Functions


#################### Streamlit
############ Header


# Set the page configuration with a custom title, icon, and layout
st.set_page_config(page_title='Banyan - Carbon Calculator Ads', page_icon="assets/favicon.svg", layout='wide')

# Insert the CSS styles into the page
css_content = read_css_file("app/style.css")
st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)

# Load the light logo image
logo_image_light = Image.open("assets/Criteo-logo.png")

# Convert the light logo image to a base64 string
logo_base64_light = convert_image_to_base64(logo_image_light)

# Display the light logo in the sidebar
display_image_in_sidebar(logo_base64_light, width=310, margin_bottom=20)

########### Preparing data
st.markdown(
    """
    <style>
        .element-container {
            margin-top: -0.4rem !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
st.write('<style>div.block-container{padding-top:1.5rem;}</style>', unsafe_allow_html=True)
########### Sidebar
st.sidebar.title("Navigation")
# Your sidebar radio buttons
navigation = st.sidebar.radio("Go to", ["Overview","Recommendations"])

for i in range(10): #avant c'était 30
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

if "edit_expander" not in st.session_state:
    st.session_state.edit_expander = False

edit_button_container = st.sidebar.markdown(
    '<div id="edit-button-container"></div>',
    unsafe_allow_html=True
)
df,first_day,last_day = load_df()
st.write('')
df, df_sum_by_day, dfSumByDevice = restrict_all_dataframes(df)
#df_video_context, df_banner_context = get_df_context(df)
col1, col2 = st.columns([4, 1])
col1.write("## Hi Guillaume, welcome back!")
col2.write('')
col2.write('')
col2.write('')
now_minus_1 = datetime.datetime.now() - timedelta(hours=1) - timedelta(minutes=12)
col2.markdown("###### " + str("Last update : "+str(now_minus_1.strftime("%Y-%m-%d %H:%M:%S"))))
st.write('')
st.write('')
st.write(
    """Banyan provides an overview of the environmental impact of your advertising campaigns and helps you identify the most eco-friendly options.""")
# Get the dataframes restricted to the selected date range and the indicators updated
# Deal restriction
st.write('')
with st.expander("Campaign, Date & Media Context Selection"):
    col1, col2, col3 = st.columns([1, 1, 1])
col1.write('### Deal')
deal = col1.selectbox("Select a deal", get_deals_list(df))
df = restrict_by_deal(df, deal)
col2.write('### Date')
start_range, end_range = render_calendar(col2, first_day, last_day)
# TODO ICI RENDER LOAD df.csv en fonction de la marque, mais restrict en fonction de la durée
col3.markdown('### Media Context', unsafe_allow_html=True)
media_context = col3.selectbox("Select a media context", ["All", "Video", "Banner"])
df = restict_by_media_context(df, media_context)
imps = df["imps"].sum()
viewed_imps = df["viewed_imps"].sum()
clicks = df["clicks"].sum()
budget_paid = df["spend"].sum()
co2_total = df["co2total"].sum()
# create sub columns
col3, col4, col5, col6 = col2.columns(4)
if col3.button("Last Day"):
    start_range, end_range = last_day, last_day
if col4.button("Last Week"):
    start_range, end_range = last_day - timedelta(days=7), last_day
if col5.button("Last Month"):
    start_range, end_range = last_day - timedelta(days=30), last_day
if col6.button("All Time"):
    start_range, end_range = first_day, last_day

############ OVERVIEW
if navigation == "Overview":
    st.markdown("""---""")
    st.markdown(str('## Lifetime overview of : ' + "Nike"))
    st.write("")
    st.write("")
    ######## Setting KPIs
    col1, col2, col3, col4 = st.columns(4)
    co2total = round(df["co2total"].sum(), 2)
    imps = df["imps"].sum()
    col1.metric(label="Impressions", value=human_format(imps),
                help="Number of impressions delivered")
    col4.metric(label="Cost", value=human_format(budget_paid).lower() + "$",
                help="Already spent budget on the total", delta_color='inverse')
    # edit
    col2.metric(label="CO2e Emissions", value=human_formatCO2(co2_total),
                help="Total CO2e emitted by the campaign", delta_color='off')
    col3.metric(label="CO2e / Impression", value=human_formatCO2(round(co2_total / imps, 2)) + "CO2e",
                help="Total CO2e divided by the number of impressions")
    col1.write("72 % of viewed impressions")
    col4.write("Total budget spent so far")
    col2.write("56 gCO2e per Click")
    col3.write("Average CO2e per impression")
    st.write("---")
    st.write("### CO2 Impact Breakdown")
    st.write(" ")
    AdTechImpact, DataCenterImpact, DeviceTransmissionEnergy, DeviceImpact = df['CO2AdTech'].sum(), df[
        'CO2Datacenter'].sum(), df['CO2Transmission'].sum(), df['CO2Device'].sum()
    st.image("assets/output-onlinepngtools.png", output_format='PNG', use_column_width=True, width=6840)
    colAdTech, colDATA, colTRANSMISSION, COLENDUDERDEVICE = st.columns([0.8, 0.8, 0.8, 1])
    colAdTech.markdown(
        """
        <style>
            .centered-header {
                text-align: center;
                margin-top: -50px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    colDATA.markdown(
        """
        <style>
            .centered-header {
                text-align: center;
                margin-top: -50px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    colTRANSMISSION.markdown(
        """
        <style>
            .centered-header {
                text-align: center;
                margin-top: -50px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    COLENDUDERDEVICE.markdown(
        """
        <style>
            .centered-header {
                text-align: center;
                margin-top: -50px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    # Render the level 3 header with the unique class
    colAdTech.markdown(
        "<h3 class='centered-header'>" + human_formatCO2(int(round(AdTechImpact, 0))) + "CO2e" + "</h3>",
        unsafe_allow_html=True)
    colDATA.markdown(
        "<h3 class='centered-header'>" + human_formatCO2(int(round(DataCenterImpact, 0))) + "CO2e" + "</h3>",
        unsafe_allow_html=True)
    colTRANSMISSION.markdown(
        "<h3 class='centered-header'>" + human_formatCO2(
            int(round(DeviceTransmissionEnergy, 0))) + "CO2e" + "</h3>",
        unsafe_allow_html=True)
    COLENDUDERDEVICE.markdown(
        "<h3 class='centered-header'>" + human_formatCO2(int(round(DeviceImpact, 0))) + " CO2e" + "</h3>",
        unsafe_allow_html=True)
    sum = DataCenterImpact + DeviceTransmissionEnergy + DeviceImpact + AdTechImpact
    colAdTech2, colDATA2, colTRANSMISSION2, COLENDUDERDEVICE2 = st.columns([0.8, 0.8, 0.8, 1])
    colAdTech2.markdown(
        """
        <style>
            .centered-header {
                text-align: center;
                margin-top: -12px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    colDATA2.markdown(
        """
        <style>
            .centered-header {
                text-align: center;
                margin-top: -12px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    colTRANSMISSION2.markdown(
        """
        <style>
            .centered-header {
                text-align: center;
                margin-top: -12px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    COLENDUDERDEVICE2.markdown(
        """
        <style>
            .centered-header {
                text-align: center;
                margin-top: -12px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
    AdTechPurcent = int(round(AdTechImpact * 100 / sum, 2))
    DataCenterPurcent = int(round(DataCenterImpact * 100 / sum, 2))
    DeviceTransmissionPurcent = int(round(DeviceTransmissionEnergy * 100 / sum, 2))
    DevicePurcent = int(round(DeviceImpact * 100 / sum, 2))
    sumDifference = 100 - (AdTechPurcent + DataCenterPurcent + DeviceTransmissionPurcent + DevicePurcent)
    if sumDifference > 0:
        DataCenterPurcent = DataCenterPurcent + 1
        sumDifference = sumDifference - 1
    if sumDifference > 0:
        DeviceTransmissionPurcent = DeviceTransmissionPurcent + 1
        sumDifference = sumDifference - 1
    colAdTech2.markdown(
        "<h4 class='centered-header'>" + str(AdTechPurcent) + " % of the impact" + "</h4>",
        unsafe_allow_html=True)
    colDATA2.markdown(
        "<h4 class='centered-header'>" + str(DataCenterPurcent) + " % of the impact" + "</h4>",
        unsafe_allow_html=True)
    colTRANSMISSION2.markdown(
        "<h4 class='centered-header'>" + str(DeviceTransmissionPurcent) + " % of the impact" + "</h4>",
        unsafe_allow_html=True)
    COLENDUDERDEVICE2.markdown(
        "<h4 class='centered-header'>" + str(DevicePurcent) + " % of the impact" + "</h4>",
        unsafe_allow_html=True)
    st.markdown("""---""")
    st.write("### Conversion Rates KPIs")
    st.write(" ")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="CO2e Per Impression", value=human_formatCO2(round(co2_total /imps, 2)) + "CO2e",
                help="Average quantity of CO2e emitted by an impression")
    col2.metric(label="CO2e Per Viewed Impression", value=human_formatCO2(round(co2_total / viewed_imps, 2)) + "CO2e",
                help="Average quantity of CO2e emitted by an viewed impression")
    if clicks == 0: clicks = 1
    col3.metric(label="CO2e Per Click", value=human_formatCO2(co2_total / clicks) + "CO2e",
                help="Average quantity of CO2e emitted by a click")
    col4.metric(label="CO2e Per $ Spent", value=human_formatCO2(co2_total / budget_paid) + "CO2e",
                help="Average quantity of CO2e emitted by $ spent")
    df_sum_by_day["co2PerViewedImp"] = df_sum_by_day["co2total"] / df_sum_by_day["viewed_imps"]
    data_options = {
        "gCO2 Per Impression": ("co2PerImp", "gco2e Per Impression"),
        "gCO2 Per Viewed Impression": ("co2PerViewedImp", "gco2e Per Viewed Impression"),
        "gCO2 Per $ Spent": ("co2Per$Spent", "gco2e Per $ Spent"),
        "gCO2 Per Click": ("co2PerClick", "gco2e Per Click"),
    }
    st.write(" ")
    selected_data = st.selectbox("Select data to display:",
                                 options=["gCO2 Per Impression","gCO2 Per Viewed Impression", "gCO2 Per Click","gCO2 Per $ Spent"])

    # Get the selected column name and label
    column_name, y_label = data_options[selected_data]
    # Create the plot
    fig2 = px.line(
        df_sum_by_day.round(3),
        x="day",
        y=column_name,
        labels={"day": "Date", column_name: y_label},
        title=f"Daily {selected_data}"
    )
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
    st.markdown("""---""")
    st.write("### Campaigns Overview")
    dfBrandAll = df.groupby(['line_item']).sum(numeric_only=True).reset_index()
    dfBrandAll = dfBrandAll.sort_values(by=['co2total'], ascending=False)

    top_brands = dfBrandAll.head(10)
    other_co2 = dfBrandAll.iloc[10:]['co2total'].sum()
    other_imps = dfBrandAll.iloc[10:]['imps'].sum()
    other_clicks = dfBrandAll.iloc[10:]['clicks'].sum()
    other_cost = dfBrandAll.iloc[10:]['spend'].sum()
    st.dataframe(top_brands, use_container_width=True)
    st.markdown("""---""")
    # Use the campaign name from the session state
    st.write("### CO2e equivalence to real life")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    col1, col2, col3 = st.columns([1, 1, 1])
    co2total = round(df["co2total"].sum(), 2)
    col1.metric(label="Years in Phones Lifespan " + emoji.emojize(":iphone:"),
                value=ajouter_espace_milliers(str(round(co2total / 31020, 1)) + " Years"))
    col2.metric(label="Hours Spent on Netflix " + emoji.emojize(":tv:"),
                value=ajouter_espace_milliers(str(round(co2total / 55, 1)) + " Hours"))
    col3.metric(label="Kilometers in a Thermal Car " + emoji.emojize(":car:"),
                value=ajouter_espace_milliers(str(round(co2total / 110, 1)) + " Km"))
    col1.write('31.02 kgCO2e per phone per year')
    col2.write('55 gCO2e per hour of Netflix')
    col3.write('110 gCO2e per km in a thermal car')
    st.write(" ")
    st.write(" ")
    st.write(" ")

    ########### Campaign Performance Analysis

if navigation == "Campaign Performance Analysis":
    imps,viewed_imps,clicks,co2total=df["imps"].sum(),df["viewed_imps"].sum(),df["clicks"].sum(),df["co2total"].sum()
    st.write("---")
    st.write("### Volumes")
    col1, col2, col3 = st.columns(3)

    col1.metric(label="Impressions", value=human_format(imps),
                help="Number of impressions delivered")
    col2.metric(label="Budget", value=human_format(budget_paid).lower() + "$",
                help="Already paid budget on the total ")
    col3.metric(label="CO2e Emissions", value=human_formatCO2(co2_total),
                help="Total CO2e emitted by the campaign")
    st.markdown("""---""")
    st.write("### Total per KPI")
    # TODO round (1) for co2e
    data_options = {
        "CO2e Emissions": ("co2total", "kgCO2e Emissions"),
        "Impressions": ("imps", "Impressions"),
        "Viewable Impressions": ("viewed_imps", "Viewable Impressions"),
        "Budget Spent ($)": ("spend", "Budget Spent ($)"),
        "Viewability Rate (%)": ("viewability_rate_calculated", "Viewability Rate"),
        "Clicks": ("clicks", "Clicks"),
    }
    st.write("" "")
    selected_data = st.selectbox("Select data to display:",
                                 options=["Impressions", "Viewable Impressions", "Clicks","CO2e Emissions",
                                          "Budget Spent ($)", "Viewability Rate (%)"])

    # Get the selected column name and label
    column_name, y_label = data_options[selected_data]
    df_sum_by_day["viewability_rate_calculated"] = df_sum_by_day["viewed_imps"]/df_sum_by_day["imps"]
    # Create the plot
    fig2 = px.line(
        df_sum_by_day.round(2),
        x="day",
        y=column_name,
        labels={"day": "Date", column_name: y_label},
        title=f"Daily {selected_data}",
    )
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    st.markdown("""---""")
    st.write("### Devices ")
    st.write(" ")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="CO2e by Mobile Phones", value=human_formatCO2(
        dfSumByDevice[dfSumByDevice['device_type'] == 'mobile phones'].sum()["co2total"]) + "CO2e",
                help="Average quantity of CO2e emitted on mobile phones")

    col2.metric(label="CO2e by Desktops & Laptops", value=human_formatCO2(
        dfSumByDevice[dfSumByDevice['device_type'] == 'desktops & laptops'].sum()["co2total"]) + "CO2e",
                help="Average quantity of CO2e emitted on desktops & laptops")

    col3.metric(label="CO2e by Tablets", value=human_formatCO2(
        dfSumByDevice[dfSumByDevice['device_type'] == 'tablets'].sum()["co2total"]) + "CO2e",
                help="Average quantity of CO2e emitted on tablets")
    col4.metric(label="CO2e by Other Devices", value=human_formatCO2(dfSumByDevice[(dfSumByDevice[
                                                                                        'device_type'] != 'mobile phones') & (
                                                                                           dfSumByDevice[
                                                                                               'device_type'] != 'desktops & laptops') & (
                                                                                           dfSumByDevice[
                                                                                               'device_type'] != 'tablets')].sum()[
                                                                         "co2total"]) + "CO2e",
                help="Average quantity of CO2e emitted on other devices")

    fig = px.bar(dfSumByDevice.round(3), x='device_type', y='co2total', text='co2total',
                 labels={'device_type': 'Device Type', 'co2total': 'CO2 Emissions'},
                 title="Total CO2e Emissions by Device")

    formatted_values = [human_formatCO2(co2) for co2 in dfSumByDevice['co2total']]

    # Mettre à jour le texte des barres avec les valeurs formatées
    fig.update_traces(text=formatted_values)

    # Afficher le graphique
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("""---""")
    if media_type(df) == "video" or media_type(df) == "both":
        st.write("### By Video Context ")
        st.dataframe(df_video_context, use_container_width=True)
    if media_type(df) == "banner" or media_type(df) == "both":
        st.write("### By Banner Context ")
        st.dataframe(df_banner_context[
                         ["Banner Size", "Impressions", "Viewed Impressions", "Clicks", "Curator Total Cost",
                          "Impression per $ Spent", "CO2e Per Click"]],
                     use_container_width=True)

    st.write("---")
    st.write("### Countries")
    st.write(" ")
    st.write("Carbon Intensity depending on the country")
    st.write(" ")
    # TODO add a table or a map
    # Obtention des métriques pour chaque pays
    df_country_co2 = get_each_country_co2(df)
    # Initialisation de la liste data
    data = []

    # Mapping des intensités de carbone pour chaque pays
    carbon_intensity = {
        "France": "Very Low",
        "Germany": "High",
        "Spain": "Low",
        "Italy": "Medium",
        "United Kingdom": "Medium",
        "Belgium": "Low"
    }

    country_mapping = {
        'ES': 'Spain',
        'GB': 'United Kingdom',
        'FR': 'France',
        'DE': 'Germany',
        'IT': 'Italy',
        'BE': 'Belgium'
    }

    for index, row in df_country_co2.iterrows():
        country_code = row['geo_country']
        country_name = country_mapping[country_code]

        data.append({
            "Country": country_name,
            "Volume of emissions (CO2e)": human_formatCO2(row['co2total']),
            "Carbon Intensity": carbon_intensity[country_name],
            "Impressions": row['imps'],
            "Clicks": row['clicks'],
            "Budget Spent": row["spend"],
            "CO2e per Impression": human_formatCO2(row['co2total'] / row['viewed_imps']),
            "Viewability Rate": str(round(row['viewed_imps'] / row['imps'] * 100, 1)) + "%"
        })

    # Création du DataFrame
    df_country = pd.DataFrame(data)

    # Arrondissement de la colonne 'Budget Spent' à deux chiffres après la virgule
    df_country["Budget Spent"] = df_country["Budget Spent"].round(2)

    # Ajout du signe dollar
    df_country["Budget Spent"] = df_country["Budget Spent"].apply(lambda x: f"{x} $")

    # Affichage du DataFrame dans Streamlit
    st.dataframe(df_country.reset_index(drop=True), use_container_width=True)
if navigation == "Recommandations":

    st.write('')
    st.write('')
    st.title('Recommandations')
    st.write('')

if navigation == "Methodology":
    st.write('---')
    colSRI, colGM = st.columns(2)
    colSRI.write('')
    colSRI.write('')
    colSRI.write(' ### SRI Methodology :')
    colSRI.write('')
    colSRI.write('')
    colSRI.write(
        "The SRI methodology for calculating the impact of an online advertisement is based on a service approach that evaluates the carbon footprint of the advertising campaign as a whole, including its distribution to each terminal. ")
    colSRI.write(
        "This approach includes three steps: collecting data on the advertising formats used, creating a measurement tool based on this data, and using this tool to assess the carbon impact of each campaign. ")
    colSRI.write(
        "The impact is calculated by taking into account the manufacturing, consumption, and end of life of the three parts involved in providing the service: the terminals used for logging in, the networks that deliver the information, and the servers that store the data and respond to requests.")
    colGM.write('')
    colGM.write('')
    colGM.write(' ### SRI + GM Methodology :')
    colGM.write('')
    colGM.write('')
    colGM.write('The methodology of Greenmetrics is rooted in the principles of the SRI methodology.')
    colGM.write(
        'It enhances the SRI methodology by incorporating the concept of energy consumed by the device during website loading, which varies based on the type of content loaded and the device used.')
    colGM.write(
        "With its ISO 14067 certification, Greenmetrics is capable of providing an accurate estimation of the energy required, pinpointing the exact contribution of the advertisement.")
