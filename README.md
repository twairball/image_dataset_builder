# Image Dataset Builder

Crawl web images and build dataset, for e.g. machine learning. 

````
# query and download images to output dir

$ python ./google_images.py "cats" \
    --out outputs/cats \
    --count 1000

$ python ./google_images.py "dogs" \
    --out outputs/dogs \
    --count 1000

# now we got cats and dogs
````

# Install

1. `pip install -r requirements.txt`
2. Download selenium chromedriver:
    
    https://sites.google.com/a/chromium.org/chromedriver/downloads
    
    Save to to `./drivers/chromedriver`

# Image sources

- [x] Google Images
- [ ] Bing Images
- [ ] Baidu Images

# LICENSE

MIT
