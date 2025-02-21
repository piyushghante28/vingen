

import streamlit as st
import aiohttp
import asyncio
import time

# Extended WMI (World Manufacturer Identifier) for different brands
WMI_CODES = {
    "Toyota": "JTD", "Ford": "1FT", "Honda": "1HG", "BMW": "WBA", "Mercedes": "WDB",
    "Chevrolet": "1GC", "Tesla": "5YJ", "Audi": "WAU", "Nissan": "1N4", "Hyundai": "KMH",
    "Kia": "KNA", "Jeep": "1J4", "Dodge": "1B3", "Volkswagen": "3VW", "Subaru": "JF1",
    "Mazda": "JM1", "Lexus": "JTH", "Volvo": "YV1", "Porsche": "WP0", "Jaguar": "SAJ",
    "Land Rover": "SAL", "Mitsubishi": "JA3", "Infiniti": "JNK", "Acura": "19U", "Ferrari": "ZFF",
    "Lamborghini": "ZHW", "Bugatti": "VF9", "Rolls-Royce": "SCA", "Bentley": "SCB"
}

# Function to fetch a real VIN from the API asynchronously
API_URL = "https://randomvin.com/getvin.php?type=real"

async def fetch_vin(session):
    async with session.get(API_URL) as response:
        return await response.text()

async def fetch_valid_vin(manufacturer_wmi, log):
    attempts = 0
    async with aiohttp.ClientSession() as session:
        while True:
            tasks = [fetch_vin(session) for _ in range(50)]  # Make 5 requests in parallel
            responses = await asyncio.gather(*tasks)
            attempts += len(responses)
            
            for vin in responses:
                vin = vin.strip()
                log.append(f"Attempt {attempts}: {vin}")
                if vin.startswith(manufacturer_wmi):
                    return vin
            
            await asyncio.sleep(0.2)  # Reduce wait time

# Streamlit UI
st.title("Random VIN Generator")
st.sidebar.title("VIN Generation Log")

# Log area
log = st.sidebar.empty()
log_data = []

# Display buttons in a single row
grid_columns = st.columns(len(WMI_CODES)*2)

for index, (manufacturer, wmi) in enumerate(WMI_CODES.items()):
    with grid_columns[index]:
        if st.button(manufacturer):
            valid_vin = asyncio.run(fetch_valid_vin(wmi, log_data))
            st.markdown(
                f"""
                <div style='text-align: center; padding: 10px; background: linear-gradient(to bottom, #5A7CA6, #2E4C6D); color: white; font-size: 24px; font-weight: bold; border-radius: 8px;'>
                    {valid_vin}
                </div>
                """,
                unsafe_allow_html=True
            )

# Update log in the sidebar
log.write("\n".join(log_data[-10:]))  # Show last 10 attempts


# # # import streamlit as st
# # # import aiohttp
# # # import asyncio
# # # import time

# # # # Extended WMI (World Manufacturer Identifier) for different brands
# # # WMI_CODES = {
# # #     "Toyota": "JTD", "Ford": "1FT", "Honda": "1HG", "BMW": "WBA", "Mercedes": "WDB",
# # #     "Chevrolet": "1GC", "Tesla": "5YJ", "Audi": "WAU", "Nissan": "1N4", "Hyundai": "KMH",
# # #     "Kia": "KNA", "Jeep": "1J4", "Dodge": "1B3", "Volkswagen": "3VW", "Subaru": "JF1",
# # #     "Mazda": "JM1", "Lexus": "JTH", "Volvo": "YV1", "Porsche": "WP0", "Jaguar": "SAJ",
# # #     "Land Rover": "SAL", "Mitsubishi": "JA3", "Infiniti": "JNK", "Acura": "19U", "Ferrari": "ZFF",
# # #     "Lamborghini": "ZHW", "Bugatti": "VF9", "Rolls-Royce": "SCA", "Bentley": "SCB"
# # # }

# # # # Function to fetch a real VIN from the API asynchronously
# # # API_URL = "https://randomvin.com/getvin.php?type=real"

# # # async def fetch_vin(session):
# # #     async with session.get(API_URL) as response:
# # #         return await response.text()

# # # async def fetch_valid_vin(manufacturer_wmi, log):
# # #     attempts = 0
# # #     async with aiohttp.ClientSession() as session:
# # #         while True:
# # #             tasks = [fetch_vin(session) for _ in range(5)]  # Make 5 requests in parallel
# # #             responses = await asyncio.gather(*tasks)
# # #             attempts += len(responses)
            
# # #             for vin in responses:
# # #                 vin = vin.strip()
# # #                 log.append(f"Attempt {attempts}: {vin}")
# # #                 if vin.startswith(manufacturer_wmi):
# # #                     return vin
            
# # #             await asyncio.sleep(0.2)  # Reduce wait time

# # # # Streamlit UI
# # # st.title("Random VIN Generator")
# # # st.sidebar.title("VIN Generation Log")

# # # # Log area
# # # log = st.sidebar.empty()
# # # log_data = []

# # # # Display buttons in a grid layout
# # # cols = st.columns(5)  # 5 buttons per row
# # # index = 0

# # # for manufacturer, wmi in WMI_CODES.items():
# # #     with cols[index % 5]:
# # #         if st.button(manufacturer):
# # #             valid_vin = asyncio.run(fetch_valid_vin(wmi, log_data))
# # #             st.success(f"Generated VIN for {manufacturer}: {valid_vin}")
# # #     index += 1

# # # # Update log in the sidebar
# # # log.write("\n".join(log_data[-10:]))  # Show last 10 attempts

# # # # import streamlit as st
# # # # import aiohttp
# # # # import asyncio
# # # # import time

# # # # # Extended WMI (World Manufacturer Identifier) for different brands
# # # # WMI_CODES = {
# # # #     "Toyota": "JTD",
# # # #     "Ford": "1FT",
# # # #     "Honda": "1HG",
# # # #     "BMW": "WBA",
# # # #     "Mercedes": "WDB",
# # # #     "Chevrolet": "1GC",
# # # #     "Tesla": "5YJ",
# # # #     "Audi": "WAU",
# # # #     "Nissan": "1N4",
# # # #     "Hyundai": "KMH",
# # # #     "Kia": "KNA",
# # # #     "Jeep": "1J4",
# # # #     "Dodge": "1B3",
# # # #     "Volkswagen": "3VW",
# # # #     "Subaru": "JF1",
# # # #     "Mazda": "JM1",
# # # #     "Lexus": "JTH",
# # # #     "Volvo": "YV1",
# # # #     "Porsche": "WP0",
# # # #     "Jaguar": "SAJ",
# # # #     "Land Rover": "SAL",
# # # #     "Mitsubishi": "JA3",
# # # #     "Infiniti": "JNK",
# # # #     "Acura": "19U",
# # # #     "Ferrari": "ZFF",
# # # #     "Lamborghini": "ZHW",
# # # #     "Bugatti": "VF9",
# # # #     "Rolls-Royce": "SCA",
# # # #     "Bentley": "SCB"
# # # # }

# # # # # Function to fetch a real VIN from the API asynchronously
# # # # API_URL = "https://randomvin.com/getvin.php?type=real"

# # # # async def fetch_vin(session):
# # # #     async with session.get(API_URL) as response:
# # # #         return await response.text()

# # # # async def fetch_valid_vin(manufacturer_wmi, log):
# # # #     attempts = 0
# # # #     async with aiohttp.ClientSession() as session:
# # # #         while True:
# # # #             tasks = [fetch_vin(session) for _ in range(5)]  # Make 5 requests in parallel
# # # #             responses = await asyncio.gather(*tasks)
# # # #             attempts += len(responses)
            
# # # #             for vin in responses:
# # # #                 vin = vin.strip()
# # # #                 log.append(f"Attempt {attempts}: {vin}")
# # # #                 if vin.startswith(manufacturer_wmi):
# # # #                     return vin
            
# # # #             await asyncio.sleep(0.2)  # Reduce wait time

# # # # # Streamlit UI
# # # # st.title("Random VIN Generator")
# # # # st.sidebar.title("VIN Generation Log")

# # # # # Log area
# # # # log = st.sidebar.empty()
# # # # log_data = []

# # # # # Create buttons for each manufacturer
# # # # for manufacturer, wmi in WMI_CODES.items():
# # # #     if st.button(f"Generate {manufacturer} VIN"):
# # # #         valid_vin = asyncio.run(fetch_valid_vin(wmi, log_data))
# # # #         st.success(f"Generated VIN for {manufacturer}: {valid_vin}")
    
# # # #     # Update log in the sidebar
# # # #     log.write("\n".join(log_data[-10:]))  # Show last 10 attempts


# # # # # import streamlit as st
# # # # # import random
# # # # # import string
# # # # # import requests
# # # # # import time

# # # # # # Extended WMI (World Manufacturer Identifier) for different brands
# # # # # WMI_CODES = {
# # # # #     "Toyota": "JTD",
# # # # #     "Ford": "1FT",
# # # # #     "Honda": "1HG",
# # # # #     "BMW": "WBA",
# # # # #     "Mercedes": "WDB",
# # # # #     "Chevrolet": "1GC",
# # # # #     "Tesla": "5YJ",
# # # # #     "Audi": "WAU",
# # # # #     "Nissan": "1N4",
# # # # #     "Hyundai": "KMH",
# # # # #     "Kia": "KNA",
# # # # #     "Jeep": "1J4",
# # # # #     "Dodge": "1B3",
# # # # #     "Volkswagen": "3VW",
# # # # #     "Subaru": "JF1",
# # # # #     "Mazda": "JM1",
# # # # #     "Lexus": "JTH",
# # # # #     "Volvo": "YV1",
# # # # #     "Porsche": "WP0",
# # # # #     "Jaguar": "SAJ",
# # # # #     "Land Rover": "SAL",
# # # # #     "Mitsubishi": "JA3",
# # # # #     "Infiniti": "JNK",
# # # # #     "Acura": "19U",
# # # # #     "Ferrari": "ZFF",
# # # # #     "Lamborghini": "ZHW",
# # # # #     "Bugatti": "VF9",
# # # # #     "Rolls-Royce": "SCA",
# # # # #     "Bentley": "SCB"
# # # # # }

# # # # # # Function to fetch a real VIN from the API
# # # # # API_URL = "https://randomvin.com/getvin.php?type=real"
# # # # # def fetch_valid_vin(manufacturer_wmi):
# # # # #     while True:
# # # # #         response = requests.get(API_URL)
# # # # #         if response.status_code == 200:
# # # # #             vin = response.text.strip()
# # # # #             if vin.startswith(manufacturer_wmi):
# # # # #                 return vin
# # # # #         time.sleep(1)  # Avoid excessive API calls

# # # # # # Streamlit UI
# # # # # st.title("Random VIN Generator")
# # # # # st.write("Select a manufacturer to generate a valid random VIN.")

# # # # # manufacturer = st.selectbox("Select Manufacturer", list(WMI_CODES.keys()))

# # # # # if st.button("Generate VIN"):
# # # # #     valid_vin = fetch_valid_vin(WMI_CODES[manufacturer])
# # # # #     st.success(f"Generated VIN: {valid_vin}")
