import scrapy
import json

from scrapy.mail import MailSender
mailer = MailSender()

from tutorial.items import DmozItem
from scrapy.http import Request
from scrapy.contrib.spiders import CrawlSpider, Rule

class DmozSpider(scrapy.Spider):

    name = "dmoz"
    allowed_domains = ["proadvisorservice.intuit.com"]

    #min_lat = 24
    #max_lat = 50
    #min_long = -125
    #max_long = -65

    #haw_min_long = -175
    #haw_max_long = -153
    #haw_min_lat = 20
    #haw_max_lat = 30

    #alas_min_long = -170
    #alas_max_long = -140
    #alas_min_lat = 54
    #alas_max_lat = 71

    min_lat = 30
    max_lat = 31
    min_long = -100
    max_long = -99

    haw_min_long = 0
    haw_max_long = 0
    haw_min_lat = 0
    haw_max_lat = 0

    alas_min_long = 0
    alas_max_long = 0
    alas_min_lat = 0
    alas_max_lat = 0

    def start_requests(self):
        for i in range(self.min_lat, self.max_lat):
            for j in range(self.min_long, self.max_long):
                yield scrapy.Request('http://proadvisorservice.intuit.com/v1/search?latitude=%d&longitude=%d&radius=70&pageNumber=1&pageSize=&sortBy=distance' % (i, j),
                    dont_filter=True,
                    callback = self.parse)

        for i in range(self.haw_min_lat, self.haw_max_lat):
            for j in range(self.haw_min_long, self.haw_max_long):
                yield scrapy.Request('http://proadvisorservice.intuit.com/v1/search?latitude=%d&longitude=%d&radius=70&pageNumber=1&pageSize=&sortBy=distance' % (i, j),
                    dont_filter=True,
                    callback = self.parse)

        for i in range(self.alas_min_lat, self.alas_max_lat):
            for j in range(self.alas_min_long, self.alas_max_long):
                yield scrapy.Request('http://proadvisorservice.intuit.com/v1/search?latitude=%d&longitude=%d&radius=70&pageNumber=1&pageSize=&sortBy=distance' % (i, j),
                    dont_filter=True,
                    callback = self.parse)

    def parse(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        for x in jsonresponse['searchResults']:
            item = DmozItem()
            item['firstName'] = x['firstName'].lower()
            item['lastName'] = x['lastName'].lower()
            item['email'] = x['email'].lower()
            item['companyName'] = x['companyName'].lower()
            
            if x.get('phoneNumber'):
                item['phoneNumber'] = x['phoneNumber']
            else:
                item['phoneNumber'] = None

            o = x['qbopapCertVersions']
            d = x['papCertVersions']

            if not o:
              item['qbo'] = "FALSE"
            else:
              item['qbo'] = "TRUE"

            if not d:
              item['qbd'] = "FALSE"
            else:
              item['qbd'] = "TRUE"

            yield item

