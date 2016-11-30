import scrapy, re, json
from yelp_scrapy.items import Review

class QuotesSpider(scrapy.Spider):
    name = "reviews"

    def start_requests(self):
        urls = [
            'https://www.yelp.com/biz/coffee-project-new-york-new-york'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_review)


    def parse_review(self, response):
        def parse_rating(x):
            return re.search('^\d\.\d', x).group(0)
        def parse_review_content(x):
            return re.sub("<br[^>]*>","\n",re.search("^<p[^>]*>(.*)</p>$", x).group(1))
        def check_equal_list(x):
            return len(x) == 0 or x.count(x[0]) == len(x)

        items = []

        try:
            businessId = re.search('www.yelp.com/biz/([^/]+)', response.url).group(1)
            filename = 'yelp_scrapy/data/%s.jl' % businessId
            

            users = response.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), ' review ')\
             and @data-review-id]/div/div[@class='review-sidebar-content']/descendant::a[@class='user-display-name']/text()").extract()
            ratings = response.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), ' review ')\
                and @data-review-id]/div/div[@class='review-content']/descendant::div[contains(@class, 'i-star')]/@title").extract()
            reviews = response.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), ' review ')\
                and @data-review-id]/div/div[@class='review-content']/p[1]").extract()

            if not check_equal_list([len(users), len(ratings), len(reviews)]):
                self.logger.error(response.url)
                self.logger.error("Length of users, ratings and reviews are not identical...")
                return

            for u, r, c in zip(users, ratings, reviews):
                item = Review()
                item['user'] = u
                item['rating'] = parse_rating(r)
                item['business'] = businessId
                item['review'] = parse_review_content(c)
                items.append(item)
            return items
        except Exception as e:
            self.logger.error(e)
            self.logger.error("Something wrong with %s\n"%response.url)
            return items
