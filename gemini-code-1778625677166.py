import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# App Configuration
st.set_page_config(page_title="Melinda's Pizza Scoring", page_icon="🍕")

# Cloud Connection (Connects to your Google Sheet)
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("🍕 Melinda's Pizza Scoring")
st.markdown("---")

with st.form("rating_form", clear_on_submit=True):
    # Header Info
    pizzeria = st.text_input("Pizzeria Name")
    style = st.selectbox("Pizza Style", ["New York", "Neapolitan", "Detroit", "Sicilian", "Tavern", "Coal Fired"])
    toppings = st.multiselect("Toppings Observed", 
                             ["Plain Cheese", "Pepperoni", "Sausage", "Mushrooms", "Onions", "Fresh Basil", "Hot Honey", "Cup & Char"])

    st.subheader("1. The Crust")
    col1, col2 = st.columns(2)
    with col1:
        crust_crisp = st.select_slider("Crispness", options=["Soggy", "Doughy", "Standard", "Crispy", "Crunchy"])
        crust_char = st.slider("Underbelly Char", 1, 10, 5)
    with col2:
        crust_flavor = st.slider("Crust Flavor", 1, 10, 7)
        thickness = st.select_slider("Thickness", options=["Paper Thin", "Thin", "Medium", "Thick", "Deep"])

    st.subheader("2. The Sauce & Cheese")
    col3, col4 = st.columns(2)
    with col3:
        sauce_flavor = st.slider("Sauce (Sweet/Acidity)", 1, 10, 5)
        sauce_consist = st.select_slider("Sauce Consistency", options=["Watery", "Balanced", "Thick/Paste"])
    with col4:
        cheese_quality = st.slider("Cheese Quality/Melt", 1, 10, 7)
        cheese_oil = st.select_slider("Oiliness", options=["Dry", "Glistening", "Oily/Pools"])

    st.subheader("3. Technicals")
    col5, col6 = st.columns(2)
    with col5:
        flop = st.select_slider("Structural Integrity (Flop)", options=["No Flop", "Minimal", "Significant", "Total Collapse"])
    with col6:
        ratio = st.slider("Crust/Sauce/Cheese Balance", 1, 10, 5)

    st.subheader("The Verdict")
    final_score = st.slider("✨ FINAL SCORE", 0.0, 10.0, 7.0, step=0.1)
    notes = st.text_area("Final Thoughts on Freshness & Quality")

    submitted = st.form_submit_button("Lock in Score 🚀")

    if submitted:
        new_entry = {
            "Pizzeria": pizzeria, "Style": style, "Toppings": ", ".join(toppings),
            "Crust": f"{crust_crisp}/{crust_char}", "Sauce": sauce_flavor,
            "Cheese": cheese_quality, "Flop": flop, "Ratio": ratio,
            "Total": final_score, "Notes": notes
        }
        
        # Cloud Update
        existing_data = conn.read()
        updated_df = pd.concat([existing_data, pd.DataFrame([new_entry])], ignore_index=True)
        conn.update(data=updated_df)
        st.success(f"Score of {final_score} saved to Melinda's Archive!")