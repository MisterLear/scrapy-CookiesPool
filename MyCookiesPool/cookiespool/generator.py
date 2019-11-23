import time
import numpy as np
import scipy.interpolate as si
import platform
import json
import random
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from cookiespool.config import SELENIUM_TIMEOUT, EXECUTABLE_PATH, HEADLESS, LOGIN_URL, COOKIES_TABLE
from cookiespool.db import MongoDBConfig



class QichachaCookiesGenerator():
    def __init__(self):
        self.timeout = SELENIUM_TIMEOUT
        self.url = LOGIN_URL
        self.executable_path = EXECUTABLE_PATH
        chrome_options = webdriver.ChromeOptions()
        if HEADLESS:
            chrome_options.add_argument('--headless')
        # 去除 --ignore
        chrome_options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # chrome_options.add_argument('--disable-gpu')
        if platform.system() == 'Windows':
            self.browser = webdriver.Chrome(executable_path=self.executable_path, chrome_options=chrome_options)
        else:
            chrome_options.add_argument('no-sandbox')  # 针对linux root用户
            self.browser = webdriver.Chrome(chrome_options=chrome_options)

        self.browser.maximize_window()
        self.browser.set_page_load_timeout(self.timeout)
        self.browser.implicitly_wait(self.timeout)
        self.wait = WebDriverWait(self.browser, self.timeout, poll_frequency=0.5)
        self.conn = MongoDBConfig(COOKIES_TABLE)

    def close_spider(self):
        self.browser.quit()

    def spoof_match_track(self, distance):
        '''
        模拟滑动快慢轨迹
        :param distance: 需要移动的距离
        :return: 移动轨迹track[0.2,]
        '''
        track = []  # 移动轨迹
        current = 0  # 当前位置
        mid = distance * 4 / 5  # #减速阀值 4/5加速. 1/5加速
        t = 0.2  # 计算间隔
        v = 30  # 速度v

        while current < distance:
            if current < mid:
                # 加速度
                a = 2
            else:
                a = -3
            v_0 = v
            v = v_0 + a * t  # 当前速度 = 初速度+加速*加速时间
            move = v_0 * t + 0.5 * a * t**2  # 移动距离
            current += move  # 当前移动距离
            track.append(round(move))  # 加入轨迹:浮点型
        return track

    def slide_and_match(self, slider, distance):
        '''
        :param slider: 滑块
        :param distance: 需要移动的距离
        :return:
        '''
        action = ActionChains(self.browser)  # 实例化一个action对象
        action.click_and_hold(slider).perform()  # 鼠标左键按下不放
        track = self.spoof_match_track(distance)  # 模拟滑动快慢轨迹
        for x in track:
            action.move_by_offset(xoffset=x, yoffset=0).perform()
            action.reset_actions()
        action.release().perform() # 释放鼠标
        time.sleep(0.5)

    def spoof_track(self, distance):
        '''
        模拟滑动快慢轨迹
        :param distance: 需要移动的距离
        :return: 移动轨迹track[0.2,]
        '''

        # Curve base:
        points_list = [[[0, 0], [distance / 2 , 0], [distance * 3 / 4, 2], [distance, 3], [distance, 0]],
                       [[0, 0], [distance / 2 , 0], [distance, 3], [distance, 0]],
                       [[0, 0], [distance, 3], [distance, 0]],
                       [[0, 0], [distance / 2 , 0], [distance * 3 / 4, 2], [distance, 0]]]
        points = random.choice(points_list)
        points = np.array(points)

        x = points[:, 0]
        y = points[:, 1]
        m = len(points)
        t = range(len(points))
        ipl_t = np.linspace(0.0, len(points) - 1, 100)

        x_tup = si.splrep(t, x, k=m-1)
        y_tup = si.splrep(t, y, k=m-1)

        x_list = list(x_tup)
        xl = x.tolist()
        x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

        y_list = list(y_tup)
        yl = y.tolist()
        y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

        x_i = si.splev(ipl_t, x_list)  # x interpolate values
        y_i = si.splev(ipl_t, y_list)  # y interpolate values
        return zip(x_i, y_i)

    def slide(self, slider, distance):
        action = ActionChains(self.browser)  # 实例化一个action对象
        action.move_to_element(slider).perform() # 鼠标移动到滑块上
        action.click_and_hold(slider).perform()  # 鼠标左键按下不放
        track = self.spoof_track(distance)  # 模拟滑动快慢轨迹
        try:
            for x, y in track:
                action.move_by_offset(xoffset=x, yoffset=y).perform()
                action = ActionChains(self.browser)
        except:
            time.sleep(0.5)


    def dump_cookies(self, username):
        """
        登录完成后,将cookies保存到本地文件
        """
        dictCookies = self.browser.get_cookies()
        self.conn.update({"_id": username},
                         {'$set': {'cookies': dictCookies}}, upsert=True)
        self.close_spider()


    def login(self, username, password):
        self.browser.get(self.url)
        self.wait.until(EC.presence_of_element_located((By.ID, 'normalLogin')))
        # 转到密码登录的js界面
        self.browser.find_element_by_id('normalLogin').click()

        self.wait.until(EC.presence_of_element_located((By.ID, 'nameNormal')))
        self.browser.find_element_by_id('nameNormal').click()  # 点击输入文本的输入框
        self.browser.find_element_by_id('nameNormal').send_keys(username)  # 账号
        self.browser.find_element_by_id('pwdNormal').click() # 点击输入文本的输入框
        self.browser.find_element_by_id('pwdNormal').send_keys(password)  # 密码
        self.slide_bar(username, password)

    def slide_bar(self, username, password):
        locator = (By.ID, 'nc_1_n1z')
        slider_button = self.wait.until(EC.presence_of_element_located(locator)) # 找到滑动板块的按钮
        self.slide(slider_button, 380)

        # alert 是 企查查 登录出现问题时弹出的
        alert = self.browser.find_element_by_xpath('//*[@id="dom_id_one"]/div').text
        if "点击刷新" in alert:
            # 点击刷新直到出现滑块才停止
            self.browser.find_element_by_xpath('//*[@id="dom_id_one"]/div/span/a').click()
            return self.slide_bar(username, password)

        else:
            self.browser.find_element_by_xpath('//*[@id="user_login_normal"]/button').click()  # 点击登录
            time.sleep(5)
            self.dump_cookies(username)

    def get_cookies(self):
        document = self.conn.find({})
        # document = self.conn.find({"cookies": None})
        if len(document) == 0:
            print("请先录入一些用户名和密码：")
            exit()
        else:
            for each in document:
                username = each.get("_id")
                password = each.get("password")
                self.login(username, password)
