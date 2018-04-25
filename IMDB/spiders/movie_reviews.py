import scrapy
import urllib

class QuotesSpider(scrapy.Spider):
    name = "movie_reviews"
    allowed_domains = ['www.imdb.com']
    base_url = "https://www.imdb.com"

    def start_requests(self):
        # Note: id_type can only be two values, title/user
        # ID is either user_id or title_id
        yield scrapy.Request(self.base_url + '/{}/{}/reviews?ref_=tt_urv'.format(self.id_type,self.id))

    def parse(self, response):
        
        for review in response.css('div.review-container'):
            user_id = review.css('.display-name-link a::attr(href)').extract_first().split('/')[2] if self.id_type == 'title' else self.id
            title_id = review.css('.lister-item-header a::attr(href)').extract_first().split('/')[2] if self.id_type == 'user' else self.id
            #user_name = review.css('.display-name-link a::text').extract_first()
            yield {
                'rating': review.css('span.rating-other-user-rating span::text').extract_first(),
                'date': review.css('.review-date::text').extract_first(),
                'title_id': title_id,
                'user_id': user_id,
                'title': review.css('.title::text').extract_first(),
                'content': '\n'.join(review.css('.content div.text::text').extract())
            }
        data_key = response.css('.load-more-data::attr(data-key)').extract_first()
        ajax_url = '/{}/{}/reviews/_ajax?'.format(self.id_type,self.id)
        self.logger.info('Data Key: %s', data_key)
        parameters = {"ref_": "undefined","paginationKey":data_key}
        if data_key is not None and ajax_url is not None:
            yield scrapy.Request(self.base_url + ajax_url + urllib.parse.urlencode(parameters),callback = self.parse)