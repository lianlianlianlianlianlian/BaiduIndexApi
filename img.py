import requests
import time
from datetime import datetime
from urllib.parse import urlparse

# 参数配置
BAIDU_API_URL = 'http://data.zz.baidu.com/urls?site=https://img.darklotus.cn&token=DzWQIBW7fXILKWYN'  # 百度收录 API 地址
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
MANUAL_URL_FILE = 'urls.txt'  # 本地 URL 文件名

# 从文件中读取手动提交的 URL
def read_manual_urls(filename):
    """
    从指定文件读取 URL
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]  # 读取每行并去除空白
        return urls
    except Exception as e:
        print(f"读取手动 URL 文件时出错: {e}")
        return []

# 提交 URL 到百度收录 API
def submit_url_to_baidu(url):
    """
    将指定的 URL 提交到百度收录 API
    """
    if not url:
        print("没有要提交的 URL。")
        return None  # 返回 None 表示没有进行提交

    try:
        headers = {
            'Content-Type': 'text/plain; charset=UTF-8',  # 确保内容类型为纯文本
        }
        response = requests.post(BAIDU_API_URL, data=url.encode('utf-8'), headers=headers)  # 发送 POST 请求
        response.raise_for_status()  # 检查请求是否成功
        return response.json()  # 返回响应的 JSON 数据
    except requests.exceptions.HTTPError as e:
        print(f"提交 URL {url} 时出错: {e}")
        print(f"响应状态码: {e.response.status_code}")
        print(f"响应内容: {e.response.text}")  # 打印响应内容以帮助排查问题
    except Exception as e:
        print(f"提交 URL {url} 时发生其他错误: {e}")
    return None  # 返回 None 表示提交失败

# 记录日志
def log_submission(url, response, domain):
    """
    记录成功提交的 URL 和响应状态到日志文件
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间
    status_message = "提交成功" if response.get('success') == 1 else "提交失败"  # 根据状态设置消息
    log_filename = f"{domain}_log.txt"  # 生成日志文件名
    with open(log_filename, 'a', encoding='utf-8') as log:  # 以追加模式打开日志文件
        log_entry = f"{timestamp} {url} 状态: {status_message}\n"  # 格式化日志条目
        log.write(log_entry)  # 写入日志文件

# 从 URL 中提取域名
def extract_domain(api_url):
    """
    从 API URL 中提取域名
    """
    # 从 site 参数中提取域名
    parsed_url = urlparse(api_url)  # 解析 URL
    domain = parsed_url.query.split('=')[1].split('/')[2]  # 提取 site 参数中的域名
    return domain  # 返回域名部分

# 主程序
def main():
    """
    主程序，执行读取 URL 和逐条提交 URL 的过程
    """
    urls = read_manual_urls(MANUAL_URL_FILE)  # 从文件获取 URL 列表
    domain = extract_domain(BAIDU_API_URL)  # 提取域名用于日志文件名
    
    if urls:
        print("成功获取到 URL:", urls)  # 打印获取到的 URL
        for url in urls:  # 逐条提交 URL
            response = submit_url_to_baidu(url)  # 提交 URL 到百度收录 API
            log_submission(url, response, domain)  # 记录日志
            time.sleep(2)  # 等待 2 秒后再提交下一个 URL
    else:
        print("未找到任何 URL，无法提交。")

if __name__ == '__main__':
    main()