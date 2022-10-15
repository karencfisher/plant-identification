# plant-identification

Project to develop Android application to identify wild plants in this area (Moab).

1) Data collection: get plant images

2) Data preprocessing and scaling of images

3) Transfer learning using Mobilenet 

4) Conversion of model to TF Lite

5) Integerate into present Android image classification as MVP

6) Add retrieval and display of information about identified specimen

### Data collection

#### Issues:

Getting sufficient numbers of accurate images

Using NPS checklist for vascular plants in Arches National Park, trying to obtain images via Google image search API.
Main obstacle is limits on the API, including dialy limit on requests. Each batch of 10 images may contain 0 - 10 specific
images (title contains full query string): but we are limited to only search 20 batches (200 images) to try to satisfy
our desired number of images.

Has to filter out unrelated images from search results. Presently matching image title with complete query string. 

