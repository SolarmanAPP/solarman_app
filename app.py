import streamlit as st
import requests
import os

st.set_page_config(page_title="SolarMan - Quick Estimate", layout="centered")
st.title("☀️ SolarMan - Solar Quote Generator")

address = st.text_input("Enter your home address:")

maps_key = os.getenv("GOOGLE_MAPS_API_KEY")
solar_key = os.getenv("GOOGLE_SOLAR_API_KEY")

def geocode_address(address, maps_key):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": maps_key}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
    return None, None

def get_solar_data(lat, lon, solar_key):
    url = f"https://solar.googleapis.com/v1/buildingInsights:findClosest?location.latitude={lat}&location.longitude={lon}&key={solar_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

if address and maps_key and solar_key:
    lat, lon = geocode_address(address, maps_key)
    if lat and lon:
        st.success(f"📍 Location found: ({lat:.5f}, {lon:.5f})")
        solar_data = get_solar_data(lat, lon, solar_key)
        if solar_data and "solarPotential" in solar_data:
            potential = solar_data["solarPotential"]
            panels = potential.get("maxArrayPanelsCount", "N/A")
            kw_capacity = potential.get("maxArrayAreaMeters2", 0) * 0.15
            sunlight_hours = potential.get("maxSunshineHoursPerYear", 1600) / 365

            st.markdown("### ☀️ Solar Estimate Summary")
            st.write(f"Max system size: **{kw_capacity:.2f} kW**")
            st.write(f"Max panel count: **{panels}**")
            st.write(f"Average sun hours/day: **{sunlight_hours:.1f}**")

            monthly_kwh = kw_capacity * sunlight_hours * 30
            st.write(f"Estimated monthly production: **{monthly_kwh:.0f} kWh/month**")
        else:
            st.error("⚠️ No solar data available for this location.")
    else:
        st.error("❌ Could not find location. Please double-check the address.")
elif not maps_key or not solar_key:
    st.warning("⚠️ API keys missing. Add them to Streamlit secrets.")
else:
    st.info("Enter an address to see solar potential.")
