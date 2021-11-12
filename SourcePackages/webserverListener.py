import json
import os
from re import T
import time
from datetime import date, datetime
from typing import List

from flask import redirect, request
from flask_cors import CORS

import pandalearning as pdl
from pdlearn import user
from webServerConf import UserInfo, WebMessage, WebQrUrl, app, web_db, LAST_STATUS_REFRESH_ALL_COOKIES


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


def web_log_and_resp_ok(resp_data=dict()):
    web_log(resp_data)
    return resp_ok(resp_data)


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


def web_log(send_log):
    print(send_log)
    web_db.session.add(WebMessage(send_log))
    web_db.session.commit()


@app.route('/')
def hello_world():
    return redirect('/static/index.html', code=302)


@app.route('/jump')
def jump_app():
    return redirect('/static/jump.html', code=302)


@app.route('/api/sleep/<sleep_time>')
def sleep(sleep_time):
    time.sleep(float(sleep_time))
    resp_data = dict()
    resp_data['sleep'] = sleep_time
    return resp_ok(resp_data)


@app.route('/api/now')
def now():
    return resp_ok(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


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
            msg += "当前代码已经是最新的了"
            return web_log_and_resp_ok("当前代码已经是最新的了")
        else:

            os.popen("cp -r /xuexi/code/TechXueXi/SourcePackages/* /xuexi")
            return web_log_and_resp_ok("代码更新完成"+msg)
    except Exception as e:
        return resp_err("更新失败："+str(e))


@app.route('/api/list_users_status_from_memory')
def list_users_status_from_memory():
    return resp_models_ok(web_db.session.query(UserInfo).all())


@app.route('/api/refresh_all_cookies')
def refresh_all_cookies():
    return do_refresh_all_cookies(force=False)


@app.route('/api/force_refresh_all_cookies')
def force_refresh_all_cookies():
    return do_refresh_all_cookies(force=True)


def do_refresh_all_cookies(force):
    if (not force) and LAST_STATUS_REFRESH_ALL_COOKIES['USER_STATUS'] and ((datetime.now() - LAST_STATUS_REFRESH_ALL_COOKIES['TIME']).seconds < 30):
        return list_users_status_from_memory()
    LAST_STATUS_REFRESH_ALL_COOKIES['TIME'] = datetime.now()
    user_status = user.refresh_all_cookies(display_score=True)
    LAST_STATUS_REFRESH_ALL_COOKIES['USER_STATUS'] = user_status
    user_infos = web_db.session.query(UserInfo).all()
    for user_info in user_infos:
        web_db.session.delete(user_info)
    for (uid, status) in user_status.items():
        web_db.session.add(UserInfo(uid, status))
    web_db.session.commit()
    return list_users_status_from_memory()


@app.route('/api/add')
def add():

    filename = os.path.join('user', 'user_status.json')
    new = []
    bad_file_flag=False
    error_line_index = 8
    with open(filename, 'r', encoding='utf-8') as conf:
        for line in conf:
            new.append(line)
        # 保险起见，判断两次
        if  '"0":"default"' in new[error_line_index-1] and '},' in new[error_line_index+1]:
            bad_file_flag=True
            print("================================================")
            print("检测到文件出现问题~~~")
            print("正在冒死修复", filename)
            # print(new[error_line_index-1])
            # 一般错误为'        "0":"default"\n'
            new[error_line_index-1] = new[error_line_index-1][:-1]+',\n'
            new[error_line_index] = ''
            new[error_line_index+1] = ''

    if bad_file_flag:
        with open(filename, 'w', encoding='utf-8') as conf:
            for line in new:
                conf.write(line)
            print("修复完毕~~~")
            print("================================================")

    pdl.add_user()
    sleep(3) and do_refresh_all_cookies(force=True)
    return web_log_and_resp_ok('ヾ(o◕∀◕)ﾉヾ☆登录成功，手动点击UID开始学习★ヾ(≧O≦)〃嗷~')


@app.route('/api/learn')
def learn():
    ''' 新线程无法操控内存数据库'''
    # web_db.session.add(WebMessage('新线程无法操控内存数据库'))
    # web_db.session.commit()
    # return resp_models_ok(WebMessage('新线程无法操控内存数据库'))
    names = pdl.get_all_user_name()
    if len(names) <= 1:
        return web_log_and_resp_ok('请添加用户')
    else:
        pdl.start(None)
        return web_log_and_resp_ok('全部账号开始学习：{}'.format(names))


@app.route('/api/learn_by_nick_name/<nick_name>')
def learn_by_nick_name(nick_name):
    names = pdl.get_all_user_name()
    if len(names) <= 1:
        return web_log_and_resp_ok('请添加用户')
    else:
        names = pdl.get_all_user_name()
        for name in names:
            if nick_name == name:
                pdl.start(nick_name)
                return web_log_and_resp_ok('开始学习：{}'.format(nick_name))


@app.route('/api/learn_by_uid/<uid>')
def learn_by_uid(uid):
    pdl.start_learn(uid, None)
    return web_log_and_resp_ok('开始学习：{}'.format(user.get_fullname(uid)))


@app.route('/api/list_user')
def list_user():
    return resp_ok(user.list_user(printing=False))


@app.route('/api/remove_cookie/<uid>')
def remove_cookie(uid):
    user_name = user.get_fullname(uid)
    msg = 'uid: {}  ,username: {} 状态清除成功'.format(uid, user_name)
    user.remove_cookie(uid)
    web_log(msg)
    return resp_models_ok(WebMessage(msg))


@app.route('/api/list_qrurls')
def list_qrurls():
    qrurls = web_db.session.query(WebQrUrl).all()
    # print(
    #     '二维码:', [((datetime.now() - qrurl.timestamp).seconds, qrurl.timestamp) for qrurl in qrurls])
    for qrurl in qrurls:
        # print('--------------------------------\n秒：{}\n--------------------------------'.format(
        #     (datetime.now() - qrurl.timestamp).seconds))
        if (datetime.now() - qrurl.timestamp).seconds > 300:
            web_log('超时，二维码已被移除: {}'.format(qrurl.id))
            web_db.session.delete(qrurl)
    web_db.session.commit()
    return resp_models_ok(qrurls)


@app.route('/api/list_messages')
def list_messages():
    messages = web_db.session.query(WebMessage).all()
    # print(
    #     '消息:', [(datetime.now() - message.timestamp).seconds for message in messages])
    for message in messages:
        # print('--------------------------------\n分：{}\n--------------------------------'.format(
        #     (datetime.now() - message.timestamp).seconds/60))
        if (datetime.now() - message.timestamp).seconds > 300:
            # web_log('超时，消息已被移除: {} - {}'.format(message.id, message.timestamp))
            web_db.session.delete(message)
    web_db.session.commit()
    return resp_models_ok(messages)


if __name__ == "__main__":
    CORS(app, supports_credentials=True)
    app.run(host='0.0.0.0', port='80', debug=True)
