import streamlit as st
import requests
import os

def estimate_solar_financing(area_kwh_month, home_sqft, cost_per_watt=None,
                              financing_rate=4.5, loan_years=20, tax_credit=0.30):
    """
    Estimates solar system cost and monthly payment based on electricity usage and home size.

    Inputs:
        area_kwh_month (float): user's average monthly electricity usage in kWh
        home_sqft (float): size of the home in square feet
        cost_per_watt (float): installed cost per watt ($/W). If None, uses national average.
        financing_rate (float): annual loan interest rate (in %)
        loan_years (int): loan term duration in years
        tax_credit (float): federal solar Investment Tax Credit (ITC) portion (e.g., 0.30 for 30%)

    Returns:
        dict with keys: system_size_kw, gross_cost, net_cost, monthly_payment
    """

    # Constants / benchmarks
    AVG_USAGE_PER_KW = 855  # average US household monthly kWh
    AVG_COST_PER_WATT = cost_per_watt or 3.00  # $/W range $2.74–$3.30

    # Derive system size needed (kW)
    normalized_usage = area_kwh_month / AVG_USAGE_PER_KW
    system_kw = normalized_usage * 11  # average system ~11 kW

    # Cost calculations
    gross_cost = system_kw * 1000 * AVG_COST_PER_WATT
    net_cost = gross_cost * (1 - tax_credit)

    # Loan amortization monthly payment
    r = financing_rate / 100 / 12
    n = loan_years * 12
    monthly_payment = (net_cost * r) / (1 - (1 + r)**(-n))

    return {
        "system_size_kw": round(system_kw, 2),
        "gross_cost": round(gross_cost, 2),
        "net_cost_after_incentives": round(net_cost, 2),
        "estimated_monthly_payment": round(monthly_payment, 2)
    }
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
| [🌟 **PSCCU Solar Financing Options (Preferred)**](https://www.psccu.org/loans/solar-loans.html) | 15 yr | 4.24% | ~$187/mo |

---

📎 Click one of the partners to apply, or reach out to your certified installer for help.

📩 Once you’re approved, this section will connect to real-time financing tools and monthly breakdowns.
    """)
