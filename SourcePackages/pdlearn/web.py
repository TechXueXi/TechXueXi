from webServerConf import WebMessage, WebQrUrl, web_db

from datetime import date, datetime


class WebHandler:

    def __init__(self):
        try:
            web_db.create_all()
        except Exception as e:
            pass

    def add_message(self, message):
        try:
            msg = WebMessage(message.strip())
            web_db.session.add(msg)
            web_db.session.commit()
        except Exception as e:
            web_db.session.rollback()
            print(e)
            pass

    def add_qrurl(self, url):
        try:
            qrurl = WebQrUrl(url)
            web_db.session.add(qrurl)
            web_db.session.commit()
        except Exception as e:
            web_db.session.rollback()
            print(e)
            pass
