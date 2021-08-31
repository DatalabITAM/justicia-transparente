
# %%
# class SpiderSentencias(CrawlSpider)
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import math
from sys import stdout
import pandas as pd 
import time


# %%
class NuevoLeonSpider:


    def __init__(self, url = 'https://www.pjenl.gob.mx/SentenciasPublicas/Modulos/Penales.aspx', headless = False, debug = True):
        '''
        Iniciamos Spider en la pagina de sentencias de Nuevo Leon.
        '''
        self.debug = debug
        self.url = url
        self.options = Options()
        self.options.add_argument("--disable-extensions")
        self.page = 1
        self.record_count = 0
        if headless:
            self.options.add_argument("--disable-gpu")
            self.options.add_argument("--headless")
            # self.options.add_argument("--no-sandbox") # linux only
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(url)
        temp_data, self.page_index = pd.read_html(self.driver.page_source)
        self.data = temp_data.loc[::-2]
        self.page_index = self.page_index.loc[0]
        self.visor_soup = None
        self.pdf_sources = []
        self.last_page = math.inf


    def get_tables(self):
        if self.page % 10 != 0:
            temp_data, __ = pd.read_html(self.driver.page_source)
            temp_data = temp_data.loc[::-2]
        else:
            temp_data, self.page_index = pd.read_html(self.driver.page_source)
            self.page_index = self.page_index.loc[0]
        self.data = self.data.append(temp_data)
        
    
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

    def page_crawler(self):
        if self.page != 1:
            self.get_tables()
            self.driver.execute_script("scrollBy(0,-100000);")

        
        pdf_css_names = self.find_buttons('pdf')
            
        for pdf_css_selector in pdf_css_names:
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
            self.visor_soup = bs(self.driver.page_source.encode('utf8'), 'html.parser')
            self.pdf_sources.append('https://www.pjenl.gob.mx' +  self.visor_soup.find('iframe')['src'])
            self.close_viewer()
            
                
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


    def crawl(self):
        while self.page < self.last_page:
            stdout.write(f'Page {self.page} of {self.last_page}')
            if self.last_page == math.inf and self.page_index.iloc[-1] != '...':
                self.last_page = self.page_index.iloc[-2]
            self.page_crawler()
            self.next_page()
            stdout.write('\r')
    
    def next_page(self):
        if self.page < self.last_page:
            self.page += 1              
            t0 = time.time()
            timeout = 0
            while timeout<15:
                try:
                    WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.LINK_TEXT, str(self.page)))).click()
                    break
                except:
                    pass
                time.sleep(0.2)
                timeout = time.time() - t0
            WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.LINK_TEXT, str(self.page+1))))
            
        

    def spit(self, path = 'data.xlsx'):
        self.data.to_excel(path)
        return self.data

    def kill(self):
        self.driver.quit()
                
            
# %%
spider = NuevoLeonSpider()

# %%
# %%
spider.crawl()
# %%
spider.kill()
# %%
spider.driver.find_element_by_class_name('btn-default')

# %%
spider.
# %%

# %%
btn_0 = '#ContentPlaceHolder1_gdvPenal_ImgBtnSentencia_0'
# %%

# %%
spider.driver.ScrollTo(0,0)
# %%
