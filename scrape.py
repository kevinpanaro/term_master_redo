from scrapy.spider import Spider
from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import Selector
#from drexel_termmaster.items import DrexelTermmasterItem
from urlparse import urljoin
from scrapy.utils.response import get_base_url
from scrapy.http import Request
from scrapy import log
import types
import json
from StringIO import StringIO
import ast
# To run: "scrapy crawl term_crawler"


final_dict = {}
term_dict = {}
code_dict = {}
num_dict = {}
type_dict = {}
crn_dict = {}
term_to_scrape = "Spring Quarter 14-15"

def merge(x,y):
    # store a copy of x, but overwrite with y's values where applicable         
    merged = dict(x,**y)

    xkeys = x.keys()

    # if the value of merged[key] was overwritten with y[key]'s value           
    # then we need to put back any missing x[key] values                        
    for key in xkeys:
        # if this key is a dictionary, recurse                                  
        if type(x[key]) is types.DictType and y.has_key(key):
            merged[key] = merge(x[key],y[key])

    return merged

# Defines the Spider
class MySpider(Spider):
    name = "term_crawler_test"
    allowed_domains = ["drexel.edu"]
    start_urls = ["https://duapp2.drexel.edu/webtms_du/app?"]
    
    
    

    # Colleges
    # Selects all links on page that are class 'term'
    def parse(self, response):
        sel = Selector(response)
        titles = sel.xpath("//div[@class='term']")
        links = []
        title_name = []
        for titles in titles:
            link = titles.xpath("a/@href").extract()
            title = titles.xpath("a/text()").extract()
            title_name.append(title)
            links.append(link)
        # Makes links strings so they can be followed
        for link in range(len(links)):
            if title_name[link][0] == term_to_scrape:
                print links[link]
                sublink = urljoin(str(response.url), links[link][0])
                yield Request(sublink, callback=self.parse_colleges)

    # Subjects
    # Selects all links on page that are id 'sideLeft'
    def parse_colleges(self, response):
        sel = Selector(response)
        titles = sel.xpath("//div[@id='sideLeft']")
        links = []
        for titles in titles:
            link = titles.xpath("a/@href").extract()
            title = titles.xpath("a/text()").extract()
            links.append(link)
        # Makes links strings so they can be followed
        for link in links:
            for x in range(len(link)):
                sublink = urljoin(str(response.url), link[x])
                yield Request(sublink, callback=self.parse_subjects)

    # Classes
    # Selects all links on page that are class 'odd' of 'even'
    def parse_subjects(self, response):
        sel = Selector(response)
        titles = sel.xpath("//div[@class='odd'] | //div[@class='even']")
        links = []
        for titles in titles:
            link = titles.xpath("a/@href").extract()
            title = titles.xpath("a/text()").extract()
            links.append(link)
        # Makes links strings so they can be followed
        for link in links:
            for x in range(len(link)):
                sublink = urljoin(str(response.url), link[x])
                yield Request(sublink, callback=self.parse_classes)

    # CRN
    # Selects all CRN number, which are links
    def parse_classes(self, response):
        sel = Selector(response)
        titles = sel.xpath("//td//td//td//p")
        links = []
        for titles in titles:
            link = titles.xpath("a/@href").extract()
            title = titles.xpath("a/text()").extract()
            if len(title) != 0:
                links.append(link)
        # Makes links strings so they can be followed
        for link in links:
            for x in range(len(link)):
                sublink = urljoin(str(response.url), link[x])
                yield Request(sublink, callback=self.parse_crn)

    # Data Collection
    # Returns all valeus in a list, with text extracted (this takes a long time)
    def parse_crn(self, response):

        sel = Selector(response)
        titles = sel.xpath("//tr")
        items = []
        empty = []
        term_dict = {}

        # Main "folders"
        term = term_to_scrape
        subject_code = titles.xpath("//td[@class='odd'][1]/text()").extract()[0]
        course_number = titles.xpath("//td[@class='even'][2]/text()").extract()[0]
        instruction_type = titles.xpath("//td[@class='even'][5]/text()").extract()[0]
        crn = titles.xpath("//td[@class='even'][1]/text()").extract()[0]

        # stuff in CRN "folder"
        credits = titles.xpath("//td[@class='even'][3]/text()").extract()[0]
        title = titles.xpath("//td[@class='odd'][3]/text()").extract()[0]
        instructor = titles.xpath("//td[@class='odd'][4]/text()").extract()[0]
        max_enroll = titles.xpath("//td[@class='odd'][5]/text()").extract()[0]
        enroll = titles.xpath("//td[@class='even'][6]/text()").extract()[0]
        comments = titles.xpath("//td[@class='even']/table//td/text()").extract()[0]
        start_date = sel.xpath("//tr[@class='even']/td[1]/text()").extract()[0]
        end_date = sel.xpath("//tr[@class='even']/td[2]/text()").extract()[0]
        times = sel.xpath("//tr[@class='even']/td[3]/text()").extract()[0]
        days = sel.xpath("//tr[@class='even']/td[4]/text()").extract()[0]
        buidling = sel.xpath("//tr[@class='even']/td[5]/text()").extract()[0]
        room = sel.xpath("//tr[@class='even']/td[6]/text()").extract()[0]
        link = response.url


        # print term, subject_code, course_number, instruction_type, crn, credits, title, instructor,max_enroll,enroll,comments,start_date,end_date

        # make crn_dict
        crn_dict={crn:
                            {
                                "credits"   : credits,
                                "title"     : title,
                                "instructor": instructor,
                                "max_enroll": max_enroll,
                                "enroll"    : enroll,
                                "comments"  : comments,
                                "start_date": start_date,
                                "end_date"  : end_date,
                                "times"     : times,
                                "days"      : days,
                                "building"  : buidling,
                                "room"      : room,
                                # "link"      : link
                            }
                        }


        instruction_type_dict = {instruction_type: crn_dict}
        course_number_dict = {course_number: instruction_type_dict}
        subject_code_dict = {subject_code: course_number_dict}
        term_dict = {term: subject_code_dict}
        

        with open("drexel.json", "r+") as f:
            data = f.read()

            if len(data) == 0:
                f.write(str(term_dict))
            else:
                data_dict = ast.literal_eval(data)
                f.seek(0)
                f.truncate()
                json.dump((merge(term_dict,data_dict)), f)
            

                

            



        return None


        
        
        # for titles in titles:
        #     item['crn'] = titles.xpath("//td[@class='even'][1]/text()").extract()
        #     item['subject_code'] = titles.xpath("//td[@class='odd'][1]/text()").extract()
        #     item['course_number'] = titles.xpath("//td[@class='even'][2]/text()").extract()
        #     item['section'] = titles.xpath("//td[@class='odd'][2]/text()").extract()
        #     item['credits'] = titles.xpath("//td[@class='even'][3]/text()").extract()
        #     item['title'] = titles.xpath("//td[@class='odd'][3]/text()").extract()
        #     item['instructor'] = titles.xpath("//td[@class='odd'][4]/text()").extract()
        #     item['instruction_type'] = titles.xpath("//td[@class='even'][5]/text()").extract()
        #     item['max_enroll'] = titles.xpath("//td[@class='odd'][5]/text()").extract()
        #     item['enroll'] = titles.xpath("//td[@class='even'][6]/text()").extract()
        #     item['section_comments'] = titles.xpath("//td[@class='even']/table//td/text()").extract()




        #     item['start_date'] = sel.xpath("//tr[@class='even']/td[1]/text()").extract()
        #     item['end_date'] = sel.xpath("//tr[@class='even']/td[2]/text()").extract()
        #     item['times'] = sel.xpath("//tr[@class='even']/td[3]/text()").extract()
        #     item['days'] = sel.xpath("//tr[@class='even']/td[4]/text()").extract()
        #     item['building'] = sel.xpath("//tr[@class='even']/td[5]/text()").extract()
        #     item['room'] = sel.xpath("//tr[@class='even']/td[6]/text()").extract()
        #     item['link'] = response.url
        #     item['term'] = [u''.join(list(str(sel.xpath('//td/div[@align="left"]/text()').extract()[0])[13:]))]
        # items.append(item)
        # return items

        # f = open('drexel.json','w')
        # f.write(final_dict_json) 
        # f.close()

