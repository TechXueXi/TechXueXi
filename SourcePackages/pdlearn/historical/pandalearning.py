from pdlearn import dingding
from pdlearn import user

def user_flag(dd_status, uname):
    if False and dd_status:
        cookies = dingding.dd_login_status(uname, has_dd=True)
    else:
        # if (input("是否保存钉钉帐户密码，保存后可后免登陆学 xi (Y/N) ")) not in ["y", "Y"]:
        if True:
            cookies = user.get_cookie(uname)
            if not cookies:
                print("未找到有效登录信息，需要登录")
                driver_login = Mydriver(nohead=False)
                cookies = driver_login.login()
                driver_login.quit()
        else:
            cookies = dingding.dd_login_status(uname)
    a_log = user.get_a_log(uname)
    v_log = user.get_v_log(uname)
    d_log = user.get_d_log(uname)
    return cookies, a_log, v_log, d_log

if __name__ == '__main__':
    dd_status, uname = user.get_user()
    cookies, a_log, v_log = user_flag(dd_status, uname)