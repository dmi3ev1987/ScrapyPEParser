import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        for table_row in response.css('tr.row-odd, tr.row-even'):
            abbr = table_row.css('abbr::text').get()
            if abbr:
                current_pep_url = table_row.css(
                    'a.reference::attr(href)'
                ).get()
                name = table_row.css('a.reference::attr(title)').get()
                number = table_row.css('a.reference::text').get()

                yield response.follow(
                    current_pep_url,
                    callback=self.parse_pep,
                    meta={
                        'number': int(number),
                        'name': name.split(' – ')[-1].strip(),
                    },
                )

    def parse_pep(self, response):
        status = response.css('dt:contains("Status") + dd abbr::text').get()

        data = {
            'number': response.meta['number'],
            'name': response.meta['name'],
            'status': status,
        }
        yield PepParseItem(data)
