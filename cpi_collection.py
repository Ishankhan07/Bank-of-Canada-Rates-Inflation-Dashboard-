import requests
import os

os.makedirs("data", exist_ok=True)

product_id = "18100004"

api_url = (
    f"https://www150.statcan.gc.ca/t1/wds/rest/"
    f"getFullTableDownloadCSV/{product_id}/en"
)

print("Requesting CPI download link...")

response = requests.get(api_url, timeout=60)

print("API Status Code:", response.status_code)

response.raise_for_status()

result = response.json()

download_url = result["object"]

print("Downloading actual CPI ZIP file...")

zip_response = requests.get(download_url, timeout=120)

print("Download Status Code:", zip_response.status_code)

zip_response.raise_for_status()

file_path = "data/cpi_raw.zip"

with open(file_path, "wb") as file:
    file.write(zip_response.content)

print("CPI ZIP downloaded successfully!")
print("File size:", os.path.getsize(file_path), "bytes")