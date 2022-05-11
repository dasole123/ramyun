from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import certifi

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'SPARTA'
ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.l2ux3.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbramyun

@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        # DB에서 저장된 데이터 찾아서 HTML에 나타내기 TJ
        recommends = list(db.recommend.find({}, {'_id': False}))
        return render_template("main.html", recommends=recommends)

    except jwt.ExpiredSignatureError: #msg="로그인 시간이 만료되었습니다.
        return redirect(url_for("main_page", msg=token_receive))
    except jwt.exceptions.DecodeError:#msg="로그인 정보가 존재하지 않습니다.
        return redirect(url_for("main_page", msg=token_receive))



@app.route('/index')
def main_page():
    token_receive = request.args.get("msg")
    print(token_receive)
    recommends = list(db.recommend.find({}, {'_id': False}))
    return render_template("main.html", recommends=recommends, token=token_receive)



@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    nickname_receive = request.form['nickname_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                               # 아이디
        "password": password_hash,                                  # 비밀번호
        "profile_name": username_receive,                           # 프로필 이름 기본값은 아이디
        "profile_pic": "",                                          # 프로필 사진 파일 이름
        "profile_pic_real": "profile_pics/profile_placeholder.png", # 프로필 사진 기본 이미지
        "nickname_receive": nickname_receive                        # 닉네임
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})

@app.route("/recommend", methods=["POST"])
def recommend_post():
    title_receive = request.form['title_give']
    kind_receive = request.form['kind_give']
    spicy_receive = request.form['spicy_give']

    comment_receive = request.form['comment_give']
    like_receive = request.form['num_give']

    file = request.files["file_give"]
    extension = file.filename.split('.')[-1]  # 항상 jpg 가 아닐수 있자나 [-1] 마지막걸 가져옴 . 기준으로 나누고 TJ
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    filename = f'file-{mytime}'
    # save_to =f'static/{filename}.jpg'  를 아래로 변경 확장자 달라도 가능하게 저장 TJ
    save_to = f'static/{filename}.{extension}'

    file.save(save_to)

    doc = {
        'title': title_receive,
        'kind': kind_receive,
        'pepper': spicy_receive,
        'comment': comment_receive,
        'file': f'{filename}.{extension}',
        'like': like_receive
    }
    db.recommend.insert_one(doc)

    return jsonify({'msg': 'save 완료!'})

# 좋아요 기능

@app.route('/like', methods=['POST'])
def like():
    num_receive = request.form["num_give"]
    title_receive = request.form["title_give"]

    target_post = db.recommend.find_one({'title': title_receive})
    current_like = int(target_post['like'])
    plus_like = str(current_like+num_receive)

    db.recommend.update_one({'like': plus_like})

    return jsonify({'msg': '좋아요 +1'})

# @app.route("/recommend", methods=["GET"])
# def recommend_get():
#     recommend_list = list(db.recommend.find({}, {'_id': False}))
#
#     return jsonify({'recommends': recommend_list})

#로그인 기본 페이지 링크
@app.route('/login_page')
def login_page():
    return render_template('index.html')

# 검색기능
@app.route("/search", methods=["GET"])
def search_get():
    #search_receive = request.form['search_give']
    #search_recommend_list = list(db.recommend.find({'kind':f'{search_receive}'}, {'_id': False}))
    search_recommend_list = list(db.recommend.find({'kind':'너구리'}, {'_id': False}))
    return jsonify({'search_recommends': search_recommend_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)