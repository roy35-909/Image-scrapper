from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os,sys
import io
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import re
from pathlib import Path
from new_croper import crop_image
import shutil
# from server.upscal import upscale_your_image
chrome_options = Options()
chrome_options.add_argument("--headless") 
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--user-agent= Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")


path = './chromedriver.exe'
driver = webdriver.Chrome(options=chrome_options)
a= driver.execute_script("return navigator.userAgent")
print(a)



def download_image(url, save_path, watermark_path, directory, crop, upscale):
    response = requests.get(url)
    if response.status_code == 200:
        if watermark_path:
            image = Image.open(BytesIO(response.content))
            watermark = Image.open(watermark_path)
            image.paste(watermark, (0, 0), watermark)
            image.save(save_path)
            print(f"Image downloaded and watermarked: {save_path}")
        else:
            with open(save_path, 'wb') as file:
                file.write(response.content)
                print(f"Image downloaded and saved without watermarked: {save_path}")
            
            
            if crop:
                crop_image(save_path, f'./image/{directory}/crop')
    else:
        print(f"Failed to download image: {url}")




def load_the_url(url, crop, upscale, watermarke_file = None):
    match = re.search(r'/offer/(\d+)', url)
    if match:
        extracted_number = match.group(1)
        print(extracted_number)
    else:
        extracted_number = 1
        print("No numeric part found in the URL.")
    driver.get(url) 
    driver.execute_script("document.querySelectorAll('img').forEach(img => img.setAttribute('loading', 'eager'));")
    driver.refresh()

    wait = WebDriverWait(driver, 120)
    div_element = wait.until(EC.presence_of_element_located( (By.XPATH, "//*[@id='1081181308831']/div/div/div[1]/div[1]/div/div[2]/div/div")))

    image_elements = div_element.find_elements(By.TAG_NAME, "img")
    print(image_elements)

    directory = Path(f"./image/{extracted_number}")
    directory.mkdir(parents=True,exist_ok=True)
    d = Path(f"./image/{extracted_number}/crop")
    d.mkdir(parents=True,exist_ok=True)
    
    for index, image_element in enumerate(image_elements):
        image_url = image_element.get_attribute("src")
        print(image_url)
        
        if image_url:
            image_name = f"image_{index}.jpg"  
            image_path = f'./image/{extracted_number}/{image_name}'
            
            download_image(image_url, image_path,watermarke_file, extracted_number,crop,upscale)
    zip_file_name = f'{extracted_number}'
    zip_save_directory = 'static'
    zip_path = os.path.join(zip_save_directory,zip_file_name)
    shutil.make_archive(zip_path, 'zip', f'./image/{extracted_number}')

    # upscale_your_image(f'./image/{extracted_number}')
    driver.quit()

    return zip_path, extracted_number


if __name__ == '__main__':
    if len(sys.argv) == 2:
        print(load_the_url(sys.argv[1]))

    elif len(sys.argv) == 3:
        print(load_the_url(sys.argv[1], watermarke_file =sys.argv[2]))
    else:
        print('usage: download_images_1688.py url [zip] [watermark]')
# upscale_your_image('./image/747902474388')


# print(download_images('v', zip=1, watermark=1))  # sys.argv[1]
# load_the_url("https://detail.1688.com/offer/747902474388.html?spm=a261y.7663282.1081181309111.1.419c2257kawxBA")