import functools
import json
import logging

from src.config.logging_config import setup_logging

setup_logging()


def log_api_call(func):
    """
    装饰器，用于自动记录API调用的日志信息。
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 获取函数名作为API名称
        api_name = func.__name__

        default_logger = logging.getLogger('log_api_call_default')
        logger = getattr(args[0], 'logger', default_logger) if args else default_logger
        # logger.info(f"Calling {func.__name__} with args: {args}, kwargs: {kwargs}")

        # 打印调用的API名称和参数
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        # TODO 这里不好，打印的是函数的入参
        logger.info(f"Calling API: {api_name}({signature})")

        # 调用原始函数
        result = func(*args, **kwargs)

        # 尝试格式化输出返回值，对于非基本类型使用json.dumps简化输出
        try:
            logger.info(f"Returned: {json.dumps(result, indent=None, ensure_ascii=False)}")
        except TypeError:  # 如果result不是json serializable
            logger.info(f"Returned: {result}")

        return result

    return wrapper


if __name__ == "__main__":
    # 使用装饰器的示例函数
    @log_api_call
    def get_user_profile(user_id):
        """
        假设这是一个获取用户资料的API调用。
        """
        # 这里是模拟的API调用逻辑
        profile = {
            "user_id": user_id,
            "username": "example_user",
            "email": "user@example.com"
        }
        return profile


    # 调用示例函数
    get_user_profile(123)
