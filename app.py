import streamlit as st

# Page configuration
st.set_page_config(
    page_title="☕ Coffee Cupping App",
    page_icon="☕",
    layout="wide"
)

st.title("☕ Coffee Cupping App")
st.write("Testing basic deployment...")

# Simple form
with st.form("test_form"):
    coffee_name = st.text_input("Coffee Name")
    score = st.slider("Score", 0, 100, 80)
    submit = st.form_submit_button("Save")
    
    if submit:
        st.success(f"Coffee: {coffee_name}, Score: {score}")
        st.balloons()

st.info("Basic app is working! 🎉")