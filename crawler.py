from creepy import Crawler

class MyCrawler(Crawler):
    def process_document(self, doc):
        if doc.status == 200:
            if "http://www.tudogostoso.com.br/especiais/receitas/" in doc.url:
                if ".html" in doc.url:
                    print '[%d] %s' % (doc.status, doc.url)
                    filename = 'crawled_files/'+doc.url[49:]+'.html'
                    file = open(filename, "w")
                    file.write(doc.text)
                    file.close()
        # Do something with doc.text (the content of the page)
        else:
            pass

crawler = MyCrawler()
crawler.set_follow_mode(Crawler.F_SAME_HOST)
crawler.add_url_filter('\.(jpg|jpeg|gif|png|js|css|swf)$')
crawler.crawl('http://www.tudogostoso.com.br/')