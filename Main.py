import requests, re, time
from PIL import Image
from Helper import Helper

login_data = {
    'j_username': '1',
    'j_password': '1',
    'captchaflag': 'login1',
    '_login_image_': '1'
}

Cookie_Dict = {
	'JSESSIONID':'',
	'thuwebcookie':''
}

data_bx = {
	'm':'saveBxKc',
	'p_xnxq':'2017-2018-1',
	'tokenPriFlag':'bx',
	'page':'',
	'p_kch':'',
	'p_kcm':''
	}

data_rx = {
    'm': 'saveRxKc', 'page': '',
    'p_sort.p1': '',
    'p_sort.p2': '',
    'p_sort.asc1': 'true',
    'p_sort.asc2': 'true',
    'is_zyrxk': '',
    'tokenPriFlag': 'rx',
    'p_kch': '',
    'p_kcm': '',
    'p_kkdwnm': '',
    'p_kctsm': '05',
    'p_rxklxm': '',
    'p_xnxq': '2017-2018-1',
    'goPageNumber': '1',
    }

val_url = 'http://zhjwxk.cic.tsinghua.edu.cn/login-jcaptcah.jpg?captchaflag=login1'
login_url = 'https://zhjwxk.cic.tsinghua.edu.cn/j_acegi_formlogin_xsxk.do'
token_url = 'http://zhjwxk.cic.tsinghua.edu.cn/xkBks.vxkBksXkbBs.do?m=bxSearch&p_xnxq=2017-2018-1&tokenPriFlag=bx'
post_url = 'http://zhjwxk.cic.tsinghua.edu.cn/xkBks.vxkBksXkbBs.do'
main_url = 'http://zhjwxk.cic.tsinghua.edu.cn/xkBks.vxkBksXkbBs.do?m=main'
Msg_pattern = 'showMsg\("(.*?)"\)'
token_pattern = 'name="token" value="(.*?)"'

def main():
    classHelper = Helper(val_url, login_url, token_url, post_url, main_url, login_data, data_rx, \
                     token_pattern, Msg_pattern, 'rx')
    classHelper.Xuanke()

if __name__ == '__main__':
    main()

