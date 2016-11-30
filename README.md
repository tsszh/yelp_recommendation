# yelp_recommendation
Course project for Big Data Analysis

## Spider

### How to start the spider
1. Update `scrapy/yelp_scrapy/yelp_scrapy/data/business.jl`
2. `cd scrapy/yelp_scrapy`
3. `sh start.sh` (MacOS)

### business.jl

Each line is a valid json list:

```
[
    <business id>::string,
    <business name>::string,
    <rating>::float,
    <category>::list,
    <location>::dict
]
```

Here is an example
```
["matcha-cafe-wabi-new-york", "Matcha Cafe Wabi", 4.5, [["Coffee & Tea", "coffee"] ], {"latitude": 40.72355, "longitude": -73.98291 }]
```

### Output

For each record in `business.jl`, spider will fetch and parse the data from `https://www.yelp.com/biz/<business id>`. The results will be saved into `scrapy/yelp_scrapy/yelp_scrapy/data/<business id>.jl` in JSON Lines format.

```
[
    <user name>::string,
    <rating>::string,
    <business name>::string,
    <review>:: string
]
```

Example:

```
["Moon R.", "1.0", "matcha-cafe-wabi-new-york", "I don't know what the matcha latte tastes like because it's closed at 6:30 pm on a Friday!\n\nBetter get here a hour earlier than the closing time!"]
```
