from PIL import Image
import requests, getpass, re
from time import sleep

class Helper(object):
    def __init__(self, val_url, login_url, main_url, login_data):
        self.session = requests.Session()
        self.val_url = val_url
        self.login_url = login_url
        self.main_url = main_url
        self.login_data = login_data
        self.type = type
        self.Succeeded = []
        self.turn = 0
        self.course = []

    #show the image of identifying code
    def showVal(self):
        val_data = self.session.get(self.val_url).content
        f = open('./val.jpg', 'wb')
        f.write(val_data)
        f.close()
        im = Image.open('./val.jpg')
        im.show()

    #login operation
    def Login(self, Needname = True):
        logged = False

        #try once
        self.session.post(self.login_url, data=self.login_data)
        #real login
        while True:
            if Needname:
                self.login_data['j_username'] = input('Name:')
                self.login_data['j_password'] = getpass.getpass('Password(invisible):')
            self.showVal()
            self.login_data['_login_image_'] = input('Identifying Code:')
            self.session.post(self.login_url, data=self.login_data)
            logged = '用户登陆超时或访问内容不存在' not in self.session.get(self.main_url).text
            if logged:
                break
            else:
                result = input('Login Failed, retry?(y/n):')
                if result == 'n':
                    break
        return logged
