# shiertier_scrapy

English | [中文](https://github.com/shiertier-utils/shiertier_scrapy/blob/main/README_zh.md)

## Introduction

`shiertier_scrapy` is a Python library designed to simplify the process of downloading images from the web. It provides a robust and flexible interface for handling various HTTP status codes, retries, and image validation. This library is particularly useful for web scraping tasks where image downloads are required.

## Installation

You can install `shiertier_scrapy` via `pip`:

```bash
pip install git+https://github.com/shiertier/shiertier_scrapy.git
```

Please note that this project is still under development.

## Environment Variables and Storage Location

### Environment Variables

- `SCRAPY_SAVE_DIR`: The directory where downloaded images will be saved. If not provided, the current working directory will be used.

### Setting the Storage Location

You can specify the storage location by setting the `SCRAPY_SAVE_DIR` environment variable:

```bash
export SCRAPY_SAVE_DIR=/path/to/save_directory
```

Alternatively, you can pass the `save_dir` parameter when initializing the `ScrapyClientBase` class:

```python
from shiertier_scrapy import ScrapyClientBase

# Initialize with a custom save directory
scrapy_client = ScrapyClientBase(save_dir='/path/to/save_directory')
```

## Usage

### Downloading a Single Image

You can download a single image using the `download_one` method. This method requires the URL of the image and the desired save name. It also supports retries and sleep time between retries.

```python
from shiertier_scrapy import easy_scrapy_client

# Download a single image
easy_scrapy_client.download_one(url='http://example.com/image.jpg', save_name='image.jpg')
```

### Downloading Multiple Images

You can download multiple images concurrently using the `download_images` method. This method requires a list of URLs and corresponding save names. It also supports retries and sleep time between retries.

```python
from shiertier_scrapy import easy_scrapy_client

# URLs and save names
urls = ['http://example.com/image1.jpg', 'http://example.com/image2.jpg']
save_names = ['image1.jpg', 'image2.jpg']

# Download multiple images
easy_scrapy_client.download_images(urls=urls, save_names=save_names)
```

## Dependencies

- `requests`
- `Pillow`
- `shiertier_logger`
- `tqdm`

## License

This project is released under the MIT License. See the [LICENSE](LICENSE) file for details.