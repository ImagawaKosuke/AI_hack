from flask import Flask,render_template, request
import openai
import requests
import urllib
import json


#ChatGPTのキー
KEY = "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"
openai.api_key = KEY

#HotPapperのキー
URL_FOOD = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/"
API_KEY_FOOD = "917e8d1ded29b515"

#Vision AI
from google.cloud import vision
from google.oauth2 import service_account
import io
import cv2
import datetime
import numpy as np
 
IMG_URL = "https://imageslabo.com/wp-content/uploads/2019/05/553_dog_chihuahua_7203-973x721.jpg"
 
# 身元証明書のjson読み込み
credentials = service_account.Credentials.from_service_account_file('C:/Users/kosuk/Downloads/bright-gearbox-385710-832e673eaa6a.json')
 
client = vision.ImageAnnotatorClient(credentials=credentials)
image = vision.Image()

# Rail APIを使って駅名・県名から駅の緯度・経度を取得
def RailAPI(station, pref):
    station_url =urllib.parse.quote(station)
    pref_url =urllib.parse.quote(pref)
    api='http://express.heartrails.com/api/json?method=getStations&name={station_name}&prefecture={pref_name}'
    url=api.format(station_name=station_url, pref_name=pref_url)
    response=requests.get(url)
    result_list = json.loads(response.text)['response']['station']
    lng=result_list[0]['x']
    lat=result_list[0]['y']
    return lat, lng

# HotpepperAPIを使って駅の緯度・経度から飲み屋の情報を取得
def HotpepperAPI(lat,lng,liquid,foodcode,number,range,purposes,custom,help,other,feecode,requirement):
    api_key=API_KEY_FOOD#自身で取得したAPI keyを入力
    	
    #リクエストURLを変数に指定する
    api = 'http://webservice.recruit.co.jp/hotpepper/gourmet/v1/'
    if(requirement==1):
        body = {
        'key':API_KEY_FOOD,
        'lat':lat,
        'lng':lng,
        'format':'json',
        'count':int(number),
        'genre':foodcode,
        'cocktail':liquid[0],
        'shochu':liquid[1],
        'sake':liquid[2],
        'wine':liquid[3],
        'range':range,
        'lunch':purposes[0],
        'wedding':purposes[1],
        'free_drink':custom[0],
        'free_food':custom[1],
        'private_room':custom[2],
        'horigotatsu':custom[3],
        'tatami':custom[4],
        'course':custom[5],
        'barrier_free':help[0],
        'parking':help[1],
        'charter':help[2],
        'non_smoking':help[3],
        'card':help[4],
        'open_air':help[5],
        'english':help[6],
        'pet':help[7],
        'child':help[8],
        'credit_card':help[9],
        'sommelier':other[0],
        'night_view':other[1],
        'show':other[2],
        'equipment':other[3],
        'midnight':other[4],
        'midnight_meal':other[5],
        'karaoke':other[6],
        'band':other[7],
        'tv':other[8],
        'budget':feecode
    }
    else:
        body = {
        'key':API_KEY_FOOD,
        'lat':lat,
        'lng':lng,
        'format':'json',
        'count':int(number),
        'genre':foodcode,
        'cocktail':liquid[0],
        'shochu':liquid[1],
        'sake':liquid[2],
        'wine':liquid[3],
        'range':range,
        'lunch':purposes[0],
        'wedding':purposes[1],
        'free_drink':custom[0],
        'free_food':custom[1],
        'private_room':custom[2],
        'horigotatsu':custom[3],
        'tatami':custom[4],
        'course':custom[5],
        'barrier_free':help[0],
        'parking':help[1],
        'charter':help[2],
        'non_smoking':help[3],
        'card':help[4],
        'open_air':help[5],
        'english':help[6],
        'pet':help[7],
        'child':help[8],
        'credit_card':help[9],
        'sommelier':other[0],
        'night_view':other[1],
        'show':other[2],
        'equipment':other[3],
        'midnight':other[4],
        'midnight_meal':other[5],
        'karaoke':other[6],
        'band':other[7],
        'tv':other[8]
    }
            
    url=api.format(key=api_key)
    response = requests.get(url,body)
    result_list = json.loads(response.text)['results']['shop']
    shop_datas=[]
    count=0
    for shop_data in result_list:
        shop_datas.append([shop_data["name"],shop_data["address"],shop_data["urls"]['pc'], shop_data["budget"]['average'],shop_data['logo_image'], shop_data['genre']['name'],shop_data['access'],shop_data['open'],shop_data['close'],'Hotpepper', shop_data['catch']])
        # 0:店名, 1:住所 2:URL 3:費用 4:画像 5:ジャンル名 6:アクセス 7:営業時間 8:定休日 9:ホットペッパー 10:説明
        count+=1
    
    return shop_datas,count

def Answer(question):
    

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": question,
        }]
    )

    response = completion.choices[0].message.content

    return response

app = Flask(__name__, static_folder='/')

def modify_array(answer):
    answers = answer.splitlines()
    explanations = []
    if(len(answers)!=1):
        for i in range(len(answers)):
            sentence = answers[i]
            if sentence.find(':') != -1:
                sentences = sentence.split(':')
                #配列を格納
                explanations.append(sentences[1])
            elif sentence.find('：') != -1:
                sentences = sentence.split('：')
                #配列を格納
                explanations.append(sentences[1])
            else:
                explanations.append(sentence)
            
    return explanations

#「/」へアクセスがあった場合に、"Hello World"の文字列を返す
@app.route("/")
def hello():
    return render_template("index.html")

#「/templates」へアクセスがあった場合に、index.htmlを返す
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

