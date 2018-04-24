import scrapy


class QuotesSpider(scrapy.Spider):
    name = "movie_reviews"
    start_urls = [
        'https://www.imdb.com/title/tt0451279/reviews?ref_=tt_urv'
    ]

    def parse(self, response):
        for review in response.css('div.review-container'):
            yield {
                'rating': review.css('span.rating-other-user-rating span::text').extract_first(),
                'date': review.css('.review-date::text').extract()
                'user_name': review.css('.display-name-link a::text').extract_first(),
                'user_id': review.css('.display-name-link a::attr(href)').extract_first().split('/')[2],
                'tags': quote.css('div.tags a.tag::text').extract(),
            }