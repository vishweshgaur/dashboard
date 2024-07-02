import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Set the layout of the dashboard
st.set_page_config(layout="wide", page_title="Dashboard", page_icon="📊")

# Load the dataset
data = pd.read_csv('data.csv')

# Sidebar with switches and sliders
with st.sidebar:
    st.title("Controls")
    pump_switch = st.checkbox("Pump Switch", value=False)
    pump_seconds = st.slider("Pump Seconds", min_value=0, max_value=60, value=0)
    reset_slave = st.button("Reset Slave")
    generator_switch = st.checkbox("Generator Switch", value=False)

# Main dashboard
st.title("Dashboard")

# Display the data (assuming your CSV has relevant columns)
# Example: Displaying the first few rows of the dataset
st.subheader("Dataset Overview")
st.write(data.head())

# Assuming the dataset has columns similar to the dummy data used before
last_reading_time = data['last_reading_time'].iloc[0]
site_status = data['site_status'].iloc[0]
voltages = data[['voltage1', 'voltage2', 'voltage3', 'voltage4']].iloc[0].tolist()
door_status = data['door_status'].iloc[0]
fuel_level = data['fuel_level'].iloc[0]
gauge_value = data['gauge_value'].iloc[0]
temperature = data['temperature'].iloc[0]
humidity = data['humidity'].iloc[0]

# Columns for layout
col1, col2, col3 = st.columns(3)

# Display the data
with col1:
    st.metric("Last Reading Time", last_reading_time)
    st.metric("Site Status", site_status, delta="Active", delta_color="inverse")
    st.metric("Main Voltage 1", f"{voltages[0]} V")
    st.metric("Main Voltage 2", f"{voltages[1]} V")

with col2:
    st.metric("Main Voltage 3", f"{voltages[2]} V")
    st.metric("Main Voltage 4", f"{voltages[3]} V")
    st.metric("Door Status", door_status, delta="Closed", delta_color="inverse")
    st.metric("Generator Fuel Level", f"{fuel_level} %")

# Create Gauge
fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number",
    value=gauge_value,
    title={"text": "Gauge"},
    gauge={"axis": {"range": [0, 1023]},
           "bar": {"color": "blue"}}
))

with col3:
    st.plotly_chart(fig_gauge, use_container_width=True)

# Create charts for temperature and humidity
time = pd.date_range(start="2022-01-01", periods=60, freq="min")
temp_data = data['temperature'].tolist()
humidity_data = data['humidity'].tolist()

fig_temp = go.Figure()
fig_temp.add_trace(go.Scatter(x=time, y=temp_data, mode="lines", name="Temperature", line=dict(color='firebrick', width=2)))
fig_temp.update_layout(title="Temperature Over Time", xaxis_title="Time", yaxis_title="Temperature (°C)", template="plotly_dark")

fig_humidity = go.Figure()
fig_humidity.add_trace(go.Scatter(x=time, y=humidity_data, mode="lines", name="Humidity", line=dict(color='royalblue', width=2)))
fig_humidity.update_layout(title="Humidity Over Time", xaxis_title="Time", yaxis_title="Humidity (%)", template="plotly_dark")

col4, col5 = st.columns(2)
with col4:
    st.plotly_chart(fig_temp, use_container_width=True)

with col5:
    st.plotly_chart(fig_humidity, use_container_width=True)

# Create bar chart for voltages
fig_bar = px.bar(x=["Voltage 1", "Voltage 2", "Voltage 3", "Voltage 4"], y=voltages,
                 labels={'x': 'Voltage Type', 'y': 'Voltage (V)'}, title="Voltage Levels")
fig_bar.update_traces(marker_color='indianred')

# Create pie chart for site status
fig_pie = px.pie(values=[1], names=[site_status], title="Site Status")
fig_pie.update_traces(marker=dict(colors=['royalblue']))

# Create area chart for fuel level over time
fuel_time = pd.date_range(start="2022-01-01", periods=60, freq="min")
fuel_level_data = data['fuel_level'].tolist()

fig_area = go.Figure()
fig_area.add_trace(go.Scatter(x=fuel_time, y=fuel_level_data, fill='tozeroy', mode='none', name='Fuel Level', fillcolor='green'))
fig_area.update_layout(title="Fuel Level Over Time", xaxis_title="Time", yaxis_title="Fuel Level (%)", template="plotly_dark")

col6, col7, col8 = st.columns(3)

with col6:
    st.plotly_chart(fig_pie, use_container_width=True)

with col7:
    st.plotly_chart(fig_bar, use_container_width=True)

with col8:
    st.plotly_chart(fig_area, use_container_width=True)

# Display pump and generator switch status
st.markdown("### Device Status")
col9, col10 = st.columns(2)
with col9:
    pump_status = "ON" if pump_switch else "OFF"
    st.metric("Pump Switch", pump_status)

with col10:
    generator_status = "ON" if generator_switch else "OFF"
    st.metric("Generator Switch", generator_status)

# Add footer with some styling
st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #333;
        color: white;
        text-align: center;
        padding: 10px 0;
    }
    </style>
    <div class="footer">
        <p>Dashboard by Your Name</p>
    </div>
""", unsafe_allow_html=True)

data = pd.read_csv('data/data.csv')

