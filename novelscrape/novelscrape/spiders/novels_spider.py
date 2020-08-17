# To force scrapy to output string instead of unicode in JSON file,
# add the following line in settings.py:
# FEED_EXPORT_ENCODING = 'utf-8'

# use the following cmd to output to JSON:
# scrapy crawl novels -o novels.json
import scrapy

class NovelsSpider(scrapy.Spider):
    name = "novels"

    start_urls = [
        'https://channel.jd.com/1713-3258.html'
    ]

    def parse(self, response):
        for novel in response.css('.mc .p-name').xpath('.//a'):
            yield {
                'title': novel.css('::text').get(),
                'detail_page': novel.attrib['href'],
            }