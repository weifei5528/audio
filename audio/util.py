import re


class Util(object):
    @staticmethod
    def replace_special_str(str):
        str = re.sub('[\t\n\:\：\?]', '', str)
        return str

