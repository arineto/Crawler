from creepy import Crawler

crawled_site = 'http://www.imdb.com/search/title?year=2015,2015&title_type=feature&sort=moviemeter,asc'
desired_link = 'http://www.imdb.com/title/'

class MyCrawler(Crawler):
    def process_document(self, doc):
        if doc.status == 200:
            if desired_link in doc.url and ( len(doc.url) == len(desired_link) + 10):
                new_url =  doc.url[len(desired_link):]
                if new_url[-1] == '/':
                    print '[%d] %s' % (doc.status, doc.url)
                    filename = 'crawled_files/'+new_url[:new_url.index('/')]+'.html'
                    file = open(filename, "w")
                    file.write(doc.text)
                    file.close()
        # Do something with doc.text (the content of the page)
        else:
            pass

crawler = MyCrawler()
crawler.set_follow_mode(Crawler.F_SAME_HOST)
crawler.add_url_filter('\.(jpg|jpeg|gif|png|js|css|swf)$')
crawler.crawl(crawled_site)