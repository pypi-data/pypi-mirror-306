import requests
import html2text
import logging

h = html2text.HTML2Text()
h.ignore_links = False
h.ignore_images = False
h.ignore_mailto_links = False
h.ignore_tables = False 
h.ignore_emphasis = False 

def webpage_to_text(url: str) -> str:
    try:
        res = requests.get(url)        
        t = h.handle(res.text)
        return t
    except requests.RequestException as e:
        raise
    except Exception as e:
        raise
