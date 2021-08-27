# encoding=utf-8

import pandas as pd
import pubmed_parser as pp
import requests
from bs4 import BeautifulSoup
import os

class Pubmed_Downloader:
    
    def __init__(self, xml_path, download_folder='data'):
        self.xml_online = xml_path
        self.download_folder = download_folder
        
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)

        self.download()
        self.parse_xml()
        self.to_csv()
        
            
    def download(self):
        r = requests.get(self.xml_online)
        if r.status_code == 200:
            self.xml_local = os.path.join(self.download_folder, self.xml_online.split('/')[-1])
            
            with open(self.xml_local, 'wb') as f_out:
                f_out.write(r.content)
                
            print('downloaded file: ', self.xml_local)
        else:
            print('could not download file %s, return status code: %d'%(self.xml_online, r.status_code))
        
    def parse_xml(self):
        
        dicts_out = pp.parse_medline_xml(self.xml_local,
                                 year_info_only=True,
                                 nlm_category=True,
                                 author_list=True,
                                 reference_list=False) # return list of dictionary
        self.df = pd.DataFrame(dicts_out)
        
    def to_csv(self):
        self.csv_local = self.xml_local.replace('xml', 'csv')
        self.df.to_csv(self.csv_local, compression='infer', index=False)

if __name__ == '__main__':

    url_path = 'https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/'
    r = requests.get(url_path)

    soup = BeautifulSoup(r.text, 'html.parser')
    pubmed_files = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href.endswith('.xml.gz'):
            pubmed_files.append(url_path + href)

    n = 5
    for i, pubmed_file in enumerate(pubmed_files):
        if i < n:
            Pubmed_Downloader(pubmed_file)
