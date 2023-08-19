import requests
from bs4 import BeautifulSoup

class Extract_Image():

    def __init__(self, url = ""):
        self.url = url

    def set_url(self, url):
        self.url = url

    def get_image(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        image_tags = soup.find_all('img')
        image_tags = [img.get('src') for img in image_tags]
        final_image_urls = []
        for img_url in image_tags:
            try:
                if img_url.find('rukminim2.flixcart.com') == -1:
                    continue
                else :
                    start_index = img_url.find("/image/") + len("/image/")
                    mid_index = img_url.find("/", start_index)
                    end_index = img_url.find("/", mid_index+1)

                    img_url = img_url[:start_index] + "2000/2000" + img_url[end_index:]
                    final_image_urls.append(img_url)
            except:
                pass
        return final_image_urls

if __name__ == '__main__':
    obj = Extract_Image('https://www.flipkart.com/scube-designs-u-neck-women-blouse/p/itm281eaa5a73c28')
    print(obj.get_image())