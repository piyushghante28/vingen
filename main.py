import streamlit as st
import random
import string

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

# Function to generate a random VIN with proper validation
def generate_vin(manufacturer):
    if manufacturer not in WMI_CODES:
        return "Invalid Manufacturer"
    
    wmi = WMI_CODES[manufacturer]  # First 3 characters (WMI)
    vds = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))  # 4-9 characters (VDS)
    year_code = random.choice("ABCDEFGHJKLMNPRSTVWXY123456789")  # 10th character (Year Code, skipping I, O, Q)
    plant_code = random.choice(string.ascii_uppercase)  # 11th character (Assembly Plant)
    serial = ''.join(random.choices(string.digits, k=6))  # 12-17 characters (Serial Number)
    
    vin = f"{wmi}{vds}{year_code}{plant_code}{serial}"
    return vin

# Streamlit UI
st.title("Random VIN Generator By Piyush")
st.write("Select a manufacturer to generate a random VIN.")

manufacturer = st.selectbox("Select Manufacturer", list(WMI_CODES.keys()))

if st.button("Generate VIN"):
    random_vin = generate_vin(manufacturer)
    st.success(f"Generated VIN: {random_vin}")
