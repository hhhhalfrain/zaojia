import re
import collections

keyword_type_dict = {
    "chang": ['长', '长度', 'L'],
    "kuan": ['宽', '宽度', 'W'],
    "gao": ["高", "高度", "H"],
}


class type:
    def __init__(self):
        self._chang = None
        self._kuan = None
        self._gao = None
        self.banzhouchang = None  # 半周长
        self.zhouchang = None

    @property
    def chang(self):
        return self._chang

    @chang.setter
    def chang(self, chang):
        self._chang = chang
        if bool(self._chang) and bool(self._kuan):
            self.banzhouchang = self._chang + self._kuan
            self.zhouchang = (self._chang + self._kuan) * 2

    @property
    def kuan(self):
        return self._kuan

    @kuan.setter
    def kuan(self, kuan):
        self._kuan = kuan
        if bool(self._chang) and bool(self._kuan):
            self.banzhouchang = self._chang + self._kuan
            self.zhouchang = (self._chang + self._kuan) * 2

    @property
    def gao(self):
        return self._gao

    @gao.setter
    def gao(self, gao):
        self._gao = gao


    def input_data(obj, type, value):
        for key in keyword_type_dict:
            if type in keyword_type_dict[key]:
                setattr(obj, key, value)
                return True  # 如果匹配到了，则返回True
        return False


def match(str):
    TYPE = type()
    num_list = re.findall(r'\d+', str)
    match_list=[]
    for keyword in keyword_type_dict:
        match_list+=keyword_type_dict[keyword]
    # 按字符串长度排序
    match_list.sort(key=lambda x: len(x),reverse=True)

    re_str = '|'.join(match_list)
    kind_list = re.findall(re_str, str)
    unit_dict = {
        'mm': 1,
        'cm': 10,
        'dm': 100,
        'm': 1000,
        'km': 1000000,
        '毫米': 1,
        '厘米': 10,
        '分米': 100,
        '米': 1000,
        '千米': 1000000,
    }
    order_unit_dict = collections.OrderedDict(sorted(unit_dict.items(), key=lambda s: s[0]))
    multiple = 1
    for unit in order_unit_dict:
        if str.find(unit) > 0:
            multiple = multiple * order_unit_dict[unit]
            break
    new_num_list = []
    for num in num_list:
        new_num_list.append(eval(num) * multiple)
    data = dict(zip(kind_list, new_num_list))
    for key in data:
        TYPE.input_data(key, data[key])
    return TYPE


if __name__ == '__main__':
    s = match('长*宽*高=1*2*1(米)')
    print(s.chang)
    print(s.kuan)
    print(s.gao)
