import os
from google_images_search import GoogleImagesSearch
from dotenv import dotenv_values


API_PROJECT = os.getenv('GCS_CX')
API_KEY = os.getenv('GCS_DEVELOPER_KEY')

gis = GoogleImagesSearch(API_KEY, API_PROJECT)
params = {'q': 'mormon tea plant', 'num': 3}

data_path = os.path.join(os.getcwd(), 'data')
gis.search(search_params=params, path_to_dir=data_path, width=224, height=224)

print(os.listdir(data_path))
