import os
import time
import requests
from datetime import datetime

# Directory to save images
output_dir = "./all_images"
os.makedirs(output_dir, exist_ok=True)

# CollapseCam cameras
cams = {
    "4x2": "https://webcams.nyctmc.org/api/cameras/8f692f55-8118-423b-8bcb-1ea49eaf442b/image",
    "42x3": "https://webcams.nyctmc.org/api/cameras/5352e130-4668-4be5-a7b9-9e1ce4ea6d4c/image",
}

# Run for 60 seconds, grab every 2 seconds (30 iterations)
# Cron fires this every minute for continuous coverage
duration_sec = 60
interval_sec = 2
iterations = duration_sec // interval_sec

for i in range(iterations):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    for cam_name, cam_url in cams.items():
        try:
            resp = requests.get(cam_url, timeout=10)
            if resp.status_code == 200:
                filename = f"{cam_name}_{timestamp}.jpg"
                filepath = os.path.join(output_dir, filename)
                with open(filepath, "wb") as f:
                    f.write(resp.content)
            else:
                print(f"Failed to get image from {cam_name}, status: {resp.status_code}")
        except Exception as e:
            print(f"Error fetching {cam_name}: {e}")
    if i < iterations - 1:
        time.sleep(interval_sec)
