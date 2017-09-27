from PIL import Image
import requests, getpass, re
from time import sleep

class Helper(object):
    def __init__(self, val_url, login_url, token_url, post_url, main_url, login_data, post_data, token_pattern,\
                 Msg_pattern='showMsg\("(.*?)"\)', type='rx'):
        self.session = requests.Session()
        self.val_url = val_url
        self.login_url = login_url
        self.token_url = token_url
        self.post_url = post_url
        self.main_url = main_url
        self.login_data = login_data
        self.post_data = post_data
        self.token_pattern = token_pattern
        self.Msg_pattern = Msg_pattern
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
            print(self.login_url)
            print(self.login_data)
            print(logged)
            if logged:
                break
            else:
                result = input('Login Failed, retry?(y/n):')
                if result == 'n':
                    break
        return logged

    #get courses
    def getCourse(self, Get=True):
        if not Get:
            self.course = [

            ]
            return
        num1 = '1'
        num2 = '2'
        while True:
            num1 = input('Course Number(8)(press Enter if you finished)：')
            if num1 == '':
                break
            num2 = input('Number：')
            course_item = '2017-2018-1;' + num1 + ';' + num2 + ';'
            self.course.append(course_item)
    #get token
    def getToken(self):
        token_text = self.session.get(self.token_url).text
        if '用户登陆超时或访问内容不存在' in token_text:
            return 'LogError'
        elif '频繁' in token_text:
            return 'OpError'
        token_list = re.findall(self.token_pattern, token_text)
        if len(token_list) == 0:
            print(token_text)
            return 'OtherError'
        return token_list[0]

    #Process returned information
    def Process(self, Result):
        R_list = Result.split('!')
        i = 0
        for item in R_list:
            if '冲突' in item or '不存在' in item or '重修' in item or '限' in item:
                if '冲突' in item and self.turn > 1:
                    self.Succeeded.append(self.course[i])
                del (self.course[i])
                i -= 1
            i += 1
        #get the courses to be selected
        waiting_list = [x for x in R_list if '课余量' in x]
        waiting_list = [re.findall('课程(.*?)课余量', x)[0] for x in waiting_list]
        #return_list[1] is the warnings
        return_list = [','.join(waiting_list), [x for x in R_list if '课余量' not in x]]
        if self.type == 'rx':
            self.post_data['p_rx_id'] = self.course
        elif self.type == 'bx':
            pass
        return return_list

    def Xuanke_once(self):
        self.turn += 1
        token = self.getToken(self.token_pattern)
        if 'Error' in token:
            Msg = '第' + str(self.turn) + '次失败,' + token
            print(Msg)
            return False
        else:
            self.post_data['token'] = token
            result = self.session.post(self.post_url, data=self.post_data)
            print('第' + str(self.turn) + '次')
            R_info = re.findall(self.Msg_pattern, result.text)
            if len(R_info) == 0:
                print(result.text)
            else:
                info = self.Process(R_info[0], self.post_data)
                print('Waiting List: ' + info[0])
                print('\n'.join(info[1]))
                if len(self.Succeeded) > 0:
                    print('Selected：' + ','.join(self.Succeeded))
                sleep(2)
            return True

    def end(self):
        if len(self.Succeeded) >= 0:
            print('Selected: ' + ','.join(self.Succeeded))
        input('End, press any key to quit...')
    #Main selecting phase

    def Xuanke(self):
        if not self.Login(Needname=True):
            self.end()
            return
        self.getCourse()
        while len(self.course) > 0:
            #Error happened
            if not self.Xuanke_once():
                Is_Continue = input('Continue?(y/n):')
                if Is_Continue == 'n':
                    break
                #Log in again
                if not self.Login(Needname=False):
                    break
        self.end()
        return