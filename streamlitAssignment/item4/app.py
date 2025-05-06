# api_data_display.py
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.title("🌍 COVID-19 Statistics Viewer")
st.subheader("Live Data from disease.sh API")

# API URL (public API, no key required)
API_URL = "https://disease.sh/v3/covid-19/countries"

# Sidebar country selector
st.sidebar.header("🌐 Options")
selected_country = st.sidebar.selectbox("Select a country", ["Philippines", "USA", "India", "Brazil", "Russia"])

# Fetch API data
response = requests.get(API_URL)
if response.status_code == 200:
    data = response.json()
    df = pd.json_normalize(data)

    # Filter selected country
    country_data = df[df['country'] == selected_country].iloc[0]

    # Display key metrics
    st.header(f"🇵🇭 COVID-19 Stats: {selected_country}")
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Cases", f"{country_data['cases']:,}")
    col2.metric("Total Deaths", f"{country_data['deaths']:,}")
    col3.metric("Total Recovered", f"{country_data['recovered']:,}")

    st.markdown("---")

    # Prepare data for charts
    chart_data = {
        'Active': country_data['active'],
        'Recovered': country_data['recovered'],
        'Deaths': country_data['deaths'],
        'Today Cases': country_data['todayCases'],
        'Today Deaths': country_data['todayDeaths']
    }
    chart_df = pd.DataFrame(list(chart_data.items()), columns=['Category', 'Count'])

    st.subheader("📊 COVID-19 Breakdown Charts")

    # Chart 1: Bar Chart
    st.write("### Bar Chart")
    st.bar_chart(chart_df.set_index('Category'))

    # Chart 2: Line Chart
    st.write("### Line Chart")
    st.line_chart(chart_df.set_index('Category'))

    # Chart 3: Area Chart
    st.write("### Area Chart")
    st.area_chart(chart_df.set_index('Category'))

    # Chart 4: Pie Chart (matplotlib)
    st.write("### Pie Chart")
    fig, ax = plt.subplots()
    ax.pie(chart_df['Count'], labels=chart_df['Category'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    # Chart 5: Table Chart (styled table)
    st.write("### Data Table")
    st.dataframe(chart_df.style.highlight_max(axis=0, color='lightgreen'))

else:
    st.error("Failed to fetch data from API. Please try again later.")
