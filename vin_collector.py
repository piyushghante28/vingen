# vin_collector.py
import aiohttp
import asyncio
import os
from datetime import datetime

REAL_VIN_API = "https://randomvin.com/getvin.php?type=real"

# WMI Codes → Make mapping
WMI_CODES = {
    "Toyota": "JTD", "Ford": "1FT", "Honda": "1HG", "BMW": "WBA", "Mercedes": "WDB",
    "Chevrolet": "1GC", "Tesla": "5YJ", "Audi": "WAU", "Nissan": "1N4", "Hyundai": "KMH",
    "Kia": "KNA", "Jeep": "1J4", "Dodge": "1B3", "Volkswagen": "3VW", "Subaru": "JF1",
    "Mazda": "JM1", "Lexus": "JTH", "Volvo": "YV1", "Porsche": "WP0", "Jaguar": "SAJ",
    "Land Rover": "SAL", "Mitsubishi": "JA3", "Infiniti": "JNK", "Acura": "19U", "Ferrari": "ZFF",
    "Lamborghini": "ZHW", "Bugatti": "VF9", "Rolls-Royce": "SCA", "Bentley": "SCB"
}

def get_make(vin):
    for make, wmi in WMI_CODES.items():
        if vin.startswith(wmi):
            return make
    return None

def save_vin(vin, make):
    os.makedirs("vin_data", exist_ok=True)
    make_file = os.path.join("vin_data", f"make_{make}.txt")
    name_file = os.path.join("vin_data", "make_name.txt")

    # Save VIN
    with open(make_file, "a") as f:
        f.write(vin + "\n")

    # Save make name if new
    if os.path.exists(name_file):
        with open(name_file, "r") as f:
            makes = set(line.strip() for line in f)
    else:
        makes = set()

    if make not in makes:
        with open(name_file, "a") as f:
            f.write(make + "\n")

async def fetch_vins_forever():
    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with session.get(REAL_VIN_API) as response:
                    vin = (await response.text()).strip()
                    make = get_make(vin)
                    if make:
                        save_vin(vin, make)
                        print(f"[{datetime.now()}] ✅ {vin} → {make}")
                    else:
                        print(f"[{datetime.now()}] ❌ Unknown WMI: {vin}")
            except Exception as e:
                print(f"[{datetime.now()}] ❌ Error: {e}")
            await asyncio.sleep(1)  # Delay between requests

if __name__ == "__main__":
    asyncio.run(fetch_vins_forever())
