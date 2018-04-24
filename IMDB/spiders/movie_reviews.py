import scrapy
import urllib

class QuotesSpider(scrapy.Spider):
    name = "movie_reviews"
    allowed_domains = ['www.imdb.com']
    start_urls = [
        'https://www.imdb.com/title/tt0451279/reviews?ref_=tt_urv'
    ]

    def parse(self, response):
        base_url = "https://www.imdb.com"
        for review in response.css('div.review-container'):
            yield {
                'rating': review.css('span.rating-other-user-rating span::text').extract_first(),
                'date': review.css('.review-date::text').extract(),
                'user_name': review.css('.display-name-link a::text').extract_first(),
                'user_id': review.css('.display-name-link a::attr(href)').extract_first().split('/')[2],
                'title': review.css('.title::text').extract_first(),
                'content': '\n'.join(review.css('.content div.text::text').extract())
            }
        data_key = response.css('.load-more-data::attr(data-key)').extract_first()
        ajax_url = '/title/tt0451279/reviews/_ajax?'
        self.logger.info('Data Key: %s', data_key)
        parameters = {"ref_": "undefined","paginationKey":data_key}
        if data_key is not None and ajax_url is not None:
            yield scrapy.Request(base_url + ajax_url + urllib.parse.urlencode(parameters),callback = self.parse)