import json
import os
import time
from datetime import date, datetime
from typing import List

from flask import redirect, request
from flask_cors import CORS

from webServerConf import app, web_db

import pandalearning as pdl
from pdlearn import user, WebMessage, WebQrUrl, UserInfo


@app.before_first_request
def create_db():
    '创建表格、插入数据'
    # Recreate database each time for demo
    web_db.drop_all()
    web_db.create_all()


def request_parse(req_data):
    data = None
    if req_data.method == 'POST':
        data = req_data.json
    elif req_data.method == 'GET':
        data = req_data.args
    return data


def resp(code=200, data=dict(), status='success', resp_code=200):
    resp = {'code': code, 'data': data, 'status': status}
    return resp, resp_code


def resp_ok(resp_data=dict()):
    resp = {'code': 200, 'data': resp_data, 'status': "success"}
    return resp


def resp_db_ok(res_rows=None):
    resp = {'code': 200, 'data': [
        dict(zip(result.keys(), result)) for result in res_rows], 'status': "success"}
    return resp


def serialize(model):
    from sqlalchemy.orm import class_mapper
    columns = [c.key for c in class_mapper(model.__class__).columns]
    return dict((c, getattr(model, c)) for c in columns)


def resp_models_ok(models=[None]):
    if not isinstance(models, List):
        models = [models]
    list_json_models = [serialize(model) for model in models]
    resp = {'code': 200, 'data':
            list_json_models, 'status': "success"}
    return resp


def resp_not_found(resp_msg=None):
    resp = {'code': 404, 'msg': resp_msg, 'status': "404 NOT FOUND"}
    return resp, 404


def resp_err(resp_msg=None):
    resp = {'code': 500, 'msg': resp_msg, 'status': "ERRO"}
    return resp, 500


@app.route('/')
def hello_world():
    return redirect('/static/index.html', code=302)


@app.route('/jump')
def hello_world():
    return redirect('/static/index.html', code=302)


@app.route('/api/sleep/<sleep_time>')
def sleep(sleep_time):
    time.sleep(float(sleep_time))
    resp_data = dict()
    resp_data['sleep'] = sleep_time
    return resp_ok(resp_data)


@app.route('/api/update')
def update():
    try:
        shell = "git -C /xuexi/code/TechXueXi pull $Sourcepath $pullbranche "
        req_data = request_parse(request)
        params = req_data['params'] if 'params' in req_data else ''
        if len(params) > 1:
            shell += params[1]
        msg = os.popen(shell).readlines()[-1]
        if "up to date" in msg:
            return resp_ok("当前代码已经是最新的了")
        else:
            os.popen("cp -r /xuexi/code/TechXueXi/SourcePackages/* /xuexi")
            return resp_ok("代码更新完成"+msg)
    except Exception as e:
        return resp_err("更新失败："+str(e))


@app.route('/api/list')
def list():
    return resp_models_ok(UserInfo.query.all())


@app.route('/api/refresh_all_cookies')
def refresh_all_cookies():
    user_status = user.refresh_all_cookies(display_score=True)
    user_infos = UserInfo.query.all()
    for user_info in user_infos:
        web_db.session.delete(user_info)
    for (uid, status) in user_status.items():
        web_db.session.add(UserInfo(uid, status))
    web_db.session.commit()
    return list()


@app.route('/api/add')
def add():
    pdl.add_user()
    return resp_ok('登录成功')


@app.route('/api/learn')
def learn():
    ''' 新线程无法操控内存数据库'''
    names = pdl.get_all_user_name()
    if len(names) <= 1:
        return resp_ok('请添加用户')
    else:
        pdl.start(None)
        return resp_ok('全部账号开始学习：{}'.format(names))


@app.route('/api/learn_by_nick_name/<nick_name>')
def learn_by_nick_name(nick_name):
    names = pdl.get_all_user_name()
    if len(names) <= 1:
        return resp_ok('请添加用户')
    else:
        names = pdl.get_all_user_name()
        for name in names:
            if nick_name == name:
                pdl.start(nick_name)
                return resp_ok('开始学习：{}'.format(nick_name))


@app.route('/api/learn_by_uid/<uid>')
def learn_by_uid(uid):
    pdl.start_learn(uid, None)
    return resp_ok('开始学习：{}'.format(user.get_fullname(uid)))


@app.route('/api/list_user')
def list_user():
    return resp_ok(user.list_user(printing=False))


@app.route('/api/list_qrurls')
def list_qrurls():
    qrurls = WebQrUrl.query.all()
    for qrurl in qrurls:
        # print('--------------------------------\n秒：{}\n--------------------------------'.format(
        #     (datetime.now() - qrurl.timestamp).seconds))
        if (datetime.now() - qrurl.timestamp).seconds > 300:
            web_db.session.delete(qrurl)
    web_db.session.commit()
    return resp_models_ok(qrurls)


@app.route('/api/list_messages')
def list_messages():
    messages = WebMessage.query.all()
    for message in messages:
        # print('--------------------------------\n分：{}\n--------------------------------'.format(
        #     (datetime.now() - message.timestamp).seconds/60))
        if (datetime.now() - message.timestamp).seconds > 300:
            web_db.session.delete(message)
    web_db.session.commit()
    return resp_models_ok(messages)


if __name__ == "__main__":
    CORS(app, supports_credentials=True)
    app.run(host='0.0.0.0', port='80', debug=True)
