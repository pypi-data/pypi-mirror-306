__all__ = ["RuntimeException", "GLOBAL_DEBUG"]
__auth__ = "baozilaji@gmail.com"


GLOBAL_DEBUG = False


class RuntimeException(Exception):
    """
      全局运行时异常
    """
    def __init__(self, name: str, msg: str):
        self.name = name
        self.msg = msg
