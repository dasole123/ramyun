from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from datetime import datetime


from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.l2ux3.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbramyun

@app.route('/')
def home():
    return render_template('main.html')

@app.route("/recommend", methods=["POST"])
def recommend_post():
    title_receive = request.form['title_give']
    kind_receive = request.form['kind_give']
    spicy_receive = request.form['spicy_give']

    comment_receive = request.form['comment_give']

    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]  # 항상 jpg 가 아닐수 있자나 [-1] 마지막걸 가져옴 . 기준으로 나누고
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'file-{mytime}'
    # save_to =f'static/{filename}.jpg'  를 아래로 변경 확장자 달라도 가능하게 저장
    save_to = f'static/{filename}.{extension}'

    file.save(save_to)

    doc = {
        'title': title_receive,
        'kind': kind_receive,
        'pepper': spicy_receive,
        'comment': comment_receive,
        'file': f'{filename}.{extension}'
    }
    db.recommend.insert_one(doc)

    return jsonify({'msg': 'save 완료!'})

@app.route("/recommend", methods=["GET"])
def recommend_get():
    recommend_list = list(db.recommend.find({}, {'_id': False}))

    return jsonify({'recommends': recommend_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)