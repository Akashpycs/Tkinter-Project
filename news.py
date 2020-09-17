from bs4 import BeautifulSoup
import requests

class TechNews:
    def __init__(self):
        self._url = "https://gadgets.ndtv.com/news"
        self.stuff = []
    def connect(self):
        try:
            url = requests.get(self._url)
            return url
        except Exception as e:
            print("Error Occured :- ", e)
            return None

    def fetch(self, connection):
        page = BeautifulSoup(connection.content, 'html.parser')
        content_div = page.select('.content_section')[0]
        content_block = content_div.find('div', attrs={'class':'content_block'})
        article_list = content_block.find_all('li')
        articles = map(self.list_filter, article_list)
        for article in articles: 
            if article != None:
                self.stuff.append(article)
        
    def list_filter(self, li_item):
        article = {}
        try:
            info_div = li_item.find('div', attrs={'class':'caption_box'})
            link_to_article = info_div.find('a')
            article_title = info_div.find('span', attrs={'class':'news_listing'}).get_text()
            writer, date = info_div.find('div', attrs={'class':'dateline'}).get_text().split(', ')
        except: 
            return None
        
        article["Url"] = link_to_article
        article["Title"] = article_title
        article["Writer"] = writer
        article["On"] = date

        return article

    #to check if it can connect to url or not 
    def agent(self):
        con_obj = self.connect()
        if con_obj.status_code == 200: 
            self.fetch(con_obj)
            return True
        else: return None
        
    def deliver(self):
        ready = self.agent()
        if ready: return self.stuff
        else: return None
    
if __name__ == "__main__":
    tn = TechNews()
    news = tn.deliver() #news contains many dict objects
    
    for i in news:
        print(i.get("Title"), end="\n")

        #for url, use i.get("Url")
        #for writer, use i.get("Writer")
        #for date, use i.get("On")
