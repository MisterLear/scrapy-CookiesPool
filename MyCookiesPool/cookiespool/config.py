# Mongo Database Config
MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB = 'qichacha'
# Item Storage DBConfig
COOKIES_TABLE = 'cookies'


"""
########### SeleniumConfig START ###########
"""
SELENIUM_TIMEOUT = 20           # selenium浏览器的超时时间，单位秒
LOAD_IMAGE = True               # 是否下载图片
WINDOW_HEIGHT = 900             # 浏览器窗口大小
WINDOW_WIDTH = 900
EXECUTABLE_PATH = "/usr/local/share/"
HEADLESS = False

TEST_URL = 'https://www.qichacha.com'
LOGIN_URL = 'https://www.qichacha.com/user_login?back=%2F'

# 产生器类，如扩展其他站点，请在此配置
GENERATOR_MAP = {
    'qichacha': 'QichachaCookiesGenerator'
}

# 测试类，如扩展其他站点，请在此配置
TESTER_MAP = {
    'qichacha': 'QichachaValidityTester'
}

# 产生器和验证器循环周期
CYCLE = 20

# 产生器开关，模拟登录添加Cookies
GENERATOR_PROCESS = True
# 验证器开关，循环检测数据库中Cookies是否可用，不可用删除
VALID_PROCESS = True
