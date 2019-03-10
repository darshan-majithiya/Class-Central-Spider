# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.exceptions import CloseSpider
from scrapy.http import Request
from math import ceil

class ClasscentralSpider(Spider):
    name = 'ClassCentral'
    allowed_domains = ['class-central.com']
    start_urls = ['http://www.class-central.com/subjects/']

    def __init__(self, domain=None):
        self.domain = domain 
    
    def parse(self, response):
        if self.domain is not None: # checking if the argument is provided
            domain_url = response.xpath('//*[contains(@title, "' + self.domain.title() + '")]/@href').extract_first()
            
            if domain_url is not None:
                self.logger.info('Scraping "' + self.domain + '" domain...')
                yield Request(response.urljoin(domain_url), callback=self.get_all_courses, meta={'domain': self.domain})
            
            else:
                raise CloseSpider('Invalid domain.')

        else:
            self.logger.info('Scraping all domains...')
            domain_urls = response.xpath('//*[@class="text--blue"]/@href').extract()
            
            for domain_url in domain_urls:
                domain = response.xpath('//a[@href = "' + domain_url + '"]/span[contains(@class,"head-3")]/text()').extract_first()   
                yield Request(response.urljoin(domain_url), callback=self.get_all_courses, meta={'domain': domain})

    def get_all_courses(self, response):
        domain = response.meta['domain']
        courses = response.xpath('//a[contains(@class, "course-name")]')
        for course in courses:
            course_url = course.xpath('.//@href').extract_first() 
            yield Request(response.urljoin(course_url), callback=self.parse_course, meta={'domain': domain})
        
        page_no = response.xpath('//*[@id="show-more-courses" and @style=""]/@data-page').extract_first()
        if page_no is not None:
            yield Request(response.urljoin('?page='+ page_no), callback=self.get_all_courses,  meta={'domain': domain})

    def parse_course(self, response):
        
        # Extracting the data points
        try: 
            domain = response.meta['domain']
            course_title = response.xpath('//*[@id="course-title"]/text()').extract_first().strip()
            university = response.xpath('//*[@id="course-title"]/following-sibling::p/a[1]/text()').extract_first()
            rating = response.xpath('//div[@class="margin-vert-medium"]//strong/text()').extract_first()
            review_count = response.xpath('//a[@id="read-reviews"]/text()').extract_first()
            registered_students = response.xpath('//*[@id="read-reviews"]/following-sibling::strong/text()').extract_first()
            tags = response.xpath('//h4[contains(text(), "Tags")]/following-sibling::div/a/text()').extract()
            start_date = response.xpath('//*[@id = "sessionOptions"]/option/@content').extract_first()
            tags = [tag.strip() for tag in tags]
            subject = response.xpath('//li/strong[text()="Subject"]/following-sibling::a/text()').extract_first().strip()
            cost = response.xpath('//li/strong[text()="Cost"]/following-sibling::span/text()').extract_first().strip()
            session = response.xpath('//li/strong[text()="Session"]/following-sibling::a/text()').extract_first().strip()
            language = response.xpath('//li/strong[text()="Language"]/following-sibling::a/text()').extract_first().strip()
            duration = response.xpath('//li/strong[text()="Duration"]/following-sibling::span/text()').extract_first().strip()
            faculty = response.xpath('//h4[contains(text(),"Taught by")]/following-sibling::div/text()').extract_first().strip()
            try:
                certificate = response.xpath('//li/strong[text()="Certificate"]/following-sibling::span/text()').extract_first()
            except Exception:
                certificate = None # if no certification is available
       
            yield {
                'domain': domain,
                'subject': subject,
                'course_title': course_title,
                'university': university,
                'faculty': faculty,
                'rating': rating,
                'review_count': review_count,
                'registered_students': registered_students,
                'tags': tags,
                'cost': cost,
                'start_date': start_date,
                'session': session,
                'language': language,
                'certificate': certificate,
                'duration':duration
            }
        except Exception:
            pass
        


