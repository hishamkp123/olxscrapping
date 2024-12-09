import scrapy
from ..items import ProductItem

class OLXSpider(scrapy.Spider):
    name = 'olx_spider'
    allowed_domains = ["olx.in"]
    start_urls = ['https://www.olx.in/kozhikode_g4058877/for-rent-houses-apartments_c1723']

    headers = {
        'Accept': '/',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Host': 'www.olx.in',
        'Origin': 'https://www.olx.in',
        'Referer': 'https://www.olx.in/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'TE': 'trailers',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0'
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        # Select all product links using XPath
        listings = response.xpath('//a[starts-with(@href, "/item/")]')  # Match links starting with "/item/"

        for listing in listings:
            # Extract the relative URL of the product
            product_link = listing.xpath('@href').get()
            if product_link:
                # Construct the absolute URL
                absolute_url = response.urljoin(product_link)
                # Make a new request to the product page
                yield scrapy.Request(
                    url=absolute_url,
                    headers=self.headers,
                    callback=self.parse_product
                )
        next_pages = response.xpath('//a[@data-aut-id="pageItem"]/@href').getall()
        for next_page in next_pages:
            # Construct the absolute URL for the next page and yield the request
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(
                url=next_page_url,
                headers=self.headers,
                callback=self.parse
            )

    def parse_product(self, response):
        # Create a ProductItem instance
        item = ProductItem()
        item['property_name'] = response.xpath('//h1[@data-aut-id="itemTitle"]/text()').get()
        
        # Extract breadcrumb values using XPath
        breadcrumbs = response.xpath('//ol[@class="rui-2Pidb"]/li/a/text()').getall()
        item['breadcrumbs'] = breadcrumbs
        
        # Extract price, amount, and currency using XPath
        price = response.xpath('//span[@data-aut-id="itemPrice"]/text()').get()
        if price:
            currency = price[0]  # Currency symbol (₹)
            amount = price[1:].strip().replace(',', '')  # The numeric part
            item['price'] = {'amount': amount, 'currency': currency}
        
        # Extract other details using XPath
        item['image_url'] = response.xpath('//img[@data-aut-id="defaultImg"]/@src').get() or None
        item['description'] = response.xpath('//div[@data-aut-id="itemDescriptionContent"]/p/text()').getall()
        item['seller_name'] = response.xpath('//div[@class="eHFQs"]/text()').get()
        item['location'] = response.xpath('//span[@class="_1RkZP"]/text()').get()
        item['property_type'] = response.xpath('//span[@data-aut-id="value_type"]/text()').get()
        item['bedrooms'] = response.xpath('//span[@data-aut-id="value_rooms"]/text()').get()
        item['bathrooms'] = response.xpath('//span[@data-aut-id="value_bathrooms"]/text()').get()

        yield item