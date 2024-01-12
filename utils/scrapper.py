import re,json
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from utils.extractor import Extractor

class Scrapper:

    def __init__(self,domains,extractors: list[Extractor] = [],dump_file = 'test.json'):
        self.domains = domains
        self.dump_file = dump_file
        if not Scrapper.check_extractors(extractors):
            raise TypeError('Invalid Extractors List')
        self.extractors = extractors
        self.stream = open(dump_file,'w')
        self.sem = asyncio.Semaphore()
        self.cnt = 0

    @staticmethod
    def get_url(domain):
        url_regex = re.compile(f'^http(s)?:\/\/.*$',re.IGNORECASE)
        return domain if url_regex.match(domain) else f'https://{domain}'
    
    @staticmethod
    def process_link(link,domain):
        if link is None: return domain
        return link if link.split("/")[0] else domain + link 
    
    @staticmethod
    def check_contact(txt):
        contact_regex = re.compile(f'(contact|about)([- ])?(us|company)?',re.IGNORECASE)
        return contact_regex.match(txt)
    
    @staticmethod
    def extract_contact_links(html,domain):
        soup = BeautifulSoup(html, 'html.parser')

        anchor_tags = soup.find_all('a')

        href_properties = [Scrapper.process_link(a.get('href'),domain) for a in anchor_tags if Scrapper.check_contact(a.text)]

        return list(set(href_properties))
    
    @staticmethod
    def extract_text(html):
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text(separator="\n",strip=True)
        return text
    
    @staticmethod
    def check_extractors(extractors):
        return all([isinstance(e,Extractor) for e in extractors])
    
    def add_extractor(self,extractor):
        if not isinstance(extractor,Extractor):
            raise TypeError('Invalid Extractor Type')
        self.extractors.append(extractor)
    
    def extract_fields(self,text):
        result = {}

        for e in self.extractors:
            if e.get_field() not in result.keys():
                result[e.get_field()] = []
            result[e.get_field()].extend(e.extract(text))

        return result
    
    async def fetch_fields(self,domain):
        result = {'error':''}

        result['url'] = self.get_url(domain)
    
        url = result['url']
        print(f'fetching level 2... {url}')

        page = await self.browser.new_page()

        try:
            try:
                await page.goto(url, wait_until='networkidle')
            except Exception as e:
                result['error'] = f'{e}'
        
            html_content = await page.content()
            text_content = self.extract_text(html_content)
            field_results = self.extract_fields(text_content)

            result = {**result,**field_results}
                
        except Exception as e:
            result['error'] = f'{e}'
        finally:
            await page.close()

        return result

    async def scrape_util(self,domain):
        result = {'errors': []}

        result['home_url'] = self.get_url(domain)
  
        url = result['home_url']
        print(f'fetching level 1... {url}')

        page = await self.browser.new_page()

        try:
            try:
                await page.goto(url, wait_until='networkidle')
            except Exception as e:
                result['errors'].append({
                    'url': url,
                    'message' : f'{e}'
                })
        
            html_content = await page.content()
            text_content = self.extract_text(html_content)
            field_results = self.extract_fields(text_content)

            result = {**result,**field_results}

        
            contact_links = self.extract_contact_links(html_content,url)

            result['contact_links'] = contact_links

            max_page_limit = min(len(contact_links),5)

            routines = [asyncio.create_task(self.fetch_fields(contact_links[i])) for i in range(max_page_limit)]

            sub_results = await asyncio.gather(*routines)

            for res in sub_results:
                for e in self.extractors:
                    if e.get_field() not in result.keys():
                        result[e.get_field()] = []
                    result[e.get_field()].extend(res[e.get_field()])
                    # result[e.get_field()] = list(set(result[e.get_field()])) 
                result['errors'].append({
                    'url': res['url'],
                    'message' : res['error'] 
                })
            
        except Exception as e:
            result['errors'].append({
                'url': url,
                'message' : f'{e}' 
            })
        finally:
            await page.close()

        print(f'scrapping done.. {url}')

        async with self.sem:
            self.stream.write(json.dumps(result,indent=4) + ",")

        return result

    def chunker(self,idx,limit):
        max = min(limit,idx + 10)
        return [asyncio.create_task(self.scrape_util(self.domains[i])) for i in range(idx,max)]

    async def scrape(self,limit = None):
        async with async_playwright() as p:
            self.stream.write("[")

            self.browser = await p.chromium.launch() 

            try:
                limit = min(limit,len(self.domains)) if limit else len(self.domains)

                routines = []

                for i in range(0,limit,10): 
                    routines.extend(self.chunker(i,limit))
                    await asyncio.sleep(2)

                results = await asyncio.gather(*routines)

            except Exception as e:
                print('scrape: ',e)
            finally:
                await self.browser.close()
                self.stream.write("{}]")
                self.stream.close()

