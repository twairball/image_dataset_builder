from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import json
import time
import wget
import uuid
import csv 
import pathlib

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import argparse

parser = argparse.ArgumentParser(
    description='Download images using google image search')
parser.add_argument('query', 
    metavar='query', type=str, help='The query to download images from')
parser.add_argument('--count', 
    metavar='count', default=2000, type=int, 
    help='How many images to fetch')
parser.add_argument('--test',
    metavar='test', default=False, type=bool, 
    help="Test mode disables actual file downloads")
parser.add_argument('--out', 
    metavar='out', type=str, help="The output directory to store images", 
    required=True)

# TODO: webp
VALID_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}
    
def download_image(url, save_dir, img_type='jpg'):
    """Download image and save as random filename"""
    filename = get_image_filename(url, img_type=img_type)
    filepath = os.path.join(save_dir, filename)
    logger.info("Downloading image: %s => %s" % (url, filepath))
    wget.download(url, filepath)
    return filename

def get_image_filename(url, img_type='jpg'):    
    filename = "%s.%s" % (str(uuid.uuid4()), img_type)
    return filename

def google_image_search(
        query='street+fashion', 
        num_requested=2000, 
        save_dir='output',
        test_mode=False
        ):
    # setup selenium
    url = "https://www.google.com.hk/search?q="+query+"&source=lnms&tbm=isch"
    driver = webdriver.Chrome('drivers/chromedriver')
    driver.get(url)

    # track images
    img_count = 0
    downloaded_img_count = 0
    images_downloaded = dict()

    # 5 mouse scrolls to click "show more results" button
    number_of_scrolls = int(num_requested / 400) + 1 
    for _ in range(number_of_scrolls):
        for _ in range(10):
            driver.execute_script("window.scrollBy(0, 1000000)")
            time.sleep(0.2)
        time.sleep(0.5)
        try:
            driver.find_element_by_xpath("//input[@value='Show more results']").click()
        except Exception as e:
            print("Less images found:", e)
            continue

    images = driver.find_elements_by_xpath('//div[contains(@class,"rg_meta")]')
    total_images_scrolled = len(images)

    for img in images:
        img_count += 1
        img_url = json.loads(img.get_attribute('innerHTML'))["ou"]
        img_type = json.loads(img.get_attribute('innerHTML'))["ity"]
        if img_type not in VALID_EXTENSIONS:
            img_type = "jpg"

        try:
            if test:
                filename = get_image_filename(img_url, img_type)
            else:
                filename = download_image(img_url, save_dir, img_type)
            
            images_downloaded[img_url] = filename
            downloaded_img_count += 1

        except Exception as e:
            logging.info("Download failed: %s" % e)
        finally:
            print
        if downloaded_img_count >= num_requested:
            break

    logging.info("Total downloaded: %d / %d" % (downloaded_img_count, img_count))
    logging.info("Total scrolled: %d" % total_images_scrolled)

    driver.quit()

    return images_downloaded

if __name__ == "__main__":
    args = parser.parse_args()
    query = args.query
    output_dir = args.out
    count = args.count
    test = args.test

    # mkdir -p
    path = pathlib.Path(output_dir)
    path.parent.mkdir(parents=True, exist_ok=True)

    # crawl
    results = google_image_search(query, count, output_dir, test)

    # write results
    filepath = os.path.join(output_dir, "output.csv")
    w = csv.writer(open(filepath, "w"))
    for key, val in results.items():
        w.writerow([key, val])
    
