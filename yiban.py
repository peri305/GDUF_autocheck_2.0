import base64
import requests
from util import get_today
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA


class YiBan:
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 yiban_iOS/5.0.5",
    }

    def __init__(self, account, passwd, address):
        self.account = account
        self.passwd = passwd
        self.address = address
        self.session = requests.session()
        self.name = ""
        self.studentID = ""
        self.url = ""
        self.result = {}
        self.result_str = ""

    def request(self, url, method="get", headers=HEADERS, params=None, allow_redirects=True):
        if method == "get":
            req = self.session.get(
                url=url, params=params, timeout=10, headers=headers, allow_redirects=allow_redirects)
        else:
            req = self.session.post(
                url=url, data=params, timeout=10, headers=headers, allow_redirects=allow_redirects)
        try:
            return req.json()
        except:
            return None

    def encryptPassword(self, pwd):
        # 密码加密
        PUBLIC_KEY = '''-----BEGIN PUBLIC KEY-----
            MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEA6aTDM8BhCS8O0wlx2KzA
            Ajffez4G4A/QSnn1ZDuvLRbKBHm0vVBtBhD03QUnnHXvqigsOOwr4onUeNljegIC
            XC9h5exLFidQVB58MBjItMA81YVlZKBY9zth1neHeRTWlFTCx+WasvbS0HuYpF8+
            KPl7LJPjtI4XAAOLBntQGnPwCX2Ff/LgwqkZbOrHHkN444iLmViCXxNUDUMUR9bP
            A9/I5kwfyZ/mM5m8+IPhSXZ0f2uw1WLov1P4aeKkaaKCf5eL3n7/2vgq7kw2qSmR
            AGBZzW45PsjOEvygXFOy2n7AXL9nHogDiMdbe4aY2VT70sl0ccc4uvVOvVBMinOp
            d2rEpX0/8YE0dRXxukrM7i+r6lWy1lSKbP+0tQxQHNa/Cjg5W3uU+W9YmNUFc1w/
            7QT4SZrnRBEo++Xf9D3YNaOCFZXhy63IpY4eTQCJFQcXdnRbTXEdC3CtWNd7SV/h
            mfJYekb3GEV+10xLOvpe/+tCTeCDpFDJP6UuzLXBBADL2oV3D56hYlOlscjBokNU
            AYYlWgfwA91NjDsWW9mwapm/eLs4FNyH0JcMFTWH9dnl8B7PCUra/Lg/IVv6HkFE
            uCL7hVXGMbw2BZuCIC2VG1ZQ6QD64X8g5zL+HDsusQDbEJV2ZtojalTIjpxMksbR
            ZRsH+P3+NNOZOEwUdjJUAx8CAwEAAQ==
            -----END PUBLIC KEY-----'''
        cipher = PKCS1_v1_5.new(RSA.importKey(PUBLIC_KEY))
        cipher_text = base64.b64encode(
            cipher.encrypt(bytes(pwd, encoding="utf8")))
        return cipher_text.decode("utf-8")

    def login(self):
        url = "https://mobile.yiban.cn/api/v4/passport/login"
        param = {
            "device": "APPLE",
            "v": "5.0.2",
            "mobile": int(self.account),
            "password": self.encryptPassword(self.passwd),
            "token": "",
            "ct": "2",
            "identify": "0",
            "sversion": "25",
            "app": "1",
            "apn": "wifi",
            "authCode": "",
            "sig": "934932a8993b5e23"
        }
        header = {
            'Origin': 'https://mobile.yiban.cn',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 yiban_iOS/5.0.2',
            'Referer': 'https://mobile.yiban.cn',
            'AppVersion': '5.0.2'
        }
        response = self.request(
            url=url, method="post", params=param, headers=header)
        if response['response'] == 100:
            self.access_token = response['data']['access_token']
            # print(self.access_token)
            return response
        else:
            raise Exception("账号或密码错误")

    def getHome(self):
        params = {
            "access_token": self.access_token,
        }
        r = self.request(
            url="https://mobile.yiban.cn/api/v4/home", params=params)
        self.name = r["data"]["user"]["userName"]
        for i in r["data"]["hotApps"]:
            if i["name"] == "易广金":
                self.url = i["url"]
        return r

    def oauth(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 yiban_iOS/5.0.5",
            "Cookie": "loginToken={}; yibanM_user_token={}".format(self.access_token, self.access_token),
            "loginToken": self.access_token
        }

        data = {
            "client_id": "0b77c3ac53bd5c65",
            "redirect_uri": self.url,
        }

        oauth = self.request(
            url="https://oauth.yiban.cn/code/usersure", method="post", params=data, headers=headers)

        return oauth["reUrl"]

    def submit(self):
        self.HEADERS["loginToken"] = self.access_token

        auth_1 = self.session.get(
            url=self.oauth(), headers=self.HEADERS, allow_redirects=False)

        auth_2 = self.session.get(
            url=auth_1.headers["Location"], headers=self.HEADERS, allow_redirects=False)

        home = self.session.get(
            url=auth_2.headers["Location"], headers=self.HEADERS, allow_redirects=False)

        self.studentID = home.headers["Location"].split("studentID=")[1]

        bind = self.request(
            url="https://ygj.gduf.edu.cn/Handler/device.ashx?flag=checkBindDevice", headers=self.HEADERS)

        params = {
            "flag": "save",
            "studentID": "{0}".format(self.studentID),
            "date": "{0}".format(get_today()),
            "health": "体温37.3℃以下（正常）",
            "address": "{0}".format(self.address),
            "isTouch": "否",
            "isPatient": "不是"
        }

        self.result = self.request(
            url="https://ygj.gduf.edu.cn/Handler/health.ashx?", method="post", headers=self.HEADERS, params=params)

        if int(self.result["code"]) != 0:
            self.result_str = "{0} 打卡失败，失败原因：{1}".format(
                self.name, self.result["msg"])
            return True
        else:
            return False
