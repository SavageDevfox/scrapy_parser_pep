from urllib.parse import urljoin

import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        ctg_section = response.css('section#index-by-category tbody tr')
        for t_row in ctg_section:
            href = urljoin(
                self.start_urls[0], t_row.css('td a::attr(href)').get())
            number = t_row.xpath('./td[2]/a/text()').get()
            name = t_row.xpath('./td[3]/a/text()').get()
            yield response.follow(
                href,
                callback=self.parse_pep,
                meta={'number': number, 'name': name}
            )

    def parse_pep(self, response):
        data = {
            'number': response.meta['number'],
            'name': response.meta['name'],
            'status': response.xpath(
                '//dt[text()="Status"]/following-sibling::dd[1]/abbr/text()'
            ).get()
        }
        yield PepParseItem(data)
