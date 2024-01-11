import re
from abc import ABC, abstractmethod

class Extractor(ABC):

    @abstractmethod
    def extract(text):
        pass

    @abstractmethod
    def get_field():
        pass

class PhoneExtractor(Extractor):

    def __init__(self):
        self.field = 'phone'
        self.us_phone_regex = re.compile(r'(\(\d{3}\))( )?(\d{3})(-)(\d{4})')
        # self.phone_regexes = [
        #     re.compile("[+ -]?(\()?\d{2}(\))?.(\d{4}).(\d{4})", flags=re.I+re.M),
        #     re.compile("[+ -]?\(\d{2}\).(\d{5}).(\d{4})", flags=re.I+re.M),
        #     re.compile("\d{4}.?\d{3}.?\d{3}", flags=re.I+re.M),
        #     re.compile("\d{3}.?\d{3}.?\d{4}", flags=re.I+re.M),
        #     re.compile(r'\(\d{3}\).?(\d{3}).?(\d{4})'),
        #     re.compile(r"[+ -]?(\()?\d{3}(\))?.?(\d{2}).?(\d{2}).?(\d{2})", flags=re.I+re.M),
        # ]

    def extract(self,text):
        arr = [''.join(t) for t in self.us_phone_regex.findall(text)]
        return list(set(arr))
        # arr = []
        # for r in self.phone_regexes:
        #     tmp = [''.join(t) for t in r.findall(text)]
        #     arr.extend(tmp)

        # return list(set(arr))
    
    def get_field(self):
        return self.field