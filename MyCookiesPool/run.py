from cookiespool.generator import QichachaCookiesGenerator


def generate_cookie():
    print('Cookies生成进程开始运行')
    generator = QichachaCookiesGenerator()
    generator.get_cookies()
    print('Cookies生成完成')

if __name__ == '__main__':
    generate_cookie()