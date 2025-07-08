import aiohttp
import asyncio
import os
from datetime import datetime, timedelta

# API Endpoint
REAL_VIN_API = "https://randomvin.com/getvin.php?type=real"

# Known WMI Codes for manufacturers
WMI_CODES = {
    "Toyota": "JTD", "Ford": "1FT", "Honda": "1HG", "BMW": "WBA", "Mercedes": "WDB",
    "Chevrolet": "1GC", "Tesla": "5YJ", "Audi": "WAU", "Nissan": "1N4", "Hyundai": "KMH",
    "Kia": "KNA", "Jeep": "1J4", "Dodge": "1B3", "Volkswagen": "3VW", "Subaru": "JF1",
    "Mazda": "JM1", "Lexus": "JTH", "Volvo": "YV1", "Porsche": "WP0", "Jaguar": "SAJ",
    "Land Rover": "SAL", "Mitsubishi": "JA3", "Infiniti": "JNK", "Acura": "19U", "Ferrari": "ZFF",
    "Lamborghini": "ZHW", "Bugatti": "VF9", "Rolls-Royce": "SCA", "Bentley": "SCB"
}

# Load existing manufacturers from file
def load_existing_makes(file_path="make_name.txt"):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return set(line.strip() for line in f.readlines())
    return set()

# Append manufacturer name to file
def append_make(make_name, file_path="make_name.txt"):
    with open(file_path, "a") as f:
        f.write(f"{make_name}\n")

# Append VIN to specific make file
def append_vin(vin, make_name):
    filename = f"make_{make_name}.txt"
    with open(filename, "a") as f:
        f.write(f"{vin}\n")

# Determine manufacturer based on VIN prefix
def get_manufacturer_from_vin(vin):
    for make, wmi in WMI_CODES.items():
        if vin.startswith(wmi):
            return make
    return None

# Function to collect VINs for 5 minutes
async def collect_vins_for_5_minutes():
    saved_makes = load_existing_makes()
    async with aiohttp.ClientSession() as session:
        end_time = datetime.now() + timedelta(minutes=5)
        while datetime.now() < end_time:
            try:
                async with session.get(REAL_VIN_API) as response:
                    vin = (await response.text()).strip()
                    make = get_manufacturer_from_vin(vin)
                    if make:
                        append_vin(vin, make)
                        if make not in saved_makes:
                            append_make(make)
                            saved_makes.add(make)
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Saved: {vin} → {make}")
                    else:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Ignored unknown WMI: {vin}")
            except Exception as e:
                print(f"[ERROR] {e}")
            await asyncio.sleep(0.3)  # Slight delay between calls

# Run this loop every 10 minutes, collecting for 5
async def run_every_10_minutes():
    while True:
        print(f"\n=== 🚀 Starting VIN Collection @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
        await collect_vins_for_5_minutes()
        print(f"=== 💤 Sleeping for 5 minutes ===\n")
        await asyncio.sleep(5 * 60)

# Entry point
if __name__ == "__main__":
    asyncio.run(run_every_10_minutes())
