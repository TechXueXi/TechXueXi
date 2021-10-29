from webserverListener import Message, QrUrl, db

from datetime import date, datetime


class WebHandler:

    def __init__(self):
        try:
            db.create_all()
        except Exception as e:
            pass

    def add_message(self, message):
        try:
            msg = Message(message.strip(), datetime.now())
            db.session.add(msg)
            db.session.commit()
        except Exception as e:
            pass

    def add_qrurl(self, url):
        try:
            qrurl = QrUrl(url)
            db.session.add(qrurl, datetime.now())
            db.session.commit()
        except Exception as e:
            pass
