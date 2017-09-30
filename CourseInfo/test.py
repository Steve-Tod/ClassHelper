from Helper import Helper
import re, json

login_data = {
    'j_username': '1',
    'j_password': '1',
    'captchaflag': 'login1',
    '_login_image_': '1'
}
search_data = {
    'm': 'kkxxSearch',
    'page': '1',
    'p_sort.asc1': 'true',
    'p_sort.asc2': 'true',
    'p_xnxq': '2017-2018-1',
    'pathContent': '%D2%BB%BC%B6%BF%CE%BF%AA%BF%CE%D0%C5%CF%A2',
    'goPageNumber': '1',
    'token': 'a'
}

Tag = {}

val_url = 'http://zhjwxk.cic.tsinghua.edu.cn/login-jcaptcah.jpg?captchaflag=login1'
login_url = 'https://zhjwxk.cic.tsinghua.edu.cn/j_acegi_formlogin_xsxk.do'
main_url = 'http://zhjwxk.cic.tsinghua.edu.cn/xkBks.vxkBksXkbBs.do?m=main'
post_url = 'http://zhjwxk.cic.tsinghua.edu.cn/xkBks.vxkBksJxjhBs.do'
token_url = 'http://zhjwxk.cic.tsinghua.edu.cn/xkBks.vxkBksJxjhBs.do?m=kkxxSearch&p_xnxq=\
2017-2018-1&pathContent=%D2%BB%BC%B6%BF%CE%BF%AA%BF%CE%D0%C5%CF%A2'
p_key = '<div align="center"><span>(.*?)</span>'
p_val = '<span class="trunk">(.*?)</span>'
page_pattern = '共 (.*?) 页'

#process one page
def Process(result):
    #get numbers
    ctags = re.findall(p_key, result)
    i = 0
    ctags1 = []
    while i < len(ctags):
        ctags1.append(' '.join(ctags[i: i + 2]))
        i += 3
    #get name and time
    tags = re.findall(p_val, result)
    Index0 = tags.index('本科文化素质课组') + 1
    tags1 = tags[Index0:]
    while '实验信息' in tags1:
        tags1.remove('实验信息')
    i = 0
    tags2 = []
    while i < len(tags1):
        temp = tags1[i:i + 7]
        tags2.append(temp)
        i += 7
    i = 0
    while i < len(tags2):
        Tag[ctags1[i]] = tags2[i]
        i += 1


H = Helper(val_url, login_url, main_url, login_data)

H.Login()

#get page number
result = H.session.get(token_url)
page = int(re.findall(page_pattern, result.text)[0])
print('There are ' + str(page) + ' pages')
for p in range(page):
    search_data['page'] = str(p + 1)
    return_page = H.session.post(post_url, search_data)
    print('Processing page ' + re.findall('第(.*?)页', return_page.text)[0])
    Process(return_page.text)

f = open('info.txt', 'w')
f.write(json.dumps(Tag))
f.close()