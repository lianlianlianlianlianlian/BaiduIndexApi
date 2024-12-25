import requests
import time
from datetime import datetime
from urllib.parse import urlparse

# 参数配置
BAIDU_API_URL = 'http://data.zz.baidu.com/urls?site=https://blog.darklotus.cn&token=DzWQIBW7fXILKWYN'  # 百度收录 API 地址
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
# 多行字符串方式定义 URL
URLS = """
https://blog.darklotus.cn/tutorials/cloudflarewafconfig.html
https://blog.darklotus.cn/tutorials/npmjiasu.html
https://blog.darklotus.cn/notes/nasallinone.html
https://blog.darklotus.cn/tutorials/syncapplepasswordschromeedge.html
https://blog.darklotus.cn/tutorials/importbrowserpasswordstoicloud.html
https://blog.darklotus.cn/notes/heike666666.html
https://blog.darklotus.cn/notes/macsip.html
https://blog.darklotus.cn/tutorials/typechofwrite.html
https://blog.darklotus.cn/tutorials/blogbackup.html
https://blog.darklotus.cn/tutorials/e5cpumacos.html
""".strip().splitlines()  # 按换行符拆分成列表

# 提交 URL 到百度收录 API
def submit_url_to_baidu(url):
    if not url:
        print("没有要提交的 URL。")
        return None

    try:
        headers = {
            'Content-Type': 'text/plain; charset=UTF-8',
        }
        response = requests.post(BAIDU_API_URL, data=url.encode('utf-8'), headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"提交 URL {url} 时出错: {e}")
        print(f"响应状态码: {e.response.status_code}")
        print(f"响应内容: {e.response.text}")
    except Exception as e:
        print(f"提交 URL {url} 时发生其他错误: {e}")
    return None

# 记录日志
def log_submission(url, response, domain):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status_message = "提交成功" if response and response.get('success') == 1 else "提交失败"
    log_entry = f"{timestamp} {url} 状态: {status_message}"
    print(log_entry)

# 从 URL 中提取域名
def extract_domain(api_url):
    parsed_url = urlparse(api_url)
    domain = parsed_url.query.split('=')[1].split('/')[2]
    return domain

# 主程序
def main():
    domain = extract_domain(BAIDU_API_URL)
    
    if URLS:
        print("成功获取到 URL:", URLS)
        for url in URLS:
            response = submit_url_to_baidu(url)
            log_submission(url, response, domain)
            time.sleep(2)
    else:
        print("未找到任何 URL，无法提交。")

if __name__ == '__main__':
    main()
