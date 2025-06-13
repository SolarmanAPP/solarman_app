import streamlit as st
import os

st.set_page_config(page_title="SolarMan App", layout="wide")

tab1, tab2, tab3 = st.tabs(["🏠 Home", "📊 Estimate", "💰 Financing Options"])

with tab1:
    st.title("🔆 SolarMan")
    st.subheader("Home")
    st.write("Welcome to the SolarMan App! Use the tabs above to navigate.")

with tab2:
    st.header("📊 Estimate")
    st.info("This section will include your solar system size, sun hours, and bill offset details. (From Solar API version)")

with tab3:
    st.header("💰 Financing Options")
    st.markdown("""
### 📌 Loan Examples

| Loan Provider | Term | Rate | Est. Monthly for $25,000 |
|---------------|------|------|---------------------------|
| GoodLeap | 25 yr | 4.99% | ~$145/mo |
| Sunlight Financial | 20 yr | 5.49% | ~$165/mo |
| [🌟 **PSCCU Solar Financing Options (Preferred)**](https://www.psccu.org/loans/solar-loans.html) | 15 yr | 4.24% | ~$187/mo |

---

📎 Click one of the partners to apply, or reach out to your certified installer for help.

📩 Once you’re approved, this section will connect to real-time financing tools and monthly breakdowns.
    """)
