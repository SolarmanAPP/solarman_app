import streamlit as st
import requests
import os

st.set_page_config(page_title="SolarMan - Solar Estimate", layout="centered")

st.title("🔆 SolarMan: Solar Estimate Tool")

tabs = st.tabs(["🏠 Home", "📊 Estimate", "📎 Upload Utility Bill"])

with tabs[0]:
    st.header("Welcome to SolarMan")
    st.write("Use the tabs above to estimate your solar system potential or upload your utility bill.")

with tabs[1]:
    st.header("📊 Solar Potential Estimate")
    address = st.text_input("Enter your home address for solar analysis:")

    # Load secrets
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
                area_m2 = potential.get("maxArrayAreaMeters2", 0)
                kw_capacity = area_m2 * 0.15  # assume 150W/m²
                sunlight_hours = potential.get("maxSunshineHoursPerYear", 1600) / 365

                st.markdown("### ☀️ Solar Estimate Summary")
                st.write(f"**Max system size:** {kw_capacity:.2f} kW")
                st.write(f"**Estimated max panels:** {panels}")
                st.write(f"**Average daily sunlight:** {sunlight_hours:.1f} hours/day")

                monthly_kwh = kw_capacity * sunlight_hours * 30
                st.write(f"**Estimated monthly production:** {monthly_kwh:.0f} kWh/month")

                bill_kwh = st.number_input("📄 Optional: Enter your monthly utility usage (kWh)", min_value=0)
                if bill_kwh > 0:
                    needed_panels = round((bill_kwh / (sunlight_hours * 30)) / 0.4)  # 400W per panel estimate
                    st.success(f"You'd need approximately **{needed_panels} panels** to offset your bill.")
            else:
                st.error("No solar data available for this location.")
        else:
            st.error("Address not found.")
    elif not maps_key or not solar_key:
        st.warning("API keys not found. Add them in Streamlit Cloud Secrets.")
    else:
        st.info("Enter your address to get a solar estimate.")

with tabs[2]:
    st.header("📎 Upload Your Utility Bill")
    uploaded_file = st.file_uploader("Upload a PDF, image, or bill summary (for future AI processing):")
    if uploaded_file:
        st.success("✅ File uploaded. In a future release, we will analyze this to size your system automatically.")
