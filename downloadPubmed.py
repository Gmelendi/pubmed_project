# encoding=utf-8

import pandas as pd
import pubmed_parser as pp
import requests
from bs4 import BeautifulSoup
import os
import json

class Pubmed_Downloader:
    
    def __init__(self, xml_path, download_folder='data'):
        self.xml_online = xml_path
        self.download_folder = download_folder
        
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)

        # download file from pubmed repository
        self.download()
        # load & parse file
        self.parse_xml()
        # save to local
        self.write_to_local()
        # delete source file
        self.delete_source_file()
        
            
    def download(self):
        r = requests.get(self.xml_online)
        if r.status_code == 200:
            self.xml_local = os.path.join(self.download_folder, self.xml_online.split('/')[-1])
            # check if file already exists
            if not os.path.exists(self.xml_local):
                with open(self.xml_local, 'wb') as f_out:
                    f_out.write(r.content)
                print('downloaded file: ', self.xml_local)
            else:
                print('using cached data for file: ', self.xml_local)

        else:
            print('could not download file %s, return status code: %d'%(self.xml_online, r.status_code))
        
    def parse_xml(self):
        
        dicts_out = pp.parse_medline_xml(self.xml_local,
                                 year_info_only=True,
                                 nlm_category=True,
                                 author_list=True,
                                 reference_list=False) # return list of dictionary

        self.df = pd.DataFrame(dicts_out)
        self.df = self.df.dropna(subset=['abstract'])
        self.df = self.df.loc[self.df.abstract != '']

        def parse_document(doc):
            return {
                'text': doc.abstract, 
                'meta': {
                    'title': doc.title, 
                    'pmid': doc.pmid,
                    'pubdate': doc.pubdate
                }
            }

        self.documents = self.df.apply(parse_document, axis=1).tolist()

    def write_to_local(self):
        json_fname = self.xml_local.replace('.xml.gz', '.json')
        with open(json_fname, 'w', encoding='utf-8') as f_out:
            json.dump(self.documents, f_out)

    def delete_source_file(self):
        if os.path.exists(self.xml_local):
            os.remove(self.xml_local)


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
