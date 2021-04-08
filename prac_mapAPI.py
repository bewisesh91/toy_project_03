from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient('localhost', 27017)
# client = MongoClient('내AWS아이피', 27017, username="아이디", password="비밀번호")
db = client.db_flask_practice3


@app.route('/')
def main():
    return render_template("index.html")


@app.route('/map')
def test_map():
    return render_template("prac_mapAPI.html")


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)