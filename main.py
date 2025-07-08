# app.py
import streamlit as st
import random
import asyncio
import aiohttp
import os

st.set_page_config(
    page_title="VIN Generator",
    layout="centered",
    page_icon="https://cdn-icons-png.flaticon.com/512/846/846338.png"
)

WMI_CODES = {
    "Toyota": "JTD", "Ford": "1FT", "Honda": "1HG", "BMW": "WBA", "Mercedes": "WDB",
    "Chevrolet": "1GC", "Tesla": "5YJ", "Audi": "WAU", "Nissan": "1N4", "Hyundai": "KMH",
    "Kia": "KNA", "Jeep": "1J4", "Dodge": "1B3", "Volkswagen": "3VW", "Subaru": "JF1",
    "Mazda": "JM1", "Lexus": "JTH", "Volvo": "YV1", "Porsche": "WP0", "Jaguar": "SAJ",
    "Land Rover": "SAL", "Mitsubishi": "JA3", "Infiniti": "JNK", "Acura": "19U", "Ferrari": "ZFF",
    "Lamborghini": "ZHW", "Bugatti": "VF9", "Rolls-Royce": "SCA", "Bentley": "SCB"
}

REAL_VIN_API = "https://randomvin.com/getvin.php?type=real"
FAKE_VIN_API = "https://randomvin.com/getvin.php?type=fake"

async def fetch_vin(api_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            return await response.text()

async def fetch_valid_vin(manufacturer_wmi):
    async with aiohttp.ClientSession() as session:
        while True:
            response = await fetch_vin(REAL_VIN_API)
            if response.startswith(manufacturer_wmi):
                return response.strip()

st.markdown("""
    <style>
    body {
        background-color: #121212;
        font-family: monospace;
    }
    .big-vin {
        font-size: 50px;
        font-weight: bold;
        color: #0a0a0a;
        text-align: center;
        padding: 20px;
        background: #b8c6df;
        border-radius: 15px;
        margin-top: 20px;
        margin-bottom: 20px;
        box-shadow: #84a5e0;
    }
    .dropdown-container {
        text-align: center;
    }
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        padding: 10px;
        color: #00ffcc;
        font-family: monospace;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚗 Random VIN Generator")

make_file = "vin_data/make_name.txt"
if os.path.exists(make_file):
    with open(make_file) as f:
        available_makes = sorted(set(line.strip() for line in f))
else:
    available_makes = sorted(WMI_CODES.keys())

selected_manufacturer = st.selectbox("Select Manufacturer", available_makes)

if st.button("Generate VIN by Manufacturer"):
    file_path = f"vin_data/make_{selected_manufacturer}.txt"
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            vins = [line.strip() for line in f if line.strip()]
        if vins:
            st.markdown(f'<div class="big-vin">{random.choice(vins)}</div>', unsafe_allow_html=True)
        else:
            st.warning("No VINs available yet for this make.")
    else:
        manufacturer_wmi = WMI_CODES.get(selected_manufacturer)
        if manufacturer_wmi:
            valid_vin = asyncio.run(fetch_valid_vin(manufacturer_wmi))
            st.markdown(f'<div class="big-vin">{valid_vin}</div>', unsafe_allow_html=True)
        else:
            st.error("Invalid WMI code. Cannot fetch VIN.")

if st.button("Real VIN Generator (Random)"):
    real_vin = asyncio.run(fetch_vin(REAL_VIN_API))
    st.markdown(f'<div class="big-vin">{real_vin.strip()}</div>', unsafe_allow_html=True)

if st.button("Dummy VIN Generator (Random)"):
    dummy_vin = asyncio.run(fetch_vin(FAKE_VIN_API))
    st.markdown(f'<div class="big-vin">{dummy_vin.strip()}</div>', unsafe_allow_html=True)

st.markdown('<div class="footer">Made By Piyush Ghante</div>', unsafe_allow_html=True)

# # app.py
# import streamlit as st
# import random
# import asyncio
# import aiohttp
# import os

# st.set_page_config(
#     page_title="VIN Generator",
#     layout="centered",
#     page_icon="https://cdn-icons-png.flaticon.com/512/846/846338.png"
# )

# WMI_CODES = {
#     "Toyota": "JTD", "Ford": "1FT", "Honda": "1HG", "BMW": "WBA", "Mercedes": "WDB",
#     "Chevrolet": "1GC", "Tesla": "5YJ", "Audi": "WAU", "Nissan": "1N4", "Hyundai": "KMH",
#     "Kia": "KNA", "Jeep": "1J4", "Dodge": "1B3", "Volkswagen": "3VW", "Subaru": "JF1",
#     "Mazda": "JM1", "Lexus": "JTH", "Volvo": "YV1", "Porsche": "WP0", "Jaguar": "SAJ",
#     "Land Rover": "SAL", "Mitsubishi": "JA3", "Infiniti": "JNK", "Acura": "19U", "Ferrari": "ZFF",
#     "Lamborghini": "ZHW", "Bugatti": "VF9", "Rolls-Royce": "SCA", "Bentley": "SCB"
# }

# REAL_VIN_API = "https://randomvin.com/getvin.php?type=real"
# FAKE_VIN_API = "https://randomvin.com/getvin.php?type=fake"

# async def fetch_vin(api_url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(api_url) as response:
#             return await response.text()

# async def fetch_valid_vin(manufacturer_wmi):
#     async with aiohttp.ClientSession() as session:
#         while True:
#             response = await fetch_vin(REAL_VIN_API)
#             if response.startswith(manufacturer_wmi):
#                 return response.strip()

# st.markdown("""
#     <style>
#     body {
#         background-color: #121212;
#         font-family: monospace;
#     }
#     .big-vin {
#         font-size: 50px;
#         font-weight: bold;
#         color: #0a0a0a;
#         text-align: center;
#         padding: 20px;
#         background: #b8c6df;
#         border-radius: 15px;
#         margin-top: 20px;
#         margin-bottom: 20px;
#         box-shadow: #84a5e0;
#     }
#     .dropdown-container {
#         text-align: center;
#     }
#     .footer {
#         position: fixed;
#         bottom: 0;
#         width: 100%;
#         padding: 10px;
#         color: #00ffcc;
#         font-family: monospace;
#     }
#     </style>
# """, unsafe_allow_html=True)

# st.title("🚗 Random VIN Generator")

# # Load makes from file or fallback to dict
# make_file = "vin_data/make_name.txt"
# if os.path.exists(make_file):
#     with open(make_file) as f:
#         available_makes = sorted(set(line.strip() for line in f))
# else:
#     available_makes = sorted(WMI_CODES.keys())

# selected_manufacturer = st.selectbox("Select Manufacturer", available_makes)

# if st.button("Generate VIN by Manufacturer"):
#     # Use existing txt file if available
#     file_path = f"vin_data/make_{selected_manufacturer}.txt"
#     if os.path.exists(file_path):
#         with open(file_path, "r") as f:
#             vins = [line.strip() for line in f if line.strip()]
#         if vins:
#             st.markdown(f'<div class="big-vin">{random.choice(vins)}</div>', unsafe_allow_html=True)
#         else:
#             st.warning("No VINs available yet for this make.")
#     else:
#         # Fallback to live fetch if file missing
#         manufacturer_wmi = WMI_CODES.get(selected_manufacturer)
#         if manufacturer_wmi:
#             valid_vin = asyncio.run(fetch_valid_vin(manufacturer_wmi))
#             st.markdown(f'<div class="big-vin">{valid_vin}</div>', unsafe_allow_html=True)
#         else:
#             st.error("Invalid WMI code. Cannot fetch VIN.")

# if st.button("Real VIN Generator (Random)"):
#     real_vin = asyncio.run(fetch_vin(REAL_VIN_API))
#     st.markdown(f'<div class="big-vin">{real_vin.strip()}</div>', unsafe_allow_html=True)

# if st.button("Dummy VIN Generator (Random)"):
#     dummy_vin = asyncio.run(fetch_vin(FAKE_VIN_API))
#     st.markdown(f'<div class="big-vin">{dummy_vin.strip()}</div>', unsafe_allow_html=True)

# st.markdown('<div class="footer">Made By Piyush Ghante</div>', unsafe_allow_html=True)


# # import streamlit as st
# # import aiohttp
# # import asyncio

# # # Apply Dark Theme with Monospace Font
# # st.set_page_config(page_title="VIN Generator", layout="centered",page_icon="https://cdn-icons-png.flaticon.com/512/846/846338.png")


# # # Define Manufacturer WMI codes
# # WMI_CODES = {
# #     "Toyota": "JTD", "Ford": "1FT", "Honda": "1HG", "BMW": "WBA", "Mercedes": "WDB",
# #     "Chevrolet": "1GC", "Tesla": "5YJ", "Audi": "WAU", "Nissan": "1N4", "Hyundai": "KMH",
# #     "Kia": "KNA", "Jeep": "1J4", "Dodge": "1B3", "Volkswagen": "3VW", "Subaru": "JF1",
# #     "Mazda": "JM1", "Lexus": "JTH", "Volvo": "YV1", "Porsche": "WP0", "Jaguar": "SAJ",
# #     "Land Rover": "SAL", "Mitsubishi": "JA3", "Infiniti": "JNK", "Acura": "19U", "Ferrari": "ZFF",
# #     "Lamborghini": "ZHW", "Bugatti": "VF9", "Rolls-Royce": "SCA", "Bentley": "SCB"
# # }

# # # API Endpoints
# # REAL_VIN_API = "https://randomvin.com/getvin.php?type=real"
# # FAKE_VIN_API = "https://randomvin.com/getvin.php?type=fake"

# # # Async Function to Fetch VIN
# # async def fetch_vin(api_url):
# #     async with aiohttp.ClientSession() as session:
# #         async with session.get(api_url) as response:
# #             return await response.text()

# # async def fetch_valid_vin(manufacturer_wmi):
# #     async with aiohttp.ClientSession() as session:
# #         while True:
# #             response = await fetch_vin(REAL_VIN_API)
# #             if response.startswith(manufacturer_wmi):
# #                 return response.strip()

# # # Apply Custom CSS for Large VIN Display
# # st.markdown("""
# #     <style>
# #     body {
# #         background-color: #121212;
# #         font-family: monospace;
# #     }
# #     .big-vin {
# #         font-size: 50px;
# #         font-weight: bold;
# #         color: #0a0a0a;
# #         text-align: center;
# #         padding: 20px;
# #         background: #b8c6df;
# #         border-radius: 15px;
# #         margin-top: 20px;
# #         margin-bottom: 20px;
# #         box-shadow: #84a5e0;
# #         font-family: monospace;
# #         text-align: center;
    
# #     }
# #     .dropdown-container {
# #         text-align: center;
# #     }
# #     .stSelectbox {
# #         font-family: monospace;
# #     }
# #      .footer {
# #         position: fixed;
# #         bottom: 0;
# #         width: 100%;
# #         padding: 10px;
        
# #         color: #00ffcc;
# #         font-family: monospace;
# #     }
# #     </style>
   
# # """, unsafe_allow_html=True)

# # # Streamlit UI
# # st.title("🚗 Random VIN Generator")

# # # Dropdown Menu for Car Manufacturers
# # st.markdown('<div class="dropdown-container">', unsafe_allow_html=True)
# # selected_manufacturer = st.selectbox("Select Manufacturer", list(WMI_CODES.keys()))
# # #st.markdown('</div>', unsafe_allow_html=True)

# # # Generate VIN by Manufacturer Button
# # if st.button("Generate VIN by Manufacturer"):
# #     manufacturer_wmi = WMI_CODES[selected_manufacturer]
# #     valid_vin = asyncio.run(fetch_valid_vin(manufacturer_wmi))
# #     st.markdown(f'<div class="big-vin">{valid_vin}</div>', unsafe_allow_html=True)

# # # Real VIN Generator Button
# # if st.button("Real VIN Generator (Random)"):
# #     real_vin = asyncio.run(fetch_vin(REAL_VIN_API))
# #     st.markdown(f'<div class="big-vin">{real_vin.strip()}</div>', unsafe_allow_html=True)

# # # Dummy VIN Generator Button
# # if st.button("Dummy VIN Generator (Random)"):
# #     dummy_vin = asyncio.run(fetch_vin(FAKE_VIN_API))
# #     st.markdown(f'<div class="big-vin">{dummy_vin.strip()}</div>', unsafe_allow_html=True)
# # # Footer
# # st.markdown('<div class="footer">Made By Piyush Ghante</div>', unsafe_allow_html=True)

# # # import streamlit as st
# # # import aiohttp
# # # import asyncio

# # # # Apply Dark Theme with Monospace Font
# # # st.set_page_config(page_title="VIN Generator", layout="centered")

# # # # Define Manufacturer WMI codes
# # # WMI_CODES = {
# # #     "Toyota": "JTD", "Ford": "1FT", "Honda": "1HG", "BMW": "WBA", "Mercedes": "WDB",
# # #     "Chevrolet": "1GC", "Tesla": "5YJ", "Audi": "WAU", "Nissan": "1N4", "Hyundai": "KMH",
# # #     "Kia": "KNA", "Jeep": "1J4", "Dodge": "1B3", "Volkswagen": "3VW", "Subaru": "JF1",
# # #     "Mazda": "JM1", "Lexus": "JTH", "Volvo": "YV1", "Porsche": "WP0", "Jaguar": "SAJ",
# # #     "Land Rover": "SAL", "Mitsubishi": "JA3", "Infiniti": "JNK", "Acura": "19U", "Ferrari": "ZFF",
# # #     "Lamborghini": "ZHW", "Bugatti": "VF9", "Rolls-Royce": "SCA", "Bentley": "SCB"
# # # }

# # # # API Endpoints
# # # REAL_VIN_API = "https://randomvin.com/getvin.php?type=real"
# # # FAKE_VIN_API = "https://randomvin.com/getvin.php?type=fake"

# # # # Async Function to Fetch VIN
# # # async def fetch_vin(api_url):
# # #     async with aiohttp.ClientSession() as session:
# # #         async with session.get(api_url) as response:
# # #             return await response.text()

# # # async def fetch_valid_vin(manufacturer_wmi):
# # #     async with aiohttp.ClientSession() as session:
# # #         while True:
# # #             response = await fetch_vin(REAL_VIN_API)
# # #             if response.startswith(manufacturer_wmi):
# # #                 return response.strip()

# # # # Apply Custom CSS for Large VIN Display
# # # st.markdown("""
# # #     <style>
# # #     body {
# # #         background-color: #121212;
# # #         font-family: monospace;
# # #     }
# # #     .big-vin {
# # #         font-size: 50px;
# # #         font-weight: bold;
# # #         color: #00ffcc;
# # #         text-align: center;
# # #         padding: 20px;
       
# # #         border-radius: 15px;
# # #         margin-top: 20px;
       
# # #         font-family: monospace;
# # #     }
# # #     .dropdown-container {
# # #         text-align: center;
# # #     }
# # #     .stSelectbox {
# # #         font-family: monospace;
# # #     }
# # #     </style>
# # # """, unsafe_allow_html=True)

# # # # Streamlit UI
# # # st.title("🚗 Random VIN Generator")

# # # # Dropdown Menu for Car Manufacturers
# # # st.markdown('<div class="dropdown-container">', unsafe_allow_html=True)
# # # selected_manufacturer = st.selectbox("Select Manufacturer", list(WMI_CODES.keys()))
# # # st.markdown('</div>', unsafe_allow_html=True)

# # # # Generate VIN Buttons
# # # col1, col2, col3 = st.columns(3)

# # # with col1:
# # #     if st.button("Generate VIN"):
# # #         manufacturer_wmi = WMI_CODES[selected_manufacturer]
# # #         valid_vin = asyncio.run(fetch_valid_vin(manufacturer_wmi))
# # #         st.markdown(f'<div class="big-vin">{valid_vin}</div>', unsafe_allow_html=True)

# # # with col2:
# # #     if st.button("Random Real VIN Generator "):
# # #         real_vin = asyncio.run(fetch_vin(REAL_VIN_API))
# # #         st.markdown(f'<div class="big-vin">{real_vin.strip()}</div>', unsafe_allow_html=True)

# # # with col3:
# # #     if st.button("Random Dummy VIN Generator"):
# # #         dummy_vin = asyncio.run(fetch_vin(FAKE_VIN_API))
# # #         st.markdown(f'<div class="big-vin">{dummy_vin.strip()}</div>', unsafe_allow_html=True)


# # # # import streamlit as st
# # # # import aiohttp
# # # # import asyncio

# # # # # Apply Dark Theme with Monospace Font
# # # # st.set_page_config(page_title="VIN Generator", layout="centered")

# # # # # Define Manufacturer WMI codes
# # # # WMI_CODES = {
# # # #     "Toyota": "JTD", "Ford": "1FT", "Honda": "1HG", "BMW": "WBA", "Mercedes": "WDB",
# # # #     "Chevrolet": "1GC", "Tesla": "5YJ", "Audi": "WAU", "Nissan": "1N4", "Hyundai": "KMH",
# # # #     "Kia": "KNA", "Jeep": "1J4", "Dodge": "1B3", "Volkswagen": "3VW", "Subaru": "JF1",
# # # #     "Mazda": "JM1", "Lexus": "JTH", "Volvo": "YV1", "Porsche": "WP0", "Jaguar": "SAJ",
# # # #     "Land Rover": "SAL", "Mitsubishi": "JA3", "Infiniti": "JNK", "Acura": "19U", "Ferrari": "ZFF",
# # # #     "Lamborghini": "ZHW", "Bugatti": "VF9", "Rolls-Royce": "SCA", "Bentley": "SCB"
# # # # }

# # # # # API Endpoints
# # # # REAL_VIN_API = "https://randomvin.com/getvin.php?type=real"
# # # # FAKE_VIN_API = "https://randomvin.com/getvin.php?type=fake"

# # # # # Async Function to Fetch VIN
# # # # test
# # # # async def fetch_vin(api_url):
# # # #     async with aiohttp.ClientSession() as session:
# # # #         async with session.get(api_url) as response:
# # # #             return await response.text()

# # # # async def fetch_valid_vin(manufacturer_wmi):
# # # #     async with aiohttp.ClientSession() as session:
# # # #         while True:
# # # #             response = await fetch_vin(REAL_VIN_API)
# # # #             if response.startswith(manufacturer_wmi):
# # # #                 return response.strip()

# # # # # Apply Custom CSS for Large VIN Display
# # # # st.markdown("""
# # # #     <style>
# # # #     body {
# # # #         background-color: #121212;
# # # #         font-family: monospace;
# # # #     }
# # # #     .big-vin {
# # # #         font-size: 50px;
# # # #         font-weight: bold;
# # # #         color: #00ffcc;
# # # #         text-align: center;
# # # #         padding: 20px;
# # # #         background: rgba(0, 0, 0, 0.8);
# # # #         border-radius: 15px;
# # # #         margin-top: 20px;
# # # #         box-shadow: 0px 4px 10px rgba(0,255,204,0.3);
# # # #         font-family: monospace;
# # # #     }
# # # #     .dropdown-container {
# # # #         text-align: center;
# # # #     }
# # # #     .stSelectbox {
# # # #         font-family: monospace;
# # # #     }
# # # #     </style>
# # # # """, unsafe_allow_html=True)

# # # # # Streamlit UI
# # # # st.title("🚗 Random VIN Generator")

# # # # # Dropdown Menu for Car Manufacturers
# # # # st.markdown('<div class="dropdown-container">', unsafe_allow_html=True)
# # # # selected_manufacturer = st.selectbox("Select Manufacturer", list(WMI_CODES.keys()))
# # # # st.markdown('</div>', unsafe_allow_html=True)

# # # # # Generate VIN Buttons
# # # # col1, col2, col3 = st.columns(3)

# # # # with col1:
# # # #     if st.button("Generate VIN"):
# # # #         manufacturer_wmi = WMI_CODES[selected_manufacturer]
# # # #         valid_vin = asyncio.run(fetch_valid_vin(manufacturer_wmi))
# # # #         st.markdown(f'<div class="big-vin">{valid_vin}</div>', unsafe_allow_html=True)

# # # # with col2:
# # # #     if st.button("Real VIN Generator"):
# # # #         real_vin = asyncio.run(fetch_vin(REAL_VIN_API))
# # # #         st.markdown(f'<div class="big-vin">{real_vin.strip()}</div>', unsafe_allow_html=True)

# # # # with col3:
# # # #     if st.button("Dummy VIN Generator"):
# # # #         dummy_vin = asyncio.run(fetch_vin(FAKE_VIN_API))
# # # #         st.markdown(f'<div class="big-vin">{dummy_vin.strip()}</div>', unsafe_allow_html=True)

# # # # # import streamlit as st
# # # # # import aiohttp
# # # # # import asyncio

# # # # # # Apply Dark Theme with Monospace Font
# # # # # st.set_page_config(page_title="VIN Generator", layout="centered")

# # # # # # Define Manufacturer WMI codes
# # # # # WMI_CODES = {
# # # # #     "Toyota": "JTD", "Ford": "1FT", "Honda": "1HG", "BMW": "WBA", "Mercedes": "WDB",
# # # # #     "Chevrolet": "1GC", "Tesla": "5YJ", "Audi": "WAU", "Nissan": "1N4", "Hyundai": "KMH",
# # # # #     "Kia": "KNA", "Jeep": "1J4", "Dodge": "1B3", "Volkswagen": "3VW", "Subaru": "JF1",
# # # # #     "Mazda": "JM1", "Lexus": "JTH", "Volvo": "YV1", "Porsche": "WP0", "Jaguar": "SAJ",
# # # # #     "Land Rover": "SAL", "Mitsubishi": "JA3", "Infiniti": "JNK", "Acura": "19U", "Ferrari": "ZFF",
# # # # #     "Lamborghini": "ZHW", "Bugatti": "VF9", "Rolls-Royce": "SCA", "Bentley": "SCB"
# # # # # }

# # # # # # Function to fetch a real VIN asynchronously
# # # # # API_URL = "https://randomvin.com/getvin.php?type=real"

# # # # # async def fetch_vin(session):
# # # # #     async with session.get(API_URL) as response:
# # # # #         return await response.text()

# # # # # async def fetch_valid_vin(manufacturer_wmi):
# # # # #     async with aiohttp.ClientSession() as session:
# # # # #         while True:
# # # # #             response = await fetch_vin(session)
# # # # #             if response.startswith(manufacturer_wmi):
# # # # #                 return response.strip()

# # # # # # Apply Custom CSS for Large VIN Display
# # # # # st.markdown("""
# # # # #     <style>
# # # # #     body {
# # # # #         background-color: #121212;
# # # # #         font-family: monospace;
# # # # #     }
# # # # #     .big-vin {
# # # # #         font-size: 50px;
# # # # #         font-weight: bold;
# # # # #         color: #00ffcc;
# # # # #         text-align: center;
# # # # #         padding: 20px;
# # # # #         background: rgba(0, 0, 0, 0.8);
# # # # #         border-radius: 15px;
# # # # #         margin-top: 20px;
# # # # #         box-shadow: 0px 4px 10px rgba(0,255,204,0.3);
# # # # #         font-family: monospace;
# # # # #     }
# # # # #     .dropdown-container {
# # # # #         text-align: center;
# # # # #     }
# # # # #     .stSelectbox {
# # # # #         font-family: monospace;
# # # # #     }
# # # # #     </style>
# # # # # """, unsafe_allow_html=True)

# # # # # # Streamlit UI
# # # # # st.title("🚗 Random VIN Generator")

# # # # # # Dropdown Menu for Car Manufacturers
# # # # # st.markdown('<div class="dropdown-container">', unsafe_allow_html=True)
# # # # # selected_manufacturer = st.selectbox("Select Manufacturer", list(WMI_CODES.keys()))
# # # # # st.markdown('</div>', unsafe_allow_html=True)

# # # # # # Generate VIN Button
# # # # # if st.button("Generate VIN"):
# # # # #     manufacturer_wmi = WMI_CODES[selected_manufacturer]
# # # # #     valid_vin = asyncio.run(fetch_valid_vin(manufacturer_wmi))
    
# # # # #     # Display VIN in Large Styled Box
# # # # #     st.markdown(f'<div class="big-vin">{valid_vin}</div>', unsafe_allow_html=True)
