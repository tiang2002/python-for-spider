import requests
import json
import re
import time
from selenium import webdriver
import random
from datetime import datetime
from datetime import timedelta
import os


def get_res(url, cookies):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3875.400',
        'Cookie': cookies,
        'Referer': 'https://seat.lib.whu.edu.cn/',
        'Origin': 'https://seat.lib.whu.edu.cn'
    }
    print(url)
    i = 0
    while 1:

        try:
            i += 1
            time.sleep(1)
            res = requests.get(url, headers=headers, timeout=(21, 60))
        except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
            print(e)
            print('           ~~~try ' + str(i) + ' times again~~~            ')
            time.sleep(10 + i * 10)
        else:
            print('success')
            return res
    # return None


def get_res_post(url, cookies, payload):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3875.400',
        'Cookie': cookies,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'seat.lib.whu.edu.cn',
        'Referer': 'https://seat.lib.whu.edu.cn/self',
        'Origin': 'https://seat.lib.whu.edu.cn',

    }
    print(url)
    i = 0
    while 1:

        try:
            i += 1
            time.sleep(1)
            res = requests.post(url, data=payload, headers=headers, timeout=(21, 60))
        except (requests.exceptions.Timeout, requests.exceptions.RequestException) as e:
            print(e)
            print('           ~~~try ' + str(i) + ' times again~~~            ')
            time.sleep(10 + i * 10)
        else:
            print('success')
            return res
    # return None


