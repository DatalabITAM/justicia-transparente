
# %%
# class SpiderSentencias(CrawlSpider)
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import math
from sys import stdout
import pandas as pd 
import time


# %%
class NuevoLeonSpider:


    def __init__(self, url = 'https://www.pjenl.gob.mx/SentenciasPublicas/Modulos/Penales.aspx', headless = False):
        '''
        Iniciamos Spider en la pagina de sentencias de Nuevo Leon.
        '''
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
        self.data, self.page_index = pd.read_html(self.driver.page_source)
        self.page_index = self.page_index.loc[0]
        self.visor_soup = None
        self.pdf_sources = []
        self.last_page = math.inf


    def get_tables(self):
        if self.page % 10 != 0:
            temp_data, __ = pd.read_html(self.driver.page_source)
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
        tries = 0
        while tries < 5:
            try:
                pdf_css_names = self.find_buttons('pdf')
                break
            except:
                time.sleep(2)
                tries += 1
                if tries == 5:
                    raise KeyboardInterrupt
        for pdf_name in pdf_css_names:
            while tries < 5:
                try:
                    self.driver.find_element_by_css_selector(pdf_name).click()
                    break
                except:
                    time.sleep(2)
                    tries += 1
                    if tries == 5:
                        raise KeyboardInterrupt
            self.visor_soup = bs(self.driver.page_source.encode('utf8'), 'html.parser')
            self.pdf_sources.append('https://www.pjenl.gob.mx' +  self.visor_soup.find('iframe')['src'])
            tries = 0
            while tries < 5:
                time.sleep(2)
                try:
                    self.driver.find_element_by_class_name('btn-default').click()
                    break
                except:
                    time.sleep(2)
                    tries += 1
                    if tries == 5:
                        raise KeyboardInterrupt
    
    def crawl(self):
        while self.page < self.last_page:
            stdout.write(f'Page {self.page} of {self.last_page}')
            if self.last_page == math.inf and self.page_index.iloc[-1] != '...':
                self.last_page = self.page_index.iloc[-2]
            self.page_crawler()
            if self.page < self.last_page:
                self.page += 1
                element = self.driver.find_element_by_link_text(str(self.page))
                self.driver.execute_script("arguments[0].click();", element)
            stdout.write('\r')
    
    def spit(self, path = 'data.xlsx'):
        self.data.to_excel(path)
        return self.data

    def squash(self):
        self.driver.quit()
                
            
# %%
spider = NuevoLeonSpider()
spider.crawl()

# %%
