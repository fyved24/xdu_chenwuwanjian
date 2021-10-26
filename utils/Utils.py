# -*- coding: utf-8 -*-
"""
@Time        : 2020/7/19 12:25
@Author      : NingWang
@Email       : yogehaoren@gmail.com
@File        : Utils.py
@Description : 
@Version     : 0.1-dev
"""
import requests
import pickle

DEFAULT_HEADER = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36 Edg/83.0.478.64",
    "X-Requested-With": "XMLHttpRequest",
}

UPLOAD_HEADER = {
    "Referer": "https://xxcapp.xidian.edu.cn/site/ncov/xisudailyup",
    "Origin": "https://xxcapp.xidian.edu.cn",
}

DEFAULT_UPLOAD_MESSAGE = {
    "geo_api_info": "{\"type\":\"complete\",\"position\":{\"Q\":23.322377387153,\"R\":113.54549072265701,\"lng\":113.545491,\"lat\":23.322377},\"location_type\":\"html5\",\"message\":\"Get geolocation success.Convert Success.Get address success.\",\"accuracy\":15,\"isConverted\":true,\"status\":1,\"addressComponent\":{\"citycode\":\"020\",\"adcode\":\"440112\",\"businessAreas\":[],\"neighborhoodType\":\"\",\"neighborhood\":\"\",\"building\":\"\",\"buildingType\":\"\",\"street\":\"峻岚街\",\"streetNumber\":\"7号\",\"country\":\"中国\",\"province\":\"广东省\",\"city\":\"广州市\",\"district\":\"黄埔区\",\"township\":\"九佛街道\"},\"formattedAddress\":\"广东省广州市黄埔区九佛街道开芯国际大酒店广州绿地城\",\"roads\":[],\"crosses\":[],\"pois\":[],\"info\":\"SUCCESS\"}",
    "area": "广东省 广州市 黄埔区",  # 地区
    "city": "广州市", # 城市
    "province": "广东省",  # 省份
    "address": "广东省广州市黄埔区九佛街道开芯国际大酒店广州绿地城",  # 实际地址
}

LOGIN_URL = "https://xxcapp.xidian.edu.cn/uc/wap/login/check"

UPLOAD_URL = "https://xxcapp.xidian.edu.cn/xisuncov/wap/open-report/save"

COOKIE_FILE_NAME = "cookie.txt"


def get_cookie_from_login(student_id: str, password: str):
    """
    登录获取cookie
    :param student_id: 学号
    :param password:  密码
    :param cookie_file_path cookies文件路径
    :return:
    """
    r = requests.post(LOGIN_URL, data={"username": student_id, "password": password}, headers=DEFAULT_HEADER)
    if r.status_code == 200:
        if r.json()['e'] == 0:
            print("登录成功")
            # with open(cookie_file_path, 'wb') as f:
            #     pickle.dump(r.cookies, f)

            return "ok", r.cookies

        else:
            print(r.json()['m'])
            return "登录失败, 请检查用户名或密码是否正确:%s" % r.json()['m'], ""



# def load_cookie_from_file(cookie_file_path: str):
#     """
#     从文件中加载cookie
#     :param cookie_file_path: 文件路径
#     :return:
#     """
#     with open(cookie_file_path, 'rb') as f:
#         return pickle.load(f)


def load_upload_message_file(file_path: str):
    """
    从文件中解析需要提交的信息
    :param file_path: 文件路径
    :return:
    """
    with open(file_path, "r", encoding='utf8') as f:
        text = f.read()
        upload_message = eval(text)
        for key, value in DEFAULT_UPLOAD_MESSAGE.items():
            if key not in upload_message:
                upload_message[key] = value
        return upload_message


def upload_ncov_message(cookie, upload_message):
    header = dict(DEFAULT_HEADER.items() | UPLOAD_HEADER.items())
    r = requests.post(UPLOAD_URL, upload_message, cookies=cookie, headers=header)
    if r.json()['e'] == 0:
        print("上报成功")
        return "ok"
    else:
        print("上报出现错误!")
        print("错误信息: ", r.json()['m'])
        return "上报出现错误!，错误信息:%s" % r.json()['m']


if __name__ == '__main__':
    pass
