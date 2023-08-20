from PIL import Image
import urllib.request
import requests
from io import BytesIO


img = "https://rukminim2.flixcart.com/image/2000/2000/xif0q/t-shirt/z/k/z/m-half-taddy-one-nb-nicky-boy-original-imaghwkg4mxgwtgm.jpeg?q=70"
# urllib.request.urlretrieve(img)
response = requests.get(img)
im = Image.open(BytesIO(response.content))
image_height = 200
im.resize((int(im.width * (image_height / im.height)), image_height))
# im =  Image.open(BytesIO(img))


im.show()