import streamlit as st
import pandas as pd

st.set_page_config(
    page_title = "Soccer Dashboard",
    layout = "wide"
)

st.title("Soccer Analytics Dashboard")

st.write("This is a test Streamlit app.")

data = pd.DataFrame(
    {
        "Team": ["Arsenal", "Barcelona", "PSG"],
        "Goals": [72, 81, 67]
    }
)

st.dataframe(data)

st.bar_chart(data.set_index("Team"))