
# %%
# class SpiderSentencias(CrawlSpider)
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import math
from sys import stdout
import pandas as pd 
import time

class NuevoLeonSpider:

    def __init__(self, data = None, url = 'https://www.pjenl.gob.mx/SentenciasPublicas/Modulos/Penales.aspx', debug = True, last_page = None, long_wait = 20, medium_wait = 6, short_wait = 2, chunks = None, log_level = 1):
        '''
        Iniciamos Spider en la pagina de sentencias de Nuevo Leon.
        '''
        self.debug = debug
        self.url = url
        self.options = Options()
        self.options.add_argument("--disable-extensions")
        self.crawler_page = 1
        self.active_page = 1
        self.record_count = 0
        if self.debug:
            self.log_level = log_level
        else:
            self.log_level = min(log_level, 1)
        if not debug:
            self.options.add_argument('--log-level=3')
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--headless")
            # self.options.add_argument("--no-sandbox") # linux only
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(url)
        temp_data, self.page_index = pd.read_html(self.driver.page_source)
        if data == None:
            self.data = data
        else:
            self.data = pd.DataFrame.from_records(data)
        self.page_index = self.page_index.loc[0]
        self.soup = bs(self.driver.page_source.encode('utf8'), 'html.parser')
        self.total_sentences = int(self.soup.find('span', {'id':'lblTotalPenal'}).text)
        
        # Waiting times
        self.long_wait = long_wait
        self.medium_wait = medium_wait
        self.short_wait = short_wait
        
        if last_page == None:
            self.last_page = math.ceil(self.total_sentences/20.0)
        else:
            self.last_page = last_page
        # Chunks
        self.chunks = chunks


    def get_tables(self):
        if self.crawler_page % 10 != 0:
            temp_data, __ = pd.read_html(self.driver.page_source)
            temp_data = temp_data.iloc[0:20,0:8]
        else:
            temp_data, self.page_index = pd.read_html(self.driver.page_source)
            self.page_index = self.page_index.loc[0]
        if isinstance(self.data, pd.DataFrame):
            self.data = self.data.append(temp_data)
        else:
            self.data = temp_data
    
    def fill_hrefs(self, hrefs_arr):
        self.data.loc[self.data['Sentencia'].isna(), 'Sentencia'] = hrefs_arr

    def find_buttons(self, btn_type = 'pdf'):
        '''
        Función para buscar botones de PDFs en las pagina 'Sentencias Publicas' del estado de Nuevo Leon.
        '''
        soup = bs(self.driver.page_source, 'html.parser')
        elements = []
        if btn_type.lower() == 'pdf':
            for td_tag in soup.find_all('td'):
                try:
                    temp = td_tag.findChild()['id']
                    elements.append(f'#{temp}')
                except:
                    pass
        elif btn_type.lower() == 'pages':
            links = soup.findAll('a')
            for link in links:
                if 'javascript:' in link['href']:
                    elements.append(link['href'])
        elif btn_type.lower() == 'pdf_source' or 'source':
            return 
        else:
            raise ValueError (f'Invalid button type: {btn_type}')
        return elements

    def progress_bar(self, i):
        stdout.write(f'\rPage {self.active_page} of {self.last_page}: {i+1}/{20}')
        if self.log_level > 1:
            stdout.write('\n')
    
    def crawl_page(self):
        self.get_tables()
        if self.active_page != 1:
            self.driver.execute_script("scrollBy(0,-100000);")
        pdf_css_names = self.find_buttons('pdf')
        hrefs_arr = []
        for i,pdf_css_selector in enumerate(pdf_css_names):
            if self.log_level > 1:
                stdout.write('\n')
            else:
                self.progress_bar(i)
            self.open_viewer(pdf_css_selector)
            WebDriverWait(self.driver, self.long_wait).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-default")))
            visor_soup = bs(self.driver.page_source.encode('utf8'), 'html.parser')
            if self.log_level > 2:
                print('https://www.pjenl.gob.mx' +  visor_soup.find('iframe')['src'])
            hrefs_arr.append('https://www.pjenl.gob.mx' +  visor_soup.find('iframe')['src'])
            self.close_viewer()
        self.fill_hrefs(hrefs_arr)
        # duplicate checks
        self.data.drop_duplicates(['Sentencia'], keep = 'first', inplace =True)

    def open_viewer(self, pdf_css_selector):
        t0 = time.time()
        timeout = 0
        while timeout < 40:
            try:
                if self.log_level>1:
                    print(pdf_css_selector)
                element = WebDriverWait(self.driver, self.long_wait).until(EC.element_to_be_clickable((By.CSS_SELECTOR, pdf_css_selector)))
                element.click()
                break
            except Exception as e:
                timeout = time.time() - t0
                time.sleep(.2)
                if timeout >= 30:
                    print(e)
                    raise KeyboardInterrupt 
                try:
                    element.click()
                    break
                except:
                    pass
            
    def close_viewer(self):
        # Close pdf - viewer
        timeout = 0
        t_null = time.time()
        while timeout<20:
            try:
                WebDriverWait(self.driver, self.long_wait).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-default"))).click()
                WebDriverWait(spider.driver, self.long_wait).until_not(EC.visibility_of_element_located((By.CLASS_NAME, 'btn-default')))
                break
            except Exception as e:
                timeout = t_null - time.time()
                if timeout >= 20:
                    print(e)
                    raise KeyboardInterrupt

    def crawl(self, start_from = 1):
        for page in range(start_from, self.last_page + 1):
            self.go_to(page)
            self.crawl_page()
            time.sleep(self.medium_wait)
            if self.active_page > self.crawler_page:
                self.crawler_page = self.active_page
            self.fill_links()

        
        
        
        
        # if self.chunks != None:
        #     aux = range(self.last_page)
        #     # Creamos lista de pedazos
        #     iterator  = (aux[pos:pos + self.chunks] for pos in range(0, len(aux), self.chunks))
        # else:
        #     iterator = range(self.last_page)


        # for x in iterator:
        #     # Running scrapping whole data
        #     if self.chunks == None: # x is a number                
        #         page = x + 1
        #         tries = 0
        #         while tries < 3:
        #             # if not test_page_navigation:
        #             try:
        #                 if page != 1:
        #                     self.go_to(page)
        #                 self.crawler_page = page 
        #                 self.crawl_page()
        #                 time.sleep(self.medium_wait)
        #                 break
        #             except:
        #                 self.driver.get(self.url)
        #                 self.go_to(page)


            # Scrapping in chunks
            # else: 
            #     for y in x:
            #         page = y + 1
            #         if not test_page_navigation:
            #             self.crawl_page()
            #             time.sleep(self.medium_wait)
            #             self.go_to_page(page)
            #     self.fill_links()


        
    def go_to(self, target_page = 1):
        # Navigates into given page number
        tries = 0
        timeout = 0
        t_null = time.time()
        while self.active_page != target_page and tries < 2000:
            provisional_target = target_page
            try:
                if target_page < self.active_page or self.active_page <= 10:
                    occurrence = 0
                else:
                    occurrence = 1
                try:
                    self.driver.find_element_by_link_text(str(target_page))
                    provisional_target_text = str(target_page)
                except:
                    provisional_target = self.active_page - (self.active_page % 10) 
                    if self.active_page % 10 == 0:
                        if self.active_page < target_page:
                            provisional_target += 1
                        else:
                            provisional_target -= 11
                    else:
                        if occurrence == 1 or self.active_page < 10:
                            provisional_target += 11
                        
                    provisional_target_text = '...'
                
                    if self.log_level>3:
                        print(f'Clicking: {provisional_target_text}[{occurrence}]')
                        print('Expected active page:', provisional_target)
                        time.sleep(self.medium_wait)

                self.click_page_number(provisional_target_text, occurrence)
    
                if self.has_page_shifted(provisional_target):
                    self.active_page = provisional_target
                else:
                    if self.log_level > 1:
                        print(f'Have not reached page ({provisional_target})')
                    provisional_target
                    raise RuntimeError(f"Unable to shfit into page {target_page}")
                    tries += 1
            except:
                timeout = time.time() - t_null
                if timeout > 420:
                    raise TimeoutError(f'Could not reach {target_page}')

    def click_page_number(self, number, occurrence):
        if number == '...':
            WebDriverWait(self.driver, self.long_wait + 10).until(EC.element_to_be_clickable((By.LINK_TEXT, number)))
            self.driver.find_elements_by_link_text(number)[occurrence].click()
            time.sleep(self.long_wait)
        else:
            WebDriverWait(self.driver, self.long_wait + 10).until(EC.element_to_be_clickable((By.LINK_TEXT, number))).click()
        
    
    def has_page_shifted(self, to_page):
        # When we are in page i then the element with text "i" cannot be found. We check if it has indeed disappeared.
        try:
            return WebDriverWait(self.driver, self.medium_wait).until_not(EC.element_to_be_clickable((By.LINK_TEXT, str(to_page))))
        except:
            return False

    def fill_links(self):
        def make_soup(url):
            no_soup = True
            attempts = 0
            while no_soup and attempts < 10:
                try:
                    html = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}).content
                    no_soup = False
                    break
                except:
                    attempts += 1
                    time.sleep(.5)
            return bs(html, "html.parser")

        def get_pdf_url(url):
            import re
            try:
                prefix = 'https://www.pjenl.gob.mx/SentenciasPublicas/PDFVisor/'
                soup = make_soup(url)
                pattern = re.compile(r"var DEFAULT_URL = '(.*?)';")
                script = soup.find('script', text = pattern)
                pdf_url = prefix + re.search(pattern, str(script)).group(1)
                if self.log_level>2:
                    print(pdf_url)
            except:
                pdf_url = ''
            return pdf_url

        self.data['PDF Links'] = [get_pdf_url(x) for x in self.data['Sentencia']]

    def spit(self, path = 'data.xlsx'):
        self.data.to_excel(path)
        return self.data

    def kill(self):
        self.driver.quit()
        print("Spider's dead.")
                
# %%
tries = 0
data = None
crawler_page = 1
while tries < 5:
    try:
        spider = NuevoLeonSpider(debug = False, log_level= 1, data = data)
        spider.crawl(start_from = crawler_page)
    except Exception as e:
        print(tries, e)
        crawler_page = spider.crawler_page
        data = spider.data.to_dict('records')
        spider.kill()
        tries += 1
    

# %%
spider.spit()

# %%
spider.kill()

# from pathlib import Path
# path = Path('sentencias_400.xlsx').resolve()
# spider = NuevoLeonSpider(debug =False, last_page = 10)
# spider.crawl(test_page_navigation=False)
# spider.spit(path)
# spider.kill()

# %%

import itertools
# %%
