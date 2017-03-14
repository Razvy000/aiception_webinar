# call aiception directly

# pip install requests

from pprint import pprint

from aiception import detect_object
from aiception import detect_object_sync


token = "xxxxxxxxxxxxxxxxxxxx"

image_url = "https://s-media-cache-ak0.pinimg.com/736x/d6/e0/99/d6e099456899689e563f534e2cca476e.jpg"

r = detect_object_sync(token, image_url)
pprint(r)

print('label: ' + r['answer'][0][0])
print('score: ' + str(r['answer'][0][1]))
