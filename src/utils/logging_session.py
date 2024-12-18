"""
This module defines a custom session class for logging request and response details
using the requests library.

NOTE:
要捕获API调用的原始URL、参数及返回内容，我们通常需要直接在发起网络请求的地方进行拦截，而不是仅仅依赖于函数的输入输出。
如果你正在使用的框架或库支持请求拦截器（如requests库中的session对象或者使用HTTP客户端库如httpx等），那么可以直接在这些地方设置拦截逻辑。
然而，由于直接访问网络请求的细节超出了纯Python装饰器的能力范围（装饰器只能访问到它所装饰的函数的信息），我们需要一个更具体的上下文来实现这一需求。
但我们可以设计一个更加通用的“代理”模式或利用现有的库功能来间接达到目的。
如果你使用的是requests库，可以通过自定义Session并在其中添加一个请求和响应的钩子（hooks）来实现。以下是一个例子。
这个例子中，我们创建了一个继承自requests.Session的LoggingSession类，并在其中添加了对请求前后的处理逻辑。
每次通过这个LoggingSession实例发出请求时，都会自动记录请求的URL、参数以及响应的详细信息。
请注意，实际应用中你可能需要根据自己的需求调整日志记录的方式，比如将信息写入文件或使用更复杂的日志库。
此外，上述代码仅适用于基于requests库的HTTP请求，如果你使用的是其他库（如httpx、aiohttp等），则需要查阅相应库的文档来了解如何设置请求和响应的拦截逻辑。
"""

import logging

import requests
from requests.models import Request

from src.config.logging_config import setup_logging

setup_logging()


def is_binary_content(response):
    """Check if the content is binary based on response headers."""
    content_type = response.headers.get('Content-Type', '')
    return 'image' in content_type or 'application' in content_type


class LoggingSession(requests.Session):
    """A custom session class for logging request and response details."""

    def __init__(self):
        """Initialize the session and set up logging hooks."""
        super().__init__()
        # requests only has this hooks
        self.hooks['response'].append(self.log_response)
        self.logger = logging.getLogger(self.__class__.__name__)

    def log_request(self, request):
        """Log request details before sending."""
        self.logger.info("Calling URL: %s", request.url)
        if isinstance(request, Request):
            self.logger.info("Parameters: %s", request.params)

    def log_response(self, response):
        """Log response details after receiving."""
        self.logger.info("Response Status: %s", response.status_code)
        if is_binary_content(response):
            return
        try:
            self.logger.debug("Response Content: %s", response.json())
        except ValueError as exc:
            self.logger.info("Non-JSON Response Content: %s", response.text)
            self.logger.error("Error parsing JSON: %s", exc)

    def send(self, request, **kwargs):
        """Override the send method to add logging."""
        self.log_request(request)
        return super().send(request, **kwargs)


if __name__ == "__main__":
    # Use the custom session to make a request
    session = LoggingSession()
    rsp = session.get('https://randomuser.me/api', params={'results': '1'})
    # This will automatically log the request URL, parameters, and response status and content