def init_browser(path):
    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    option.add_experimental_option("excludeSwitches", ['enable-automation'])  # ?????????????????????
    # option.add_argument('--headless')
    option.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3875.400')
    option.add_experimental_option('useAutomationExtension', False)  # ?????????????????????????????????
    # option.add_argument('--disable-gpu')  # ????????????????????????
    option.add_argument('--start-maximized')  # ?????????
    option.add_argument("disable-cache")  # ????????????
    option.add_argument('disable-infobars')
    option.add_argument('log-level=3')  # INFO = 0 WARNING = 1 LOG_ERROR = 2 LOG_FATAL = 3 default is 0
    # ????????????????????????????????????
    option.add_argument('origin="https://pixivel.moe/"')

    # option.add_argument('Referer="https://pixivel.moe/user?id=2517274"')
    # option.add_argument("--no-referrers")

    # option.add_argument('--proxy-server={0}'.format(proxy.proxy))
    preferences = {
        "webrtc.ip_handling_policy": "disable_non_proxied_udp",
        "webrtc.multiple_routes_enabled": False,
        "webrtc.nonproxied_udp_enabled": False
    }
    option.add_experimental_option("prefs", preferences)  # ??????webrtc??????????????????ip
    # option.add_argument(f'--proxy-server=' + id)  # ????????????ip

    option.add_argument('--auto-open-devtools-for-tabs')

    # No_Image_loading = {"profile.managed_default_content_settings.images": 2}
    # option.add_experimental_option("prefs", No_Image_loading)  # ??????????????????
    if path != '':
        browser = webdriver.Chrome(options=option, executable_path=path)
    else:
        browser = webdriver.Chrome(options=option)
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => false
        })
      """
    })  # ??????webdriver??????
    return browser


file = 'path.txt'
if os.path.exists(file) is False:
    path = input('?????????chromedriver?????????(???????????????Path??????????????????)???')

    with open(file, 'w+') as f:
        f.write(path)
else:
    with open(file, 'r') as f:
        data = f.readlines()
    if len(data) < 1:
        path = input('?????????chromedriver?????????(???????????????Path??????????????????)???')

        with open(file, 'w+') as f:
            f.write(path)
    else:
        path = data[0].replace('\n', '').strip()
print('????????????????????????????????????????????????')
start_time = input('????????????????????????12-30???')
end_time = input('????????????????????????12-30???')
date = input('????????????????????????1.?????????2.?????????')
date_flag = date
building = input('??????????????????1.???????????????')
rooms = input('???????????????\n1.?????????????????????\n2.???????????????\n3.?????????????????????\n')
if rooms == '1':
    rooms = [6, 7, 8, 9, 10, 11]
elif rooms == '2':
    rooms = ['12']
elif rooms == '3':
    rooms = ['15']
else:
    print('input error!')
    exit(1)

try:

    start_time = time.strptime(start_time, '%H-%M')
    end_time = time.strptime(end_time, '%H-%M')

    start_time = start_time.tm_hour * 60 + start_time.tm_min
    end_time = end_time.tm_hour * 60 + end_time.tm_min
    now_time = time.localtime().tm_hour * 60 + time.localtime().tm_min

    if start_time > end_time:
        print('input error!')
        exit(1)

except:
    print('input error!')
    exit(1)

file_name = 'user_and_code.txt'
if os.path.exists(file_name) is False:
    user = input('????????????????????????????????????????????????')
    password = input('??????????????????(????????????????????????????????????????????????)')
    with open(file_name, 'w+') as file:
        file.write(user + '\n')
        file.write(password)
else:
    with open(file_name, 'r') as file:
        data = file.readlines()
    if len(data) < 2:
        user = input('????????????????????????????????????????????????')
        password = input('??????????????????(????????????????????????????????????????????????)')
        with open(file_name, 'w+') as file:
            file.write(user + '\n')
            file.write(password)
    else:
        user = data[0].replace('\n', '').strip()
        password = data[1].replace('\n', '').strip()

if date == '1':
    date = time.strftime('%Y-%m-%d', time.localtime())
elif date == '2':
    now = datetime.now()
    now_time = now.strftime('%m-%d')
    now_hour = datetime.strptime(str(now.hour) + '-' + str(now.minute), '%H-%M')
    target = datetime.strptime(str(now.year) + '-22-45', '%Y-%H-%M')
    less = target - now_hour
    while now_time < '22-45':
        now = datetime.now()
        now_time = now.strftime('%H-%M')
        less = target - now
        print('                                  \r', end='')
        print('????????????????????????' + str(less.seconds) + '???', end='')
        time.sleep(1)

    aDay = timedelta(days=1)
    now += aDay
    date = now.strftime('%Y-%m-%d')
else:
    print('??????????????????')
    exit(1)

browser = init_browser(path)
url = 'https://seat.lib.whu.edu.cn/'
browser.get(url)

browser.find_element_by_xpath(r'/html/body/div[4]/div[2]/div[2]/dl/input').click()
browser.find_element_by_xpath(r'//*[@id="username"]').send_keys(
    user)
browser.find_element_by_xpath(r'//*[@id="password"]').send_keys(
    password)
browser.find_element_by_xpath(r'//*[@id="casLoginForm"]/p[2]/button').click()
while browser.current_url != 'https://seat.lib.whu.edu.cn/':
    time.sleep(1)
cookies = browser.get_cookies()
cookies = cookies[0]['name'] + '=' + cookies[0]['value'] + '; ' + cookies[1]['name'] + '=' + cookies[1]['value']
print(cookies)
while 1:
    flag = 0
    for room in rooms:
        res = get_res(
            'https://seat.lib.whu.edu.cn/freeBook/ajaxSearch?onDate=' + date
            + '&building=' + str(building) + '&room=' + str(room) + '&hour=null&startMin=' + str(
                start_time) + '&endMin=' + str(
                end_time) + '&power=null&window=null',
            cookies)

        res = json.loads(res.text)

        # pprint(res)
        seat_id = res['seatStr']
        seat_free = re.findall('<li class="free"(.*?)li>', seatStr)
        seat_id = []
        for each in seat_free:
            if "??????" in each:
                pass
            else:
                temp = re.findall('id="seat_(.*?)"', each)[0]
                seat_id.append(temp)
        if len(seat_id) > 0:
            flag = 1
            break
        else:
            print('????????????????????????????????????????????????')
    if flag == 1:
        break

seat_id = random.choice(seat_id)

token_url = 'https://seat.lib.whu.edu.cn/self'
browser.get(token_url)
token = browser.find_element_by_xpath('//*[@id="SYNCHRONIZER_TOKEN"]').get_attribute('value')
print(token)
reserve_url = 'https://seat.lib.whu.edu.cn/selfRes'

if date_flag != '2':
    payload = {
        'SYNCHRONIZER_TOKEN': token,
        'SYNCHRONIZER_URI': '/self',
        'date': '',
        'seat': str(seat_id),
        'start': str(start_time),
        'end': str(end_time),
        'authid': '-1'
    }
else:
    payload = {
        'SYNCHRONIZER_TOKEN': token,
        'SYNCHRONIZER_URI': '/self',
        'date': date,
        'seat': str(seat_id),
        'start': str(start_time),
        'end': str(end_time),
        'authid': '-1'
    }
reservation = get_res_post(reserve_url, cookies, payload)
print(reservation)
print(reservation.text)
