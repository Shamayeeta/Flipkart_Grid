import requests
from bs4 import BeautifulSoup

class ExtractImage():

    def __init__(self, url):
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
                    final_image_urls.append(img_url)
            except:
                pass
        return final_image_urls

if __name__ == '__main__':
    obj = ExtractImage('https://www.flipkart.com/scube-designs-u-neck-women-blouse/p/itm281eaa5a73c28')
    print(obj.get_image())