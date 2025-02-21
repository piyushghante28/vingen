import streamlit as st
import aiohttp
import asyncio

# Set up dark theme with monospace font
st.set_page_config(page_title="VIN Generator", layout="centered")

# API Endpoint
API_URL = "https://randomvin.com/getvin.php?type=real"

# Apply custom CSS for large VIN display
st.markdown("""
    <style>
    body {
        background-color: #121212;
        font-family: monospace;
    }
    .big-vin {
        font-size: 50px;
        font-weight: bold;
        color: #00ffcc;
        text-align: center;
        padding: 20px;
        background: rgba(0, 0, 0, 0.8);
        border-radius: 15px;
        margin-top: 20px;
        box-shadow: 0px 4px 10px rgba(0,255,204,0.3);
        font-family: monospace;
    }
    </style>
""", unsafe_allow_html=True)

# Async generator to fetch VINs and return the first valid one
async def fetch_first_valid_vin():
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(API_URL) for _ in range(50)]  # Fire 50 requests
        for future in asyncio.as_completed(tasks):  # Process as soon as one returns
            response = await future
            vin = await response.text()
            if vin:  # If valid VIN found, return it
                return vin
    return "VIN Not Found"

# Streamlit UI
st.title("🚗 Ultra-Fast VIN Generator")

# Generate VIN Button
if st.button("Generate VIN"):
    vin = asyncio.run(fetch_first_valid_vin())  # Get VIN as soon as first response arrives

    # Display VIN in Large Styled Box
    st.markdown(f'<div class="big-vin">{vin}</div>', unsafe_allow_html=True)
