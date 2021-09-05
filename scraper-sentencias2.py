
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

    def __init__(self, url = 'https://www.pjenl.gob.mx/SentenciasPublicas/Modulos/Penales.aspx', debug = True, last_page = None):
        '''
        Iniciamos Spider en la pagina de sentencias de Nuevo Leon.
        '''
        self.debug = debug
        self.url = url
        self.options = Options()
        self.options.add_argument("--disable-extensions")
        self.page = 1
        self.record_count = 0
        if not debug:
            self.options.add_argument('--log-level=3')
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--headless")
            # self.options.add_argument("--no-sandbox") # linux only
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(url)
        temp_data, self.page_index = pd.read_html(self.driver.page_source)
        self.data = temp_data.iloc[0:20,0:8]
        self.page_index = self.page_index.loc[0]
        self.visor_soup = None
        if last_page == None:
            self.last_page = math.inf
        else:
            self.last_page = last_page

    def get_tables(self):
        if self.page % 10 != 0:
            temp_data, __ = pd.read_html(self.driver.page_source)
            temp_data = temp_data.iloc[0:20,0:8]
        else:
            temp_data, self.page_index = pd.read_html(self.driver.page_source)
            self.page_index = self.page_index.loc[0]
        self.data = self.data.append(temp_data)
    
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

    def crawl_page(self):
        if self.page != 1:
            self.get_tables()
            self.driver.execute_script("scrollBy(0,-100000);")
        pdf_css_names = self.find_buttons('pdf')
        hrefs_arr = []
        for pdf_css_selector in pdf_css_names:
            self.open_viewer(pdf_css_selector)
            self.visor_soup = bs(self.driver.page_source.encode('utf8'), 'html.parser')
            hrefs_arr.append('https://www.pjenl.gob.mx' +  self.visor_soup.find('iframe')['src'])
            self.close_viewer()
        self.fill_hrefs(hrefs_arr)

    def open_viewer(self, pdf_css_selector):
        t0 = time.time()
        timeout = 0
        while timeout < 30:
            try:
                if self.debug:
                    print(pdf_css_selector)
                element = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, pdf_css_selector)))
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
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-default"))).click()
                WebDriverWait(spider.driver,5).until_not(EC.visibility_of_element_located((By.CLASS_NAME, 'btn-default')))
                break
            except Exception as e:
                timeout = t_null - time.time()
                if timeout >= 20:
                    print(e)
                    raise KeyboardInterrupt

    def crawl(self, only_pages = False):
        while self.page < self.last_page:
            stdout.write(f'Page {self.page} of {self.last_page}')
            if self.last_page == math.inf and self.page_index.iloc[-1] != '...':
                self.last_page = self.page_index.iloc[-2]
            if not only_pages:
                self.crawl_page()
            self.next_page()
            stdout.write('\r')
        self.fill_links()
        
    
    def next_page(self):
        if self.page < self.last_page:
            t0 = time.time()
            timeout = 0
            while timeout<15:
                try:
                    if (self.page + 1) % 10 == 1:
                        # Nextpage text
                        next_p_txt = '...'
                        if self.page >= 20:
                            WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.LINK_TEXT, next_p_txt)))
                            self.driver.find_elements_by_link_text(next_p_txt)[1].click()
                        else:
                            WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.LINK_TEXT, next_p_txt))).click()
                    else:
                        WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.LINK_TEXT, str(self.page + 1)))).click()
                
                    break
                except:
                    pass
                time.sleep(0.2)
                timeout = time.time() - t0
            if (self.page+1) % 10 == 0:
                WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.LINK_TEXT, '...')))
            else:
                WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.LINK_TEXT, str(self.page+2))))
            self.page += 1              
    
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
                if self.debug:
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
from pathlib import Path
path = Path('sentencias_400.xlsx').resolve()
spider = NuevoLeonSpider(debug =False, last_page = 10)
spider.crawl(only_pages=False)
spider.spit(path)

# %%
spider.kill()



# %%