from google.cloud import vision
from google.oauth2 import service_account
import io
 
IMG_URL = "https://imageslabo.com/wp-content/uploads/2019/05/553_dog_chihuahua_7203-973x721.jpg"
 
# 身元証明書のjson読み込み
credentials = service_account.Credentials.from_service_account_file('C:/Users/kosuk/Downloads/bright-gearbox-385710-832e673eaa6a.json')
 
client = vision.ImageAnnotatorClient(credentials=credentials)
image = vision.Image()


with io.open('./コラージュ画像/B0628B6F-333A-4426-A4D9-36390D680CF2.jpg','rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)

response = client.label_detection(image=image)
labels = response.label_annotations
 
 
for label in labels:
    print(label.description + ":" + str(label.score))
'''
image.source.image_uri = IMG_URL
 
response = client.label_detection(image=image)
labels = response.label_annotations
 
 
for label in labels:
    print(label.description + ":" + str(label.score))
 
if response.error.message:
    raise Exception(
        '{}\nFor more info on error messages, check: '
        'https://cloud.google.com/apis/design/errors'.format(
            response.error.message))
'''
