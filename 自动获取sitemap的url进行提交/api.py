import requests
import xml.etree.ElementTree as ET
import time
from datetime import datetime
from urllib.parse import urlparse

# 参数配置
SITEMAP_URL = 'https://darklotus.cn/sitemap.xml'  # 要获取的 sitemap URL
BAIDU_API_URL = 'http://data.zz.baidu.com/urls?site=https://darklotus.cn&token=DzWQIBW7fXILKWYN'  # 百度收录 API 地址
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
MAX_SUBMISSIONS_PER_DAY = 10  # 每天最大提交条数

# 从 sitemap.xml 获取最新的 URL
def get_latest_urls_from_sitemap(sitemap_url, limit=10):
    """
    从指定的 sitemap URL 获取最新的 URL
    """
    try:
        response = requests.get(sitemap_url, headers=HEADERS)  # 发送 GET 请求
        response.raise_for_status()  # 检查请求是否成功
        urls = []
        root = ET.fromstring(response.content)  # 解析 XML 内容
        # 查找所有 loc 标签
        for loc in root.findall('.//{*}loc'):
            urls.append(loc.text)  # 将 URL 添加到列表中
            if len(urls) >= limit:  # 获取到指定数量的 URL 后退出
                break
        return urls
    except Exception as e:
        print(f"从 sitemap 获取 URL 时出错: {e}")
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
def log_submission(url, response):
    """
    记录成功提交的 URL 和响应状态到日志文件
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 获取当前时间
    status_message = "提交成功" if response and response.get('success') == 1 else "提交失败"  # 根据状态设置消息
    
    # 从 SITEMAP_URL 提取域名部分
    domain = urlparse(SITEMAP_URL).netloc.split('.')[0]  
    subdomain = urlparse(SITEMAP_URL).netloc  # 完整域名
    log_filename = f"{subdomain}_log.txt"  # 生成日志文件名

    with open(log_filename, 'a', encoding='utf-8') as log:  # 以追加模式打开日志文件
        log_entry = f"{timestamp} {url} 状态: {status_message}\n"  # 格式化日志条目
        log.write(log_entry)  # 写入日志文件

# 主程序
def main():
    """
    主程序，执行获取 URL 和逐条提交 URL 的过程
    """
    urls = get_latest_urls_from_sitemap(SITEMAP_URL)  # 获取 URL 列表
    submitted_count = 0  # 记录已提交的 URL 数量

    if urls:
        print("成功获取到 URL:", urls)  # 打印获取到的 URL
        for url in urls:  # 逐条提交 URL
            if submitted_count >= MAX_SUBMISSIONS_PER_DAY:  # 检查是否达到每天最大提交条数
                print("已达到每天最大提交条数，停止提交。")
                break
            response = submit_url_to_baidu(url)  # 提交 URL 到百度收录 API
            log_submission(url, response)  # 记录日志
            submitted_count += 1  # 增加已提交计数
            time.sleep(2)  # 等待 2 秒后再提交下一个 URL
    else:
        print("未找到任何 URL，无法提交。")

if __name__ == '__main__':
    main()