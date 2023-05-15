from flask import Flask,render_template, request
import openai

KEY = "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"
openai.api_key = KEY

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
    if request.method == 'GET': 
        post1 = ""
        post2 = ""
        post3 = ""
        post4 = ""
    elif request.method == 'POST':
        post1 = request.form.get('place')
        post2 = request.form.get('food')
        post3 = request.form.get('number')
        post4 = request.form.get('purpose')
        question = '''
            私は'''+str(post4)+"が目的で"+str(post3)+"で"+str(post2)+'''を食べたいです。'''+str(post1)+'''でおすすめのレストランを10個箇条書きで教えてください。
            ただし表示は「レストラン名:説明」の感じでお願いします。
            '''
        post = Answer(question)
        information = "検索情報\n"+"場所: "+ str(post1)+ " 食べたいもの: "+ str(post2) + " 人数: "+ str(post3) + " 目的: "+ str(post4)
    return render_template('next_index.html', info= information, output=post) 


#app.pyをターミナルから直接呼び出した時だけ、app.run()を実行する
if __name__ == "__main__":
    app.run(debug=True)