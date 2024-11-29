
# 百度 URL 提交脚本

此 Python 脚本通过百度 API 自动提交一组 URL，帮助您快速实现 URL 的 SEO 收录。

同时制作了全自动读取sitemap的版本，但百度每天一个域名只能api提交十个url，实际体验并不好

所以我单独制作了自定义URL的版本，因为sitemap获取的url提交 会把一些不重要的tag 页数 也提交上去，收录这些没有意义。

设置好参数后可以用Github的Actions直接提交

暂时不知道暴露token会不会被恶搞破坏，如果会大家把仓库设为私库在用actions或者用自己的服务器计划任务提交就行了。

## 功能
- 将预定义的 URL 列表提交到百度的 SEO 平台进行收录。
- 日志记录每个提交的结果，显示成功或失败状态。
- 包含 HTTP 及其他异常的错误处理，并提供详细的日志信息。
- 从百度 API URL 中提取域名，用于日志记录。

## 环境要求
- Python 3.x
- `requests` 库

安装所需的库：
```bash
pip install requests
```

## 配置
1. **百度 API URL**：修改 `BAIDU_API_URL` 变量以使用您的百度 API 地址和 token。
2. **URL 列表**：在 `URLS` 变量中添加或修改您想提交的 URL 列表。

## 使用方法
脚本都是打好注释的，改成自己的即可。
运行脚本：
```bash
python index.py
```

脚本将执行以下操作：
- 将 `URLS` 列表中的每个 URL 提交到百度 API。
- 为每次提交记录日志，包括时间戳、URL 和提交状态（成功或失败）。

## 脚本说明

### 参数
- **BAIDU_API_URL**：百度 API 端点，包含您的唯一 token。
- **HEADERS**：自定义的请求头（包含 user-agent 信息）。
- **URLS**：包含待提交 URL 的多行字符串，通过换行符分割成列表。

### 函数
- `submit_url_to_baidu(url)`: 将单个 URL 提交到百度 API。
- `log_submission(url, response, domain)`: 记录每次 URL 提交的结果。
- `extract_domain(api_url)`: 从百度 API URL 中提取域名。
- `main()`: 控制 URL 提交流程的主函数。

## 输出示例
脚本会记录每次提交的成功或失败状态：
```
2024-11-12 14:32:01 https://darklotus.cn/ 状态: 提交成功
2024-11-12 14:32:03 https://darklotus.cn/docs 状态: 提交失败
...
```

## 常见问题
- 请确保 `BAIDU_API_URL` 中的 token 正确。
- 检查百度 API 文档，了解速率限制和配额限制。
- 如果出现 `requests.exceptions.HTTPError` 或其他异常，它们会记录在控制台输出中。

## 许可
该项目遵循 MIT 许可协议。
