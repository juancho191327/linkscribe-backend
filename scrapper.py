from transformers import pipeline
from bs4 import BeautifulSoup
import requests
import tensorflow as tf

class Scrapper(object):
    def __init__(self): 
        self.summarizer = pipeline("summarization",framework='tf')

    def read_url(self,url:str):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        results = soup.find_all(['p','h1','h2'])
        text = [result.text for result in results]
        return text

    def text_processor(self,text):
        max_chunk = 500
        ARTICLE = ' '.join(text)
        ARTICLE = ARTICLE.replace('.', '.<eos>')
        ARTICLE = ARTICLE.replace('?', '?<eos>')
        ARTICLE = ARTICLE.replace('!', '!<eos>')
        sentences = ARTICLE.split('<eos>')
        current_chunk = 0 
        chunks = []
        for sentence in sentences:
            if len(chunks) == current_chunk + 1: 
                if len(chunks[current_chunk]) + len(sentence.split(' ')) <= max_chunk:
                    chunks[current_chunk].extend(sentence.split(' '))
                else:
                    current_chunk += 1
                    chunks.append(sentence.split(' '))
            else:
                print(current_chunk)
                chunks.append(sentence.split(' '))

        for chunk_id in range(len(chunks)):
            chunks[chunk_id] = ' '.join(chunks[chunk_id])
        return chunks
    
    def summarize(self,chunks):
        res = self.summarizer(chunks, max_length=100, min_length=30, do_sample=False)
        text=' '.join([summ['summary_text'] for summ in res])
        return text

    def obtener_titulo(self, url: str):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        results = soup.find_all('h1')
        titulo = [result.text for result in results]
        return titulo
        


        
    def obtener_imagen(self, url: str):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        imagen_tag = soup.find('meta', attrs={'property': 'og:image'} or {'name': 'og:image'})
        if imagen_tag:
            imagen_url = imagen_tag.get('content')
        else:
            imagen_url = 'data:image/jpeg;base64,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'
        return imagen_url