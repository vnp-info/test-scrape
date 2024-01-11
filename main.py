import time
import asyncio
from utils.scrapper import Scrapper
from utils.file import read_csv
from utils.extractor import PhoneExtractor

async def main():
    try:
        start_time = time.perf_counter()

        # domains = ['https://orchardstreetapparel.com/products/orchard-street-apparel-gift-card']

        domains = read_csv('data/good_websites.csv')

        extractors = [PhoneExtractor()]

        obj = Scrapper(domains,extractors)

        await obj.scrape()

        end_time = time.perf_counter()
        diff = end_time - start_time

        print(f'Execution Time: {diff:0.2f}s')

        print('Done')
    except Exception as e:
        print('main: ',e)

if __name__ == "__main__":
    asyncio.run(main())