#「/nextpage」へアクセスがあった場合に、next_index.htmlを返す
@app.route("/nextpage", methods=["GET"])
def nextpage():
    return render_template("next_index.html")

@app.route('/nextpage', methods=["GET", "POST"])
def require():
    img_dir = "./manage_Develop/app/static/imgs/"
    if request.method == 'GET': 
        post1 = ""
        post2 = ""
        post3 = ""
        post4 = ""
        post5 = ""
        post6 = ""
        post7 = ""
        post8 = ""
        post9 = ""
        post10 = ""
        post11 = ""
        
    elif request.method == 'POST':
        post1 = request.form.get('station') #完了
        post2 = request.form.get('food') #完了
        post3 = request.form.get('fee')
        post4 = request.form.get('purpose') #完了
        post5 = request.form.get('prefecture') #完了
        post6 = request.form.get('riquid') #完了
        post7 = request.form.get('number') #完了
        post8 = request.form.get('range') #完了
        post9 = request.form.getlist('custom')
        post10 = request.form.getlist('help')
        post11 = request.form.get('other')
        require = request.form.getlist('require')
        img_path=None

        #値段のこだわり
        if not require:
            requirement = 0
        else:
            requirement = 1

        #値段のジャンル分け
        fee = int(post3)
        if(fee<=500):
            feecode = "B009"
        elif(500<fee and fee<=1000):
            feecode = "B010"
        elif(1000<fee and fee<=1500):
            feecode = "B011"
        elif(1500<fee and fee<=2000):
            feecode = "B001"
        elif(2000<fee and fee<=3000):
            feecode = "B002"
        elif(3000<fee and fee<=4000):
            feecode = "B003"
        elif(4000<fee and fee<=5000):
            feecode = "B008"
        elif(5000<fee and fee<=7000):
            feecode = "B004"
        elif(7000<fee and fee<=10000):
            feecode = "B005"
        elif(10000<fee and fee<=15000):
            feecode = "B006"
        elif(15000<fee and fee<=20000):
            feecode = "B012"
        elif(20000<fee and fee<=30000):
            feecode = "B013"
        elif(fee>30000):
            feecode = "B014"

        
        #### POSTにより受け取った画像を読み込む
        stream = request.files['img'].stream
        
        img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
        print(img_array)
        if len(img_array)!=0:
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

        #お酒が充実しているか
        liquid = [0,0,0,0]
        if(post6==0):
            liquid = [0,0,0,0]
        elif(post6==1):
            liquid = [1,0,0,0]
        elif(post6==2):
            liquid = [0,1,0,0]
        elif(post6==3):
            liquid = [0,0,1,0]
        else:
            liquid = [0,0,0,1]
                
        #目的
        purposes = [0,0]
        if(int(post4)==0):
            purposes = [0,0]
            purpose = "飲み会"
        elif(int(post4)==1):
            purposes = [1,0]
            purpose = "ランチ"
        elif(int(post4)==2):
            purposes = [0,1]
            purpose = "２次会"

        #カスタム
        custom = [0,0,0,0,0,0]
        for i in range(0,6):
            result = str(i) in post9
            if(result==True):
                custom[i]=1

        #配慮
        help = [0,0,0,0,0,0,0,0,0,0]
        for i in range(1,12):
            result = str(i) in post10
            if(result==True):
                help[i-1]=1

        #緯度経度
        lat_st, lng_st =RailAPI(post1, post5)

        #その他
        other = [0,0,0,0,0,0,0,0,0]
        if(int(post11)==0):
            other = [0,0,0,0,0,0,0,0,0]
        elif(int(post11)==1):
            other = [1,0,0,0,0,0,0,0,0]
        elif(int(post11)==2):
            other = [0,1,0,0,0,0,0,0,0]
        elif(int(post11)==3):
            other = [0,0,1,0,0,0,0,0,0]
        elif(int(post11)==4):
            other = [0,0,0,1,0,0,0,0,0]
        elif(int(post11)==5):
            other = [0,0,0,0,1,0,0,0,0]
        elif(int(post11)==6):
            other = [0,0,0,0,0,1,0,0,0]
        elif(int(post11)==7):
            other = [0,0,0,0,0,0,1,0,0]
        elif(int(post11)==8):
            other = [0,0,0,0,0,0,0,1,0]
        elif(int(post11)==9):
            other = [0,0,0,0,0,0,0,0,1]
        

        responce, res_len = HotpepperAPI(lat_st, lng_st,liquid,post2,post7,post8,purposes,custom,help,other,feecode,requirement)
        searchcount=15
        if(searchcount>res_len):
            searchcount = res_len

        question = "私は"+purpose+"が目的で"+str(post2)+"のジャンルのレストランに行きたいです\n"
        question += "以下のレストランを上のオーダーをする対象者向けに説明でお願いします\n"
        for i in range(searchcount):
            question +="・"
            question += responce[i][0]
            question += '\n'
        question += " ただし表示は箇条書きかつ改行で「レストラン名:説明」の感じでお願いします。"
        explanation = Answer(question)
        explanations = modify_array(explanation)
        if(len(explanations)==searchcount):
            for i in range(searchcount):
                responce[i][10] = explanations[i]

        purposelist = ["飲み会", "ランチ","二次会"]
        purposejudge = purposelist[int(post4)]
        information = "検索情報\n"+"場所: "+ str(post5) + " "+ str(post1)+ "駅 目的: " + purposejudge+ "\n"
        if(res_len==0):
            information +="以上の条件を基にしたデータは見つかりませんでした。"
    return render_template('next_index.html', info= information, res=responce) 

#app.pyをターミナルから直接呼び出した時だけ、app.run()を実行する
if __name__ == "__main__":
    app.run(debug=True)