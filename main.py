import streamlit as st
import aiohttp
import asyncio
import os
import pandas as pd
import plotly.express as px

# ========== WMI Definitions ==========
WMI_CODES = {
    "Toyota": "JTD", "Ford": "1FT", "Honda": "1HG", "BMW": "WBA", "Mercedes": "WDB",
    "Chevrolet": "1GC", "Tesla": "5YJ", "Audi": "WAU", "Nissan": "1N4", "Hyundai": "KMH",
    "Kia": "KNA", "Jeep": "1J4", "Dodge": "1B3", "Volkswagen": "3VW", "Subaru": "JF1",
    "Mazda": "JM1", "Lexus": "JTH", "Volvo": "YV1", "Porsche": "WP0", "Jaguar": "SAJ",
    "Land Rover": "SAL", "Mitsubishi": "JA3", "Infiniti": "JNK", "Acura": "19U", "Ferrari": "ZFF",
    "Lamborghini": "ZHW", "Bugatti": "VF9", "Rolls-Royce": "SCA", "Bentley": "SCB"
}

REAL_VIN_API = "https://randomvin.com/getvin.php?type=real"

# ========== Utility Functions ==========

def load_existing_makes(file_path="make_name.txt"):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return set(line.strip() for line in f.readlines())
    return set()

def append_make(make_name, file_path="make_name.txt"):
    with open(file_path, "a") as f:
        f.write(f"{make_name}\n")

def append_vin(vin, make_name):
    file_path = f"make_{make_name}.txt"
    with open(file_path, "a") as f:
        f.write(f"{vin}\n")

def get_manufacturer_from_vin(vin):
    for make, wmi in WMI_CODES.items():
        if vin.startswith(wmi):
            return make
    return None

def get_region(vin):
    prefix = vin[0].upper() if vin else "?"
    if prefix in "12345":
        return "North America"
    elif prefix in "JJKLMNOPQR":
        return "Asia"
    elif prefix in "STUVWXYZ":
        return "Europe"
    elif prefix in "ABCDEFGH":
        return "Africa"
    elif prefix == "L":
        return "China"
    elif prefix == "K":
        return "Korea"
    return "Unknown"

async def fetch_single_vin():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(REAL_VIN_API) as response:
                vin = (await response.text()).strip()
                return vin
        except Exception as e:
            st.error(f"Error fetching VIN: {e}")
            return None

def update_local_storage(vin):
    make = get_manufacturer_from_vin(vin)
    if not make:
        return None

    append_vin(vin, make)
    existing_makes = load_existing_makes()
    if make not in existing_makes:
        append_make(make)
    return make

# ========== Streamlit UI ==========

st.set_page_config(page_title="VIN Viewer", layout="wide", page_icon="🚗")
st.title("🔁 Real-time VIN Collector + Archive Viewer")

# Collect Real-Time VIN
if st.button("Generate & Store Real VIN"):
    vin = asyncio.run(fetch_single_vin())
    if vin:
        make = update_local_storage(vin)
        if make:
            st.success(f"✅ VIN Saved for {make}: {vin}")
        else:
            st.warning(f"❌ Unknown WMI: {vin}")
    else:
        st.error("Failed to fetch VIN")

# Load available makes
makes = sorted(load_existing_makes())

# Sidebar: Chart
st.sidebar.subheader("📊 VIN Count per Make")
vin_counts = {}
for make in makes:
    file_path = f"make_{make}.txt"
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            vin_counts[make] = sum(1 for line in f if line.strip())

if vin_counts:
    chart_df = pd.DataFrame(vin_counts.items(), columns=["Manufacturer", "Count"])
    fig = px.bar(chart_df, x="Manufacturer", y="Count", color="Count", title="VIN Count per Manufacturer")
    st.sidebar.plotly_chart(fig, use_container_width=True)

# Select Make
if makes:
    selected_make = st.selectbox("Select Manufacturer", makes)
    vin_file = f"make_{selected_make}.txt"

    if os.path.exists(vin_file):
        with open(vin_file, "r") as f:
            vins = [line.strip() for line in f if line.strip()]

        # Search VINs
        query = st.text_input("🔍 Search VINs", "").strip().upper()
        filtered_vins = [v for v in vins if query in v]

        st.info(f"{len(filtered_vins)} / {len(vins)} VINs matched")
        
        df = pd.DataFrame(filtered_vins, columns=["VIN"])
        df["Region"] = df["VIN"].apply(get_region)
        st.dataframe(df.tail(20), use_container_width=True)

        # Download
        st.download_button(
            label="📥 Download Filtered VINs",
            data="\n".join(filtered_vins),
            file_name=f"{selected_make}_filtered.txt",
            mime="text/plain"
        )
    else:
        st.warning("VIN file not found for selected manufacturer")
else:
    st.warning("No manufacturers found yet.")

# import streamlit as st
# import aiohttp
# import asyncio

# # Apply Dark Theme with Monospace Font
# st.set_page_config(page_title="VIN Generator", layout="centered",page_icon="https://cdn-icons-png.flaticon.com/512/846/846338.png")


# # Define Manufacturer WMI codes
# WMI_CODES = {
#     "Toyota": "JTD", "Ford": "1FT", "Honda": "1HG", "BMW": "WBA", "Mercedes": "WDB",
#     "Chevrolet": "1GC", "Tesla": "5YJ", "Audi": "WAU", "Nissan": "1N4", "Hyundai": "KMH",
#     "Kia": "KNA", "Jeep": "1J4", "Dodge": "1B3", "Volkswagen": "3VW", "Subaru": "JF1",
#     "Mazda": "JM1", "Lexus": "JTH", "Volvo": "YV1", "Porsche": "WP0", "Jaguar": "SAJ",
#     "Land Rover": "SAL", "Mitsubishi": "JA3", "Infiniti": "JNK", "Acura": "19U", "Ferrari": "ZFF",
#     "Lamborghini": "ZHW", "Bugatti": "VF9", "Rolls-Royce": "SCA", "Bentley": "SCB"
# }

# # API Endpoints
# REAL_VIN_API = "https://randomvin.com/getvin.php?type=real"
# FAKE_VIN_API = "https://randomvin.com/getvin.php?type=fake"

# # Async Function to Fetch VIN
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
#         color: #0a0a0a;
#         text-align: center;
#         padding: 20px;
#         background: #b8c6df;
#         border-radius: 15px;
#         margin-top: 20px;
#         margin-bottom: 20px;
#         box-shadow: #84a5e0;
#         font-family: monospace;
#         text-align: center;
    
#     }
#     .dropdown-container {
#         text-align: center;
#     }
#     .stSelectbox {
#         font-family: monospace;
#     }
#      .footer {
#         position: fixed;
#         bottom: 0;
#         width: 100%;
#         padding: 10px;
        
#         color: #00ffcc;
#         font-family: monospace;
#     }
#     </style>
   
# """, unsafe_allow_html=True)

# # Streamlit UI
# st.title("🚗 Random VIN Generator")

# # Dropdown Menu for Car Manufacturers
# st.markdown('<div class="dropdown-container">', unsafe_allow_html=True)
# selected_manufacturer = st.selectbox("Select Manufacturer", list(WMI_CODES.keys()))
# #st.markdown('</div>', unsafe_allow_html=True)

# # Generate VIN by Manufacturer Button
# if st.button("Generate VIN by Manufacturer"):
#     manufacturer_wmi = WMI_CODES[selected_manufacturer]
#     valid_vin = asyncio.run(fetch_valid_vin(manufacturer_wmi))
#     st.markdown(f'<div class="big-vin">{valid_vin}</div>', unsafe_allow_html=True)

# # Real VIN Generator Button
# if st.button("Real VIN Generator (Random)"):
#     real_vin = asyncio.run(fetch_vin(REAL_VIN_API))
#     st.markdown(f'<div class="big-vin">{real_vin.strip()}</div>', unsafe_allow_html=True)

# # Dummy VIN Generator Button
# if st.button("Dummy VIN Generator (Random)"):
#     dummy_vin = asyncio.run(fetch_vin(FAKE_VIN_API))
#     st.markdown(f'<div class="big-vin">{dummy_vin.strip()}</div>', unsafe_allow_html=True)
# # Footer
# st.markdown('<div class="footer">Made By Piyush Ghante</div>', unsafe_allow_html=True)

# # import streamlit as st
# # import aiohttp
# # import asyncio

# # # Apply Dark Theme with Monospace Font
# # st.set_page_config(page_title="VIN Generator", layout="centered")

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
# #         color: #00ffcc;
# #         text-align: center;
# #         padding: 20px;
       
# #         border-radius: 15px;
# #         margin-top: 20px;
       
# #         font-family: monospace;
# #     }
# #     .dropdown-container {
# #         text-align: center;
# #     }
# #     .stSelectbox {
# #         font-family: monospace;
# #     }
# #     </style>
# # """, unsafe_allow_html=True)

# # # Streamlit UI
# # st.title("🚗 Random VIN Generator")

# # # Dropdown Menu for Car Manufacturers
# # st.markdown('<div class="dropdown-container">', unsafe_allow_html=True)
# # selected_manufacturer = st.selectbox("Select Manufacturer", list(WMI_CODES.keys()))
# # st.markdown('</div>', unsafe_allow_html=True)

# # # Generate VIN Buttons
# # col1, col2, col3 = st.columns(3)

# # with col1:
# #     if st.button("Generate VIN"):
# #         manufacturer_wmi = WMI_CODES[selected_manufacturer]
# #         valid_vin = asyncio.run(fetch_valid_vin(manufacturer_wmi))
# #         st.markdown(f'<div class="big-vin">{valid_vin}</div>', unsafe_allow_html=True)

# # with col2:
# #     if st.button("Random Real VIN Generator "):
# #         real_vin = asyncio.run(fetch_vin(REAL_VIN_API))
# #         st.markdown(f'<div class="big-vin">{real_vin.strip()}</div>', unsafe_allow_html=True)

# # with col3:
# #     if st.button("Random Dummy VIN Generator"):
# #         dummy_vin = asyncio.run(fetch_vin(FAKE_VIN_API))
# #         st.markdown(f'<div class="big-vin">{dummy_vin.strip()}</div>', unsafe_allow_html=True)


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
# # # test
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
# # #         background: rgba(0, 0, 0, 0.8);
# # #         border-radius: 15px;
# # #         margin-top: 20px;
# # #         box-shadow: 0px 4px 10px rgba(0,255,204,0.3);
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
# # #     if st.button("Real VIN Generator"):
# # #         real_vin = asyncio.run(fetch_vin(REAL_VIN_API))
# # #         st.markdown(f'<div class="big-vin">{real_vin.strip()}</div>', unsafe_allow_html=True)

# # # with col3:
# # #     if st.button("Dummy VIN Generator"):
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

# # # # # Function to fetch a real VIN asynchronously
# # # # API_URL = "https://randomvin.com/getvin.php?type=real"

# # # # async def fetch_vin(session):
# # # #     async with session.get(API_URL) as response:
# # # #         return await response.text()

# # # # async def fetch_valid_vin(manufacturer_wmi):
# # # #     async with aiohttp.ClientSession() as session:
# # # #         while True:
# # # #             response = await fetch_vin(session)
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

# # # # # Generate VIN Button
# # # # if st.button("Generate VIN"):
# # # #     manufacturer_wmi = WMI_CODES[selected_manufacturer]
# # # #     valid_vin = asyncio.run(fetch_valid_vin(manufacturer_wmi))
    
# # # #     # Display VIN in Large Styled Box
# # # #     st.markdown(f'<div class="big-vin">{valid_vin}</div>', unsafe_allow_html=True)
