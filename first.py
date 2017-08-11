#the future is possible
#I think i can
#So believe youself
#trust
#zheshi zai dev1shang 
import scrapy
from scrapy import Spider
from Final.items import FinalItem

class FinalSpider(Spider):
    name = 'final'
    #9412
    #开始爬取的初始链接
    start_urls = ['http://www.cnnvd.org.cn/web/vulnerability/querylist.tag',]
    def parse(self,response):
    	#取目标网站的前9页
     	for i in range(1,10):
     		pages = 'http://www.cnnvd.org.cn/web/vulnerability/querylist.tag?pageno={0}&repairLd='.format(i)
     		yield  scrapy.Request(pages,callback=self.parse_node)
     	#获取这些页面的所有链接
    def parse_node(self,response):
        pages = []
        pagenodes = response.xpath('.//div[@class="list_list"]//li')
        for  page in pagenodes:
      	    url = 'http://www.cnnvd.org.cn'+"".join(page.xpath('.//a[@class="a_title2"]/@href').extract())
            yield scrapy.Request(url, dont_filter=True, callback=self.parse_page)
    #对每个页面的每一个链接进行爬取。取出需要的数据，并给item中相应的字段进行赋值
    def parse_page(self,response):
    	items = []
        item = FinalItem() 
        nodelist1 = response.xpath('.//div[@class="detail_xq w770"]')
        item['flawname'] = nodelist1.xpath('./h2/text()')[0].extract()
        nodes = nodelist1.xpath('./ul')
        for quote in nodes:
            name = "".join(quote.xpath('./li[1]/span/text()')[0].extract().strip())
            index = name.rfind("C")
            item['CNNVDID'] = name[index:]
            item['harmlevel'] = quote.xpath('./li[2]/span/text()')[0].extract().strip(),
            item['CVEID'] = quote.xpath('./li[3]/a/text()')[0].extract().strip(),
            item['flawtype'] =quote.xpath('./li[4]/a/text()')[0].extract().strip(),
            item['releasetime']= quote.xpath('./li[5]/a/text()')[0].extract().strip(),
            item['damagetype'] =quote.xpath('./li[6]/a/text()')[0].extract().strip(),
            item['updatetime'] =quote.xpath('./li[7]/a/text()')[0].extract().strip(),
            item['company'] =quote.xpath('./li[8]/text()')[0].extract().strip(),
            item['flawsource'] =quote.xpath('./li[9]/text()')[0].extract().strip()
            items.append(item)
        return items
        print(item)
