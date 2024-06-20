import requests
import os
from urllib.parse import urlparse
import time
import random

def fetch_data(url):
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # print(len(data["list"]))
        return data["list"]
    else:
        print("Request failed with status code:", response.status_code)
        raise Exception("Request failed with status code:", response.status_code)

def download_image(url):
    if not os.path.exists("./images"):
        os.makedirs("./images", exist_ok=True)

    image_base_name = urlparse(url).path.split("/")[-1]
    image_name = image_base_name.replace("{res}", "")

    # current_time = str(int(time.time() * 1000))

    response = requests.get(url)
    if response.status_code == 200:
        with open(f"./images/{image_name}", 'wb') as file:
            file.write(response.content)

        print(f"Image successfully downloaded")
        return True
    else:
        return False

def next_image(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    path_parts = path.split("/")
    image_base_name = path_parts[-1]
    image_name_split = image_base_name.split("_")
    image_name_split[1] = str(int(image_name_split[1]) + 1)
    new_image_name = "_".join(image_name_split)
    path_parts[-1] = new_image_name
    new_path = "/".join(path_parts)

    new_url = parsed_url._replace(path=new_path).geturl()
    return new_url



# url = "https://api.bunjang.co.kr/api/1/find_v2.json?f_category_id=910100001&page=0&order=date&req_ref=category&stat_device=w&n=100&version=4"
url = "https://api.bunjang.co.kr/api/1/find_v2.json?f_category_id=910200001&page=0&order=date&req_ref=category&stat_device=w&n=100&version=4"

try:
    data = fetch_data(url)
    for idx, item in enumerate(data):
        if item["ad"] == True:
            continue
        base_image_url = item["product_image"]
        print(f'{idx}: {item["product_image"]}')
        while True:
            if not download_image(base_image_url):
                break
            base_image_url = next_image(base_image_url)

            random_number = random.randint(40, 150)
            time.sleep(random_number / 1000)
except:
    print("Error fetching data")
    exit()

