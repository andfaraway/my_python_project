from enum import Enum, unique


@unique
class ErrorCode(Enum):

    CODE_200 = {200: '成功'}
    CODE_201 = {201: '失败'}
    CODE_300 = {300: '验证失败'}

    @property
    def code(self):
        return list(self.value.keys())[0]

    @property
    def msg(self):
        return list(self.value.values())[0]

    def format_msg(self, *args):
        return list(self.value.values())[0] + "".join(args)
