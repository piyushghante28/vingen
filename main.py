import streamlit as st
import aiohttp
import asyncio

# Apply Dark Theme with Monospace Font
st.set_page_config(page_title="VIN Generator", layout="centered")

# Define Manufacturer WMI codes
WMI_CODES = {
    "Toyota": "JTD", "Ford": "1FT", "Honda": "1HG", "BMW": "WBA", "Mercedes": "WDB",
    "Chevrolet": "1GC", "Tesla": "5YJ", "Audi": "WAU", "Nissan": "1N4", "Hyundai": "KMH",
    "Kia": "KNA", "Jeep": "1J4", "Dodge": "1B3", "Volkswagen": "3VW", "Subaru": "JF1",
    "Mazda": "JM1", "Lexus": "JTH", "Volvo": "YV1", "Porsche": "WP0", "Jaguar": "SAJ",
    "Land Rover": "SAL", "Mitsubishi": "JA3", "Infiniti": "JNK", "Acura": "19U", "Ferrari": "ZFF",
    "Lamborghini": "ZHW", "Bugatti": "VF9", "Rolls-Royce": "SCA", "Bentley": "SCB"
}

# Function to fetch a real VIN asynchronously
API_URL = "https://randomvin.com/getvin.php?type=real"

async def fetch_vin(session):
    """Fetch a single VIN from the API."""
    async with session.get(API_URL) as response:
        return await response.text()

async def fetch_valid_vin(manufacturer_wmi):
    """Fetch multiple VINs concurrently and return the first valid one."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_vin(session) for _ in range(50)]  # Fire 50 requests
        for future in asyncio.as_completed(tasks):  # Process as they arrive
            response = await future
            if response.startswith(manufacturer_wmi):  # Validate VIN
                return response.strip()

# Apply Custom CSS for Large VIN Display
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

# Streamlit UI
st.title("🚗 Fast Random VIN Generator")

# Dropdown Menu for Car Manufacturers
st.markdown('<div class="dropdown-container">', unsafe_allow_html=True)
selected_manufacturer = st.selectbox("Select Manufacturer", list(WMI_CODES.keys()))
st.markdown('</div>', unsafe_allow_html=True)

# Generate VIN Button
if st.button("Generate VIN"):
    manufacturer_wmi = WMI_CODES[selected_manufacturer]
    
    async def generate_vin():
        valid_vin = await fetch_valid_vin(manufacturer_wmi)
        st.markdown(f'<div class="big-vin">{valid_vin}</div>', unsafe_allow_html=True)

    asyncio.create_task(generate_vin())  # Run async function in Streamlit

# import streamlit as st
# import aiohttp
# import asyncio

# # Apply Dark Theme with Monospace Font
# st.set_page_config(page_title="VIN Generator", layout="centered")

# # Define Manufacturer WMI codes
# WMI_CODES = {
#     "Toyota": "JTD", "Ford": "1FT", "Honda": "1HG", "BMW": "WBA", "Mercedes": "WDB",
#     "Chevrolet": "1GC", "Tesla": "5YJ", "Audi": "WAU", "Nissan": "1N4", "Hyundai": "KMH",
#     "Kia": "KNA", "Jeep": "1J4", "Dodge": "1B3", "Volkswagen": "3VW", "Subaru": "JF1",
#     "Mazda": "JM1", "Lexus": "JTH", "Volvo": "YV1", "Porsche": "WP0", "Jaguar": "SAJ",
#     "Land Rover": "SAL", "Mitsubishi": "JA3", "Infiniti": "JNK", "Acura": "19U", "Ferrari": "ZFF",
#     "Lamborghini": "ZHW", "Bugatti": "VF9", "Rolls-Royce": "SCA", "Bentley": "SCB"
# }

# # Function to fetch a real VIN asynchronously
# API_URL = "https://randomvin.com/getvin.php?type=real"

# async def fetch_vin(session):
#     async with session.get(API_URL) as response:
#         return await response.text()

# async def fetch_valid_vin(manufacturer_wmi):
#     async with aiohttp.ClientSession() as session:
#         while True:
#             response = await fetch_vin(session)
#             if response.startswith(manufacturer_wmi):
#                 return response.strip()

# # Apply Custom CSS for Large VIN Display
# st.markdown("""
#     <style>
#     body {
#         background-color: #121212;
#         font-family: monospace;
#     }
#     .big-vin {
#         font-size: 50px;
#         font-weight: bold;
#         color: #00ffcc;
#         text-align: center;
#         padding: 20px;
#         background: rgba(0, 0, 0, 0.8);
#         border-radius: 15px;
#         margin-top: 20px;
#         box-shadow: 0px 4px 10px rgba(0,255,204,0.3);
#         font-family: monospace;
#     }
#     .dropdown-container {
#         text-align: center;
#     }
#     .stSelectbox {
#         font-family: monospace;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # Streamlit UI
# st.title("🚗 Random VIN Generator")

# # Dropdown Menu for Car Manufacturers
# st.markdown('<div class="dropdown-container">', unsafe_allow_html=True)
# selected_manufacturer = st.selectbox("Select Manufacturer", list(WMI_CODES.keys()))
# st.markdown('</div>', unsafe_allow_html=True)

# # Generate VIN Button
# if st.button("Generate VIN"):
#     manufacturer_wmi = WMI_CODES[selected_manufacturer]
#     valid_vin = asyncio.run(fetch_valid_vin(manufacturer_wmi))
    
#     # Display VIN in Large Styled Box
#     st.markdown(f'<div class="big-vin">{valid_vin}</div>', unsafe_allow_html=True)
