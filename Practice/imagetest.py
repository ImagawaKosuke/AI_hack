import cv2
import datetime
import numpy as np
from flask import Flask, render_template, request
from google.cloud import vision
from google.oauth2 import service_account
import io
 
IMG_URL = "https://imageslabo.com/wp-content/uploads/2019/05/553_dog_chihuahua_7203-973x721.jpg"
 
# 身元証明書のjson読み込み
credentials = service_account.Credentials.from_service_account_file('C:/Users/kosuk/Downloads/bright-gearbox-385710-832e673eaa6a.json')
 
client = vision.ImageAnnotatorClient(credentials=credentials)
image = vision.Image()

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def hello_world():
    img_dir = "./Practice/static/imgs/"
    if request.method == 'GET': img_path=None
    elif request.method == 'POST':
        #### POSTにより受け取った画像を読み込む
        stream = request.files['img'].stream
        
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, 1)
        #### 現在時刻を名前として「imgs/」に保存する
        dt_now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        img_path = img_dir + dt_now + ".jpg"
        cv2.imwrite(img_path, img)
        with io.open(img_path,'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        response = client.label_detection(image=image)
        labels = response.label_annotations
        
        for label in labels:
            print(label.description + ":" + str(label.score))
    #### 保存した画像ファイルのpathをHTMLに渡す
    return render_template('imagetest.html', img_path=img_path) 

if __name__ == "__main__":
    app.run(debug=True)