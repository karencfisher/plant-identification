import os
import requests
import logging
import json

from shutil import copyfileobj
from urllib.parse import quote_plus
from dotenv import dotenv_values


GCS_CX = os.getenv('GCS_CX')
API_KEY = os.getenv('GCS_DEVELOPER_KEY')

URI = f'https://customsearch.googleapis.com/customsearch/v1?'
BOILER_PLATE = f'&cx={GCS_CX}&key={API_KEY}&searchType=image&'
BOILER_PLATE += 'searchType=image&fileType=jpg&safe=off&'
BOILER_PLATE += 'imgColorType=color&alt=json'

log_path = os.path.join(os.getcwd(), 'search.log')
logging.basicConfig(filename=log_path, filemode='w', level=logging.INFO)

def search_image(item_str, count, data_path):
    start = 1
    image_count = 0

    while count > 0:
        if start >= 200:
            logging.info('Exceeded limit of start parameter')
            break

        # Maximum number of images in one query is 10
        num = 10 if count >= 10 else count
        logging.info(f'Getting {num} of {count} images fpr {item_str}')

        # Assemble URL
        query = quote_plus(item_str)
        URL = URI + f'q={query}&num={num}&start={start}'
        URL += BOILER_PLATE

        # Make request
        result = requests.get(URL)
        result_json = result.json()

        # Handle HTTP errors, record and return
        if result.status_code != 200:
            error = result_json['error']
            error_message = f'Code: {error["code"]}\nMessage: { error["message"]}'
            logging.error(error_message)
            break

        # Attempt to download found images
        for item in result_json['items']:
            image_url = item['link']
            image_string = item['title']
            success = download_image(image_url, image_string, data_path)
            if success:
                count -= 1
                image_count += 1

        start += 10
    logging.info(f'Downloaded {image_count} images')
    return image_count

def download_image(image_url, image_string, data_path):
    # Get image
    result = requests.get(image_url, stream=True)

    # Handle HTTP errors, returns False
    if result.status_code != 200:
        logging.error(f'failed getting image {image_string}')
        return False

    # Store the image in data_path
    image_file_name = image_string.strip().replace(' ', '-') + '.jpg'
    file_path = os.path.join(data_path, image_file_name)
    with open(image_file_name, 'wb') as FP:
        copyfileobj(result.raw, FB)
    logging(f'saved {image_string}')

    # Success
    return True
    

