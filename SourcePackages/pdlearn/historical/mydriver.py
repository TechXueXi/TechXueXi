class Mydriver:
    def dd_login(self, d_name, pwd):
        __login_status = False
        self.driver.get(
            "https://login.dingtalk.com/login/index.htm?"
            "goto=https%3A%2F%2Foapi.dingtalk.com%2Fconnect%2Foauth2%2Fsns_authorize"
            "%3Fappid%3Ddingoankubyrfkttorhpou%26response_type%3Dcode%26scope%3Dsnsapi"
            "_login%26redirect_uri%3Dhttps%3A%2F%2Fpc-api.xuexi.cn%2Fopen%2Fapi%2Fsns%2Fcallback"
        )
        self.driver.find_elements_by_id("mobilePlaceholder")[0].click()
        self.driver.find_element_by_id("mobile").send_keys(d_name)
        self.driver.find_elements_by_id("mobilePlaceholder")[1].click()
        self.driver.find_element_by_id("pwd").send_keys(pwd)
        self.driver.find_element_by_id("loginBtn").click()
        try:
            print("登陆中...")
            WebDriverWait(self.driver, 2, 0.1).until(lambda driver: driver.find_element_by_class_name("modal"))
            print(self.driver.find_element_by_class_name("modal").find_elements_by_tag_name("div")[0].text)
            self.driver.quit()
            __login_status = False
        except:
            __login_status = True
        return __login_status