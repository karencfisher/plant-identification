import os
import requests
import logging
import re

from shutil import copyfileobj
from urllib.parse import quote_plus
from dotenv import dotenv_values


GCS_CX = os.getenv('GCS_CX')
API_KEY = os.getenv('GCS_DEVELOPER_KEY')

URL = f'https://customsearch.googleapis.com/customsearch/v1'
PARAMS = {'cx': GCS_CX,
          'key': API_KEY,
          'q': '',
          'num': 10,
          'start': 1,
          'searchType': 'image',
          'fileType': 'jpg',
          'safe': 'off',
          'imgColorType': 'color',
          'alt': 'json'}

log_path = os.path.join(os.getcwd(), 'search.log')
logging.basicConfig(filename=log_path, filemode='w', level=logging.INFO)

def search_image(item_str, count, data_path):
    start = 1
    image_count = 0
    PARAMS['q'] = '"' + quote_plus(item_str) + '"'

    while count > 0:
        if start >= 200:
            logging.info('Exceeded limit of start parameter')
            break

        # Maximum number of images in one query is 10
        num = 10
        logging.info(f'Searching {num} images fpr {item_str}')

        # Assemble parameters
        PARAMS['num'] = num
        PARAMS['start'] = start

        # Make request
        result = requests.get(URL, PARAMS)
        result_json = result.json()

        # Handle HTTP errors, record and return
        if result.status_code != 200:
            error = result_json['error']
            logging.error(f'Code: {error["code"]}')
            logging.error(f'Message: { error["message"]}')
            break

        # Attempt to download found images
        for item in result_json['items']:
            if item_str not in item['title']:
                continue
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
    user_agent = {'User-agent': 'Mozilla/5.0'}
    result = requests.get(image_url, headers=user_agent, stream=True)

    # Handle HTTP errors, returns False
    if result.status_code != 200:
        logging.error(f'failed getting image {image_string}')
        logging.error(f'HTTP Error: {result.status_code}')
        return False

    # Store the image in data_path
    image_string = re.sub(r'[^\w\s-]', '', image_string)
    image_file_name = image_string.strip().replace(' ', '-') + '.jpg'
    file_path = os.path.join(data_path, image_file_name)
    with open(file_path, 'wb') as FP:
        copyfileobj(result.raw, FP)
    logging.info(f'saved {image_string}')

    # Success
    return True
    


if __name__ == '__main__':

    search_image('mormon tea', 10, 'data')
