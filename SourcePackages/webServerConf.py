from datetime import date, datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

SQLOTE_MEMORY = 'sqlite:///:memory:'
LAST_STATUS_REFRESH_ALL_COOKIES = {'TIME': datetime.now(), 'USER_STATUS': None}
app.config['SQLALCHEMY_DATABASE_URI'] = SQLOTE_MEMORY
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

web_db = SQLAlchemy(app)


class WebMessage(web_db.Model):
    id = web_db.Column(web_db.Integer, primary_key=True)
    text = web_db.Column(web_db.String())
    timestamp = web_db.Column(web_db.DateTime, default=datetime.now)

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return '<Message: %r>' % self.text


class WebQrUrl(web_db.Model):
    id = web_db.Column(web_db.Integer, primary_key=True)
    url = web_db.Column(web_db.String())
    timestamp = web_db.Column(web_db.DateTime, default=datetime.now)

    def __init__(self, url):
        self.url = url

    def __repr__(self):
        return '<QrUrl: %r>' % self.url


class UserInfo(web_db.Model):
    id = web_db.Column(web_db.Integer, primary_key=True)
    uid = web_db.Column(web_db.String())
    status = web_db.Column(web_db.String())
    timestamp = web_db.Column(web_db.DateTime, default=datetime.now)

    def __init__(self, uid, status):
        self.uid = uid
        self.status = status

    def __repr__(self):
        return '<QrUrl: %r %r>' % (self.uid, self.status)
if __name__ == '__main__':
    print("执行错误，请运行： webserverListener.py")