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

# VIN character values for checksum calculation
VIN_VALUES = {
    **{str(i): i for i in range(10)},
    "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8,
    "J": 1, "K": 2, "L": 3, "M": 4, "N": 5, "P": 7, "R": 9,
    "S": 2, "T": 3, "U": 4, "V": 5, "W": 6, "X": 7, "Y": 8, "Z": 9
}

# VIN character weights for checksum calculation
VIN_WEIGHTS = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]

# Function to calculate the VIN check digit
def calculate_check_digit(vin):
    total = sum(VIN_VALUES[vin[i]] * VIN_WEIGHTS[i] for i in range(17))
    remainder = total % 11
    return "X" if remainder == 10 else str(remainder)

# Function to generate a random VIN with valid check digit
def generate_vin(manufacturer):
    if manufacturer not in WMI_CODES:
        return "Invalid Manufacturer"
    
    wmi = WMI_CODES[manufacturer]  # First 3 characters (WMI)
    vds = ''.join(random.choices("ABCDEFGHJKLMNPRSTUVWXYZ0123456789", k=5))  # 4-8 characters (VDS, excluding check digit)
    year_code = random.choice("ABCDEFGHJKLMNPRSTVWXY123456789")  # 10th character (Year Code, skipping I, O, Q)
    plant_code = random.choice("ABCDEFGHJKLMNPRSTUVWXYZ")  # 11th character (Assembly Plant)
    serial = ''.join(random.choices(string.digits, k=6))  # 12-17 characters (Serial Number)
    
    vin_partial = f"{wmi}{vds}0{year_code}{plant_code}{serial}"
    check_digit = calculate_check_digit(vin_partial)
    vin = f"{wmi}{vds}{check_digit}{year_code}{plant_code}{serial}"
    
    return vin

# Streamlit UI
st.title("Random VIN Generator")
st.write("Select a manufacturer to generate a valid random VIN.")

manufacturer = st.selectbox("Select Manufacturer", list(WMI_CODES.keys()))

if st.button("Generate VIN"):
    random_vin = generate_vin(manufacturer)
    st.success(f"Generated VIN: {random_vin}")
