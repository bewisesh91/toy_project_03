from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient('localhost', 27017)
# client = MongoClient('내AWS아이피', 27017, username="아이디", password="비밀번호")
db = client.db_flask_practice3


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/goodplace', methods=["GET"])
def get_goodplace():
    # 맛집 목록을 반환하는 API
    # 우선, db에서 맛집 정보를 가져온다.
    goodplace_list = list(db.matjips.find({}, {'_id': False}))
    # goodplace_list 라는 키 값에 맛집 목록을 담아 클라이언트에게 반환합니다.
    return jsonify({'result': 'success', 'goodplace_list': goodplace_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)