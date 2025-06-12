import streamlit as st

st.set_page_config(page_title="SolarMan App", layout="centered")

st.title("☀️ SolarMan Quote Generator")
st.write("Get your custom solar estimate instantly.")

# --- Homeowner Inputs ---
address = st.text_input("🏠 Enter your home address")
roof_sqft = st.number_input("📐 Estimated available roof square footage", min_value=0)

# --- System Size Estimate ---
sqft_per_panel = 17.5  # average panel size in sqft
watts_per_panel = 400
system_size_kw = round((roof_sqft / sqft_per_panel * watts_per_panel) / 1000, 2)

# --- Pricing Constants ---
base_cost_per_watt = 2.60
post_itc_per_watt = 3.32
final_price_per_watt = 3.50

total_cost = round(system_size_kw * 1000 * final_price_per_watt, 2)

# --- Display Results ---
if address and roof_sqft > 0:
    st.subheader("🔧 System Estimate:")
    st.write(f"Estimated system size: **{system_size_kw} kW**")
    st.write(f"Estimated total cost (before incentives): **${total_cost:,.2f}**")

    # --- Financing Estimate ---
    st.subheader("💰 Financing Options")
    monthly_payment = round(total_cost * 0.015, 2)  # ~1.5% of total cost
    st.write(f"Estimated monthly payment: **${monthly_payment}/month** (20-year term)")

    st.markdown("---")
    st.markdown("### 👷 Installed by:")
    st.markdown("**Northern Pacific Electric**  
WA License: NORTHPE759BS  
Walter Struckman  
📞 206-712-4212  
📧 wstruckmannpe@gmail.com")
