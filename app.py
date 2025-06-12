import streamlit as st
from fpdf import FPDF
import tempfile
import os
import requests

st.set_page_config(page_title="SolarMan", layout="centered")
st.title("☀️ SolarMan Solar Quote Estimator")

address = st.text_input("🏠 Enter your home address:")

def get_lat_lon_from_address(address, api_key):
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address, "key": api_key}
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            location = data["results"][0]["geometry"]["location"]
            return location["lat"], location["lng"]
    return None, None

def simulate_roof_sqft_from_coords(lat, lon):
    if lat is not None and lon is not None:
        return int(300 + abs(lat * lon) % 900)  # Simulate 300–1200 sqft
    return None

api_key = os.getenv("GOOGLE_MAPS_API_KEY")

sqft_per_panel = 17.5
watts_per_panel = 400

if address and api_key:
    lat, lon = get_lat_lon_from_address(address, api_key)
    if lat is not None:
        st.success(f"📍 Location found: ({lat:.5f}, {lon:.5f})")
        roof_sqft = simulate_roof_sqft_from_coords(lat, lon)
        st.markdown(f"### 📐 Estimated Roof Area from Google Maps: **{roof_sqft} sqft**")

        num_panels = roof_sqft / sqft_per_panel
        system_kw = round((num_panels * watts_per_panel) / 1000, 2)
        cost_per_watt = 3.50
        total_cost = round(system_kw * 1000 * cost_per_watt, 2)
        est_monthly = round(total_cost * 0.015, 2)

        st.markdown("### 🔧 System Estimate")
        st.write(f"System size: **{system_kw} kW**")
        st.write(f"Estimated total cost: **${total_cost:,.2f}**")

        st.markdown("### 💰 Financing Option")
        st.write(f"Est. monthly payment (20 years): **${est_monthly}/mo**")

        st.markdown("---")
        st.markdown("""**Northern Pacific Electric**  
WA License: NORTHPE759BS  
Walter Struckman  
📞 206-712-4212  
📧 wstruckmannpe@gmail.com""")

        if st.button("📄 Download Quote as PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="SolarMan Solar Quote", ln=True, align="C")
            pdf.ln(10)
            pdf.cell(200, 10, txt=f"Address: {address}", ln=True)
            pdf.cell(200, 10, txt=f"Lat/Lon: {lat:.5f}, {lon:.5f}", ln=True)
            pdf.cell(200, 10, txt=f"Roof Area (estimated): {roof_sqft} sqft", ln=True)
            pdf.cell(200, 10, txt=f"System Size: {system_kw} kW", ln=True)
            pdf.cell(200, 10, txt=f"Total Cost: ${total_cost:,.2f}", ln=True)
            pdf.cell(200, 10, txt=f"Est. Monthly Payment: ${est_monthly}/mo", ln=True)
            pdf.ln(10)
            pdf.cell(200, 10, txt="Installed by Northern Pacific Electric", ln=True)
            pdf.cell(200, 10, txt="WA License: NORTHPE759BS", ln=True)
            pdf.cell(200, 10, txt="Walter Struckman", ln=True)
            pdf.cell(200, 10, txt="Phone: 206-712-4212", ln=True)
            pdf.cell(200, 10, txt="Email: wstruckmannpe@gmail.com", ln=True)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                pdf.output(tmp_file.name)
                st.success("PDF generated!")
                with open(tmp_file.name, "rb") as f:
                    st.download_button("⬇️ Download PDF", data=f, file_name="solarman_quote.pdf", mime="application/pdf")
                os.remove(tmp_file.name)
    else:
        st.error("⚠️ Could not locate address. Please check the spelling.")
elif not api_key:
    st.warning("🚫 Google Maps API key is not set. Add it to Streamlit Secrets.")
else:
    st.info("Enter your home address to begin.")
