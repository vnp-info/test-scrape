import asyncio
import random
from utils.file import save_to_csv

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

save_to_csv('test.json')