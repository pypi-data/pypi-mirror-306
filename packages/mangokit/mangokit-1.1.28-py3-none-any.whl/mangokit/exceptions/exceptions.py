# -*- coding: utf-8 -*-
# @Project: 芒果测试平台
# @Description:
# @Time: 2023-07-16 15:17
# @Author : 毛鹏
class MangoKitError(Exception):

    def __init__(self, code: int, msg: str, value: tuple = None):
        if value:
            msg = msg.format(*value)
        self.code = code
        self.msg = msg


class ToolsError(MangoKitError):
    pass


class MysqlConnectionError(ToolsError):
    pass


class MysqlQueryError(ToolsError):
    pass


class CacheIsEmptyError(ToolsError):
    pass


class FileDoesNotEexistError(ToolsError):
    pass


class JsonPathError(ToolsError):
    pass


class ValueTypeError(ToolsError):
    pass


class SendMessageError(ToolsError):
    pass


class ReplaceElementLocatorError(ToolsError):
    pass
