import streamlit as st
import requests
import os
from fpdf import FPDF

st.set_page_config(page_title="SolarMan - Full App", layout="wide")

tab1, tab2, tab3 = st.tabs(["🏠 Home", "📊 Estimate", "💰 Financing Options"])

with tab1:
    st.title("🔆 SolarMan")
    st.subheader("Home")
    st.write("Welcome to the SolarMan App! Use the tabs above to explore your solar system potential, calculate monthly loan payments, and connect with a certified installer.")

with tab2:
    st.header("📊 Estimate Your Solar Potential")
    address = st.text_input("Enter your home address to calculate your solar potential:")

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
                kw_capacity = area_m2 * 0.15
                sunlight_hours = potential.get("maxSunshineHoursPerYear", 1600) / 365

                st.markdown("### ☀️ Solar Estimate Summary")
                st.write(f"**Max system size:** {kw_capacity:.2f} kW")
                st.write(f"**Estimated max panels:** {panels}")
                st.write(f"**Average daily sunlight:** {sunlight_hours:.1f} hours/day")

                monthly_kwh = kw_capacity * sunlight_hours * 30
                st.write(f"**Estimated monthly production:** {monthly_kwh:.0f} kWh/month")

                bill_kwh = st.number_input("📄 Optional: Enter your monthly utility usage (kWh)", min_value=0)
                if bill_kwh > 0:
                    needed_panels = round((bill_kwh / (sunlight_hours * 30)) / 0.4)
                    st.success(f"You'd need approximately **{needed_panels} panels** to offset your bill.")

                    # Generate PDF
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    pdf.cell(200, 10, txt="Solar Estimate Report", ln=True, align="C")
                    pdf.ln(10)
                    pdf.multi_cell(200, 10, txt=f"""Address: {address}
Latitude: {lat}
Longitude: {lon}
Max System Size: {kw_capacity:.2f} kW
Estimated Panels: {panels}
Average Daily Sunlight: {sunlight_hours:.1f} hrs/day
Monthly Production: {monthly_kwh:.0f} kWh/month
Bill Usage: {bill_kwh} kWh
Panel Count to Offset: {needed_panels}""")
                    pdf_path = "/mnt/data/solar_estimate.pdf"
                    pdf.output(pdf_path)
                    st.download_button("📄 Download PDF Estimate", data=open(pdf_path, "rb"), file_name="solar_estimate.pdf", mime="application/pdf")

            else:
                st.error("No solar data available for this location.")
        else:
            st.error("Address not found.")
    elif not maps_key or not solar_key:
        st.warning("API keys not found. Add them in Streamlit Cloud Secrets.")
    else:
        st.info("Enter your address to get a solar estimate.")

with tab3:
    st.header("💰 Financing Options")
    st.markdown("""
### 📌 Loan Examples

| Loan Provider | Term | Rate | Est. Monthly for $25,000 |
|---------------|------|------|---------------------------|
| [GoodLeap](https://www.goodleap.com/) | 25 yr | 4.99% | ~$145/mo |
| [Sunlight Financial – Homeowner Application](https://sunlightfinancial.com/homeowners/) | 20 yr | 5.49% | ~$165/mo |
| [🌟 PSCCU Solar Financing Options (Preferred)](https://www.psccu.org/loans/solar-loans.html) | 15 yr | 4.24% | ~$187/mo |

---
📎 Click one of the partners to apply, or reach out to your certified installer for help.
📩 Once you’re approved, this section will connect to real-time financing tools and monthly breakdowns.
    """)
