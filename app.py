import streamlit as st
import requests
import os
from fpdf import FPDF

st.set_page_config(page_title="SolarMan - PDF Quote Generator", layout="centered")
st.title("☀️ SolarMan - Solar Quote + PDF")

address = st.text_input("Enter your home address:")
usage_kwh = st.number_input("Monthly electricity usage (kWh):", min_value=0, value=800)

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

def generate_pdf(address, size_kw, est_monthly_kwh, monthly_payment):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Solar Quote Estimate", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Address: {address}", ln=True)
    pdf.cell(200, 10, txt=f"System Size: {size_kw:.2f} kW", ln=True)
    pdf.cell(200, 10, txt=f"Estimated Monthly Production: {est_monthly_kwh:.0f} kWh", ln=True)
    pdf.cell(200, 10, txt=f"Estimated Monthly Loan Payment: ${monthly_payment:.2f}", ln=True)
    pdf_output = "/tmp/solar_quote.pdf"
    pdf.output(pdf_output)
    return pdf_output

if address and maps_key and solar_key:
    lat, lon = geocode_address(address, maps_key)
    if lat and lon:
        st.success(f"📍 Location found: ({lat:.5f}, {lon:.5f})")
        solar_data = get_solar_data(lat, lon, solar_key)
        if solar_data and "solarPotential" in solar_data:
            potential = solar_data["solarPotential"]
            area_m2 = potential.get("maxArrayAreaMeters2", 0)
            kw_capacity = area_m2 * 0.15
            sunlight_hours = potential.get("maxSunshineHoursPerYear", 1600) / 365
            est_monthly_kwh = kw_capacity * sunlight_hours * 30
            cost_per_watt = 3.50
            gross_cost = kw_capacity * 1000 * cost_per_watt
            tax_credit = 0.30
            net_cost = gross_cost * (1 - tax_credit)
            monthly_payment = (net_cost * 0.045) / 12 / (1 - (1 + 0.045 / 12) ** (-20 * 12))

            st.markdown("### ☀️ Solar Estimate Summary")
            st.write(f"System size: **{kw_capacity:.2f} kW**")
            st.write(f"Estimated monthly production: **{est_monthly_kwh:.0f} kWh**")
            st.write(f"Estimated gross system cost: **${gross_cost:,.2f}**")
            st.write(f"Estimated monthly loan payment: **${monthly_payment:.2f}**")

            pdf_file = generate_pdf(address, kw_capacity, est_monthly_kwh, monthly_payment)
            with open(pdf_file, "rb") as f:
                st.download_button("📄 Download PDF Quote", f, file_name="solar_quote.pdf")
        else:
            st.error("⚠️ No solar data available for this location.")
    else:
        st.error("❌ Could not find location. Please check the address.")
elif not maps_key or not solar_key:
    st.warning("⚠️ Missing API keys. Add them under Streamlit secrets.")
else:
    st.info("Enter your address to get started.")
