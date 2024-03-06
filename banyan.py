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
navigation = st.sidebar.radio("Go to", ["Overview"])
for i in range(10):  # avant c'était 30
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
if "edit_expander" not in st.session_state:
    st.session_state.edit_expander = False
edit_button_container = st.sidebar.markdown(
    '<div id="edit-button-container"></div>',
    unsafe_allow_html=True
)
df, first_day, last_day = load_df()
st.write('')
df, df_sum_by_day = restrict_all_dataframes(df)
# df_video_context, df_banner_context = get_df_context(df)
col1, col2 = st.columns([4, 1])
col1.write("## Hi Thibault, welcome back!")
col2.write('')
col2.write('')
col2.write('')
now_minus_1 = datetime.datetime.now() - timedelta(hours=1) - timedelta(minutes=12)
col2.markdown("###### " + str("Last update : " + str(now_minus_1.strftime("%Y-%m-%d %H:%M:%S"))))
st.write('')
st.write('')
st.write(
    """Banyan provides an overview of the environmental impact of your advertising campaigns and helps you identify the most eco-friendly options.""")
# Get the dataframes restricted to the selected date range and the indicators updated
# Deal restriction
st.write('')
with st.expander("Campaign & Date"):
    col1, col2 = st.columns([1, 1])
col1.write('### Campaign')
deal = col1.selectbox("Select a Campaign ID", get_deals_list(df))
df = restrict_by_deal(df, deal)
col2.write('### Date')
start_range, end_range = render_calendar(col2, first_day, last_day)
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
df = restrict_by_day(df, start_range, end_range)
############ OVERVIEW
if navigation == "Overview":
    st.markdown("""---""")
    col1, col2 = st.columns([5, 1])
    col1.markdown(str('## Overview of : ' + "SFR"))
    m = col2.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: rgb(31, 214, 85);
        color:black;
    }
    </style>""", unsafe_allow_html=True)

    col2.button(":white[Offset my emissions !]", use_container_width=True, on_click=open_webpage)
    # if col2.button(label=':green[Offset my emissions !]', use_container_width=True):
    #   navigation = "Offset my emissions"
    st.write("")
    st.write("")
    ######## Setting KPIs
    col1, col2, col3, col4 = st.columns(4)
    co2_total = round(df["co2total"].sum(), 2)
    imps = df["imps"].sum()
    viewed_imps = df["viewed_imps"].sum()
    budget_paid = df["spend"].sum()
    clicks = df["clicks"].sum()
    col1.metric(label="Impressions", value=human_format(imps),
                help="Number of impressions delivered")
    col2.metric(label="CO2e Emissions", value=human_formatCO2(co2_total),
                help="Total CO2e emitted by the campaign", delta_color='off')
    col3.metric(label="CO2e / Impression", value=human_formatCO2(round(co2_total / imps, 2)) + "CO2e",
                help="Total CO2e divided by the number of impressions")
    col4.metric(label="Cost", value=human_format(budget_paid).lower() + "$",
                help="Already spent budget on the total", delta_color='inverse')
    col1.write(str(round((viewed_imps/imps)*100,1))+" % of viewed impressions")
    col4.write("Total budget spent so far")
    col2.write(str(round(co2_total/clicks,1))+" gCO2e per Click")
    col3.write("Average CO2e per impression")
    st.write("---")
    AdTechImpact, DeviceTransmissionEnergy, DeviceImpact = df['CO2AdTech'].sum(), df['CO2Transmission'].sum(), df['CO2Device'].sum()
    colPHOTO, colEMPTY, colENERGY = st.columns([1.5, 0.2, 0.7])
    colPHOTO.write("### CO2 Impact Breakdown")
    colPHOTO.image("assets/graph_no_dc.png", output_format='PNG', use_column_width=True, width=6840)
    colAdTech, colTRANSMISSION, COLENDUDERDEVICE = colPHOTO.columns([0.75, 0.75, 1])
    colAdTech.write(" ")
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
    colTRANSMISSION.markdown(
        "<h3 class='centered-header'>" + human_formatCO2(
            int(round(DeviceTransmissionEnergy, 0))) + "CO2e" + "</h3>",
        unsafe_allow_html=True)
    COLENDUDERDEVICE.markdown(
        "<h3 class='centered-header'>" + human_formatCO2(int(round(DeviceImpact, 0))) + " CO2e" + "</h3>",
        unsafe_allow_html=True)
    sum =  DeviceTransmissionEnergy + DeviceImpact + AdTechImpact
    #  colAdTech2,col00, colTRANSMISSION2, COLENDUDERDEVICE2 = colPHOTO.columns([0.78,0.05,0.9, 1])
    colAdTech.markdown(
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
    colTRANSMISSION.markdown(
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
    COLENDUDERDEVICE.markdown(
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
    DeviceTransmissionPurcent = int(round(DeviceTransmissionEnergy * 100 / sum, 2))
    DevicePurcent = int(round(DeviceImpact * 100 / sum, 2))
    sumDifference = 100 - (AdTechPurcent + DeviceTransmissionPurcent + DevicePurcent)
    if sumDifference > 0:
        sumDifference = sumDifference - 1
    if sumDifference > 0:
        DeviceTransmissionPurcent = DeviceTransmissionPurcent + 1
        sumDifference = sumDifference - 1
    colAdTech.markdown(
        "<h4 class='centered-header'>" + str(AdTechPurcent) + " % of the impact" + "</h4>",
        unsafe_allow_html=True)
    colTRANSMISSION.markdown(
        "<h4 class='centered-header'>" + str(DeviceTransmissionPurcent) + " % of the impact" + "</h4>",
        unsafe_allow_html=True)
    COLENDUDERDEVICE.markdown(
        "<h4 class='centered-header'>" + str(DevicePurcent) + " % of the impact" + "</h4>",
        unsafe_allow_html=True)
    colENERGY.write('### Energy Breakdown')
    share_nuclear = 24.59
    share_renewables = 42.74
    share_fossil = 32.67
    renewables_color = (39, 120, 81)
    nuclear_color = (37, 37, 135)
    fossil_color = (255, 205, 76)
    # create a plotly streamlit pie chart
    fig = go.Figure(data=[
        go.Pie(labels=['Renewables', 'Nuclear', 'Fossil'], values=[share_renewables, share_nuclear, share_fossil])])
    fig.update_traces(hoverinfo='label+percent', textinfo='label+percent', textfont_size=17,
                      marker=dict(colors=[f'rgb{renewables_color}', f'rgb{nuclear_color}', f'rgb{fossil_color}']))
    fig.update_layout(showlegend=False, margin=dict(l=0, r=0, t=17, b=0), height=330, width=320)
    colENERGY.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown("""---""")
    st.write("### Conversion Rates KPIs")
    st.write(" ")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="CO2e Per Impression", value=human_formatCO2(round(co2_total / imps, 2)) + "CO2e",
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
                                 options=["gCO2 Per Impression", "gCO2 Per Viewed Impression", "gCO2 Per Click",
                                          "gCO2 Per $ Spent"])

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
    st.write("---")
    st.write("### CO2e equivalence to real life")
    st.write(" ")
    st.write(" ")
    st.write(" ")
    col1, col2, col3,col4 = st.columns([1, 1, 1,1])
    co2total = round(df["co2total"].sum(), 2)
    col1.metric(label="Years in Phones Lifespan " + emoji.emojize(":iphone:"),
                value=ajouter_espace_milliers(str(round(co2total / 31020, 1)) + " Years"))
    col2.metric(label="Hours Spent on Netflix " + emoji.emojize(":tv:"),
                value=ajouter_espace_milliers(str(round(co2total / 55, 1)) + " Hours"))
    col3.metric(label="Kilometers in a Thermal Car " + emoji.emojize(":car:"),
                value=ajouter_espace_milliers(str(round(co2total / 110, 1)) + " Km"))
    col4.metric(label="Paris - New York " + emoji.emojize(":airplane:"),
                value=ajouter_espace_milliers(str(round(co2total / 1_750_000, 1)) + " round trips"))
    col1.write('31.02 kgCO2e per phone per year')
    col2.write('55 gCO2e per hour of Netflix')
    col3.write('110 gCO2e per km in a thermal car')
    col4.write('1.75 TCO2e per per passager')
    st.write(" ")
    st.write(" ")
    st.write(" ")