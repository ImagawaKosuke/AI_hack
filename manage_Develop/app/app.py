from flask import Flask,render_template, request

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
def hello_world():
    if request.method == 'GET': post = ""
    elif request.method == 'POST': post = request.form['input']
    return render_template('next_index.html', output=post) 


#app.pyをターミナルから直接呼び出した時だけ、app.run()を実行する
if __name__ == "__main__":
    app.run(debug=True)