import re, requests
from abc import ABC, abstractmethod
from dataclasses import dataclass

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
        self.us_phone_regex = [re.compile(r'(\(\d{3}\))( )?(\d{3})(-)(\d{4})',flags=re.I+re.M)]
        self.phone_regexes = [
            re.compile("[+ -]?(\()?\d{2}(\))?.(\d{4}).(\d{4})", flags=re.I+re.M),
            re.compile("[+ -]?\(\d{2}\).(\d{5}).(\d{4})", flags=re.I+re.M),
            re.compile("\d{4}.?\d{3}.?\d{3}", flags=re.I+re.M),
            re.compile("\d{3}.?\d{3}.?\d{4}", flags=re.I+re.M),
            re.compile(r'\(\d{3}\).?(\d{3}).?(\d{4})'),
            re.compile(r"[+ -]?(\()?\d{3}(\))?.?(\d{2}).?(\d{2}).?(\d{2})", flags=re.I+re.M),
        ]

    def extract(self,text):
        arr = []
        for reg in self.us_phone_regex:
            tmp = [t.group() for t in reg.finditer(text)]
            arr.extend(tmp)

        return list(set(arr))
    
    def get_field(self):
        return self.field
    
class AddressExtractor(Extractor):
    
    def __init__(self):
        self.field = 'address'
        self.regex = re.compile(r'\b\d{5}\b|\b(\d{3}([- ])?\d{3})\b',flags=re.I+re.M)
        self.CODE = 'code'
        self.IS_CORRECT = 'is_correct'
        self.POSITION = 'position'

    @dataclass
    class VerifiedPincode:
        code: str
        is_correct: bool
    

    def verify_pincodes(self,pincodes) -> list[bool]:
        try:
            codes = [p[self.CODE] for p in pincodes]
            url = f'https://api.zipcodestack.com/v1/search'
            params = {
                'codes' : ','.join(codes),
                'apikey': "01HKW7TYBNN4SWCYCKZ3NMRWN5"
            }

            data = requests.get(url=url,params=params)

            result = data.json()['results'].keys() if data.json()['results'] else []

            return [{self.CODE: p[self.CODE],self.POSITION: p[self.POSITION], self.IS_CORRECT:p[self.CODE] in result} for p in pincodes]
        
        except Exception as e:
            raise e
        
    def process_pincode(self,pincode: str) -> str:
        pincode = pincode.replace(' ','')
        pincode = pincode.replace('-','')
        return pincode
   
    def extract_pincodes(self,text):
        arr = [
            {
                self.CODE: self.process_pincode(t.group()),
                self.POSITION: t.end()
            } 
            for t in self.regex.finditer(text)
        ]
        return arr
    
    def process_address(self,address:str):
        tokens = address.split("\n")
        max_left = 3

        tmp = ' '.join(tokens[-max_left:])

        return re.sub(' +', ' ', tmp).strip()
    
    def extract_addresses(self,text:str,pincodes):
        left_offset = 100
        ans = []
        for p in pincodes:
            right = p[self.POSITION]
            left = max(0,right - left_offset)
            ans.append({
                self.CODE: p[self.CODE],
                'address': self.process_address(text[left:right + 1])
            })
        
        return ans
    
    def extract(self,text):
        pincodes = self.extract_pincodes(text)

        arr = self.verify_pincodes(pincodes)

        correct_pincodes = [
            {
                self.CODE: a[self.CODE],
                self.POSITION: a[self.POSITION]
            } for a in arr if a[self.IS_CORRECT]
        ]

        # print(correct_pincodes)
        # print('95134' in [c[self.CODE] for c in correct_pincodes])

        addresses = self.extract_addresses(text,correct_pincodes)

        # for a in addresses:
        #     print(a)

        return addresses
        
    
    def get_field(self):
        return self.field
    
