import streamlit as st
import aiohttp
import asyncio

# Set up dark theme with monospace font
st.set_page_config(page_title="VIN Generator", layout="centered")

# Manufacturer WMI codes
WMI_CODES = {
    "Toyota": "JTD", "Ford": "1FT", "Honda": "1HG", "BMW": "WBA", "Mercedes": "WDB",
    "Chevrolet": "1GC", "Tesla": "5YJ", "Audi": "WAU", "Nissan": "1N4", "Hyundai": "KMH",
    "Kia": "KNA", "Jeep": "1J4", "Dodge": "1B3", "Volkswagen": "3VW", "Subaru": "JF1",
    "Mazda": "JM1", "Lexus": "JTH", "Volvo": "YV1", "Porsche": "WP0", "Jaguar": "SAJ",
    "Land Rover": "SAL", "Mitsubishi": "JA3", "Infiniti": "JNK", "Acura": "19U", "Ferrari": "ZFF",
    "Lamborghini": "ZHW", "Bugatti": "VF9", "Rolls-Royce": "SCA", "Bentley": "SCB"
}

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
    .dropdown-container {
        text-align: center;
    }
    .stSelectbox {
        font-family: monospace;
    }
    </style>
""", unsafe_allow_html=True)

# Async function to make parallel API calls
async def fetch_vins(session, manufacturer_wmi, num_requests=10):
    tasks = [session.get(API_URL) for _ in range(num_requests)]
    responses = await asyncio.gather(*tasks)  # Run requests in parallel
    vins = [await r.text() for r in responses]
    return next((vin.strip() for vin in vins if vin.startswith(manufacturer_wmi)), None)

# Function to fetch VIN with async execution
async def get_vin(manufacturer_wmi):
    async with aiohttp.ClientSession() as session:
        vin = await fetch_vins(session, manufacturer_wmi)
        return vin if vin else "VIN Not Found"

# Streamlit UI
st.title("🚗 Super-Fast VIN Generator")

# Dropdown Menu for Car Manufacturers
st.markdown('<div class="dropdown-container">', unsafe_allow_html=True)
selected_manufacturer = st.selectbox("Select Manufacturer", list(WMI_CODES.keys()))
st.markdown('</div>', unsafe_allow_html=True)

# Generate VIN Button
if st.button("Generate VIN"):
    manufacturer_wmi = WMI_CODES[selected_manufacturer]
    valid_vin = asyncio.run(get_vin(manufacturer_wmi))

    # Display VIN in Large Styled Box
    st.markdown(f'<div class="big-vin">{valid_vin}</div>', unsafe_allow_html=True)
