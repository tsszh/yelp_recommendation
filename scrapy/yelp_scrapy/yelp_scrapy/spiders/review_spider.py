import scrapy, re, json, logging
from yelp_scrapy.items import Review
import yelp_scrapy.log

logger = logging.getLogger('my-logger')

input_file = 'business.Boston'

class ReviewSpider(scrapy.Spider):
    name = "reviews"

    def __init__(self, category=None, *args, **kwargs):
        super(ReviewSpider, self).__init__(*args, **kwargs)
        self.REVIEW_LIMIT = 1000
        self.countDict = {}

    def start_requests(self):
        urls = []
        with open('yelp_scrapy/data/%s.jl'%input_file) as f:
            for line in f:
                r = json.loads(line)
                urls.append("https://www.yelp.com/biz/%s"%r[0])
        f.close()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_review)

    def update_count(self, key, count):
        if not key in self.countDict:
            self.countDict[key] = 0
        remain = max(0, self.REVIEW_LIMIT - self.countDict[key])
        self.countDict[key] += count
        return min(count, remain)

    def parse_review(self, response):
        def parse_rating(x):
            return re.search('^\d\.\d', x).group(0)
        def parse_review_content(x):
            return re.sub("<br[^>]*>","\n",re.search("^<p[^>]*>(.*)</p>$", x).group(1))
        def check_equal_list(x):
            return len(x) == 0 or x.count(x[0]) == len(x)

        try:
            businessId = re.search('www.yelp.com/biz/([^/?]+)', response.url).group(1)
            filename = 'yelp_scrapy/data/%s.jl' % businessId

            uids = response.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), ' review ')\
             and @data-review-id]/@data-signup-object").re("user_id:(.*)")

            users = response.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), ' review ')\
             and @data-review-id]/div/div[@class='review-sidebar-content']/descendant::a[@class='user-display-name']/text()").extract()

            ratings = response.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), ' review ')\
                and @data-review-id]/div/div[@class='review-content']/descendant::div[contains(@class, 'i-star')]/@title").extract()

            reviews = response.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), ' review ')\
                and @data-review-id]/div/div[@class='review-content']/p[1]").extract()

            next_page = response.xpath("//div[contains(concat(' ', normalize-space(@class), ' '), ' review-pager ')\
                ]/descendant::a[contains(concat(' ', normalize-space(@class), ' '), ' next ')]/@href").extract_first()

            if not check_equal_list([len(uids), len(users), len(ratings), len(reviews)]):
                raise Exception("Length of users, ratings and reviews are not identical...")

            count = self.update_count(businessId, len(reviews))
            if count <= 0: next_page = None

            # Parse the item
            for id, u, r, c in zip(uids, users, ratings, reviews):
                if count <= 0: break
                count -= 1
                item = Review()
                item['filepath'] = input_file
                item['userId'] = id
                item['userName'] = u
                item['rating'] = parse_rating(r)
                item['business'] = businessId
                item['review'] = parse_review_content(c)
                yield item

            logger.info("Success - %s"%response.url)

            # Follow the link
            if next_page is not None:
                # next_page = response.urljoin(next_page)
                yield scrapy.Request(next_page, callback=self.parse_review)

        except Exception as e:
            logger.error(e)
            logger.error("Error in %s"%response.url)
