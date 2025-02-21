import streamlit as st
import random
import string
import requests
import time

# Extended WMI (World Manufacturer Identifier) for different brands
WMI_CODES = {
    "Toyota": "JTD",
    "Ford": "1FT",
    "Honda": "1HG",
    "BMW": "WBA",
    "Mercedes": "WDB",
    "Chevrolet": "1GC",
    "Tesla": "5YJ",
    "Audi": "WAU",
    "Nissan": "1N4",
    "Hyundai": "KMH",
    "Kia": "KNA",
    "Jeep": "1J4",
    "Dodge": "1B3",
    "Volkswagen": "3VW",
    "Subaru": "JF1",
    "Mazda": "JM1",
    "Lexus": "JTH",
    "Volvo": "YV1",
    "Porsche": "WP0",
    "Jaguar": "SAJ",
    "Land Rover": "SAL",
    "Mitsubishi": "JA3",
    "Infiniti": "JNK",
    "Acura": "19U",
    "Ferrari": "ZFF",
    "Lamborghini": "ZHW",
    "Bugatti": "VF9",
    "Rolls-Royce": "SCA",
    "Bentley": "SCB"
}

# Function to fetch a real VIN from the API
API_URL = "https://randomvin.com/getvin.php?type=real"
def fetch_valid_vin(manufacturer_wmi):
    while True:
        response = requests.get(API_URL)
        if response.status_code == 200:
            vin = response.text.strip()
            if vin.startswith(manufacturer_wmi):
                return vin
        time.sleep(1)  # Avoid excessive API calls

# Streamlit UI
st.title("Random VIN Generator")
st.write("Select a manufacturer to generate a valid random VIN.")

manufacturer = st.selectbox("Select Manufacturer", list(WMI_CODES.keys()))

if st.button("Generate VIN"):
    valid_vin = fetch_valid_vin(WMI_CODES[manufacturer])
    st.success(f"Generated VIN: {valid_vin}")
