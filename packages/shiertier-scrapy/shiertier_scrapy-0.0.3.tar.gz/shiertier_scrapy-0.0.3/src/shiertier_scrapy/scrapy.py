import os
import re
import requests
from time import sleep
from PIL import Image
from shiertier_logger import easy_logger_i18n as logger_i18n

class ScrapyClientBase:
    def __init__(self, save_dir='.'):
        self.status_list_base = [400,401,403,404,429,500,503,504]
        self.headers = {}
        self.save_dir = save_dir

    def create_directory(self):
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
            logger_i18n.info("Save directory does not exist, creating: $$save_dir$$",{"$$save_dir$$":self.save_dir})
        else:
            logger_i18n.debug("Save directory already exists: $$save_dir$$",{"$$save_dir$$":self.save_dir})

    def sanitize_filename(self, filename):
        # delete illegal characters in filename
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
        return sanitized

    def download_one_base(self, url, save_name, replace=False):
        self.create_directory()
        save_path = os.path.join(self.save_dir, save_name)
        if os.path.exists(save_path):
            if self.validate_image(save_path) and not replace:
                logger_i18n.debug("Image validation successful: $$save_path$$",{"$$save_path$$":save_path})
                return True
            else:
                logger_i18n.debug("Image validation failed: $$save_path$$",{"$$save_path$$":save_path})
                os.remove(save_path)
        else:
            try:
                if self.headers == {}:
                    response = requests.get(url, stream=True)
                else:
                    logger_i18n.debug("Request headers: $$headers$$",{"$$headers$$":self.headers})
                    response = requests.get(url, stream=True)

                if response.status_code == 200:
                    with open(save_path, 'wb') as file:
                        for chunk in response.iter_content(1024):
                            file.write(chunk)
                    logger_i18n.debug("Image downloaded successfully: $$save_path$$",{"$$save_path$$":save_path})
                    return True
                elif response.status_code in self.status_list:
                    eval(f"self.status_{response.status_code}()")
                else:
                    logger_i18n.warning("Download failed. Status: $$status$$",{"$$status$$":response.status_code})
            except requests.exceptions.RequestException as e:
                logger_i18n.warning("Request exception: $$e$$",{"$$e$$":e})
            except ConnectionAbortedError as e:
                logger_i18n.warning("Connection aborted error: $$e$$",{"$$e$$":e})
            except Exception as e:
                logger_i18n.warning("Error: $$e$$",{"$$e$$":e})
            return False

    def status_400(self):
        logger_i18n.error("400: Bad request")

    def status_401(self):
        logger_i18n.error("401: Unauthorized")

    def status_403(self):
        logger_i18n.warning("403: Forbidden")

    def status_404(self):
        logger_i18n.warning("404: Not found")

    def status_429(self):
        logger_i18n.error("429: Too many requests")

    def status_500(self):
        logger_i18n.error("500: Internal server error")

    def status_503(self):
        logger_i18n.error("503: Service unavailable")

    def status_504(self):
        logger_i18n.error("504: Gateway timeout")

    @property
    def status_list(self, add=None):
        if type(add) == int:
            return [add] + self.status_list_base
        elif type(add) == list:
            return add + self.status_list_base
        else:
            return self.status_list_base

    def download_one(self, url, save_name, retries=3, sleep_time=2):
        if url and save_name:
            for attempt in range(retries):
                try:
                    if self.download_one_base(url, save_name):
                        return True
                except Exception as e:
                    logger_i18n.debug(f"第 {attempt + 1} 失败: {e}")
                    sleep(sleep_time)  # wait 2 seconds and retry
            logger_i18n.warning(f"下载失败{url}.")
            return False
        return False

    def validate_image(self, filepath):
        try:
            with Image.open(filepath) as img:
                img.verify()  # only check image, not read full content
            logger_i18n.debug("Image validation successful: $$filepath$$",{"$$filepath$$":filepath})
            return True
        except Exception as e:
            logger_i18n.error("Image damaged: $$e$$",{"$$e$$":e})
            return False
        
    def download_images(self, urls, save_names, retries=3, sleep_time=2):
        from concurrent.futures import ThreadPoolExecutor
        from tqdm.auto import tqdm
        # auto set thread number
        thread_num = min(len(urls), os.cpu_count())
        with ThreadPoolExecutor(max_workers=thread_num) as executor:
            list(tqdm(executor.map(self.download_one, urls, save_names, retries, sleep_time), total=len(urls)))

easy_scrapy_client = ScrapyClientBase()