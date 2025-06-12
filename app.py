import streamlit as st

# Set app layout
st.set_page_config(page_title="SolarMan", layout="centered")

# App title
st.title("☀️ SolarMan Solar Quote Estimator")

# Homeowner inputs
address = st.text_input("🏠 Enter your home address:")
roof_sqft = st.number_input("📐 Available roof square footage:", min_value=0)

# Estimations
sqft_per_panel = 17.5
watts_per_panel = 400

if roof_sqft > 0:
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
else:
    st.info("Enter roof size to generate your quote.")
