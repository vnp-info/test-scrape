import asyncio
import random,re,requests,json
from utils.file import save_to_csv
from collections import namedtuple
from dataclasses import dataclass

def fetch():
    try:
        ans = []
        for i in range(10**4):
            print(i)
            pad = 6 - len(str(i))
            code = "0" * pad + str(i)
        
            url = f'https://api.zipcodestack.com/v1/search'
            params = {
                'codes' : code,
                'apikey': "01HKYH4E0NV3VBP25W5HG04ZD0"
            }

            data = requests.get(url=url,params=params)
            ans.append(data.json())

        with open("pincode_1.json","w") as f:
            json.dump(ans,f,indent=4)
    except Exception as e:
        print(e)


fetch()





# obj.name = 'asdf'

# # sem = asyncio.Semaphore()

# class Test():
#     def __init__(self) -> None:
#         self.sem = asyncio.Semaphore()
#         self.cnt = 0

#     async def get(self):
#         await asyncio.sleep(random.random())
#         return self.cnt
    
#     async def save(self,val):
#         await asyncio.sleep(random.random())
#         self.cnt = val
    
#     async def add(self,val,idx):
#         await asyncio.sleep(random.random())
#         async with self.sem:
#             new_cnt = (await self.get()) + val
#             await self.save(new_cnt)
#         print(idx)

# async def main():
#     obj = Test()

#     tasks = [asyncio.create_task(obj.add(10,i)) for i in range(100)]

#     await asyncio.gather(*tasks)

#     print('done',await obj.get())

# asyncio.run(main())