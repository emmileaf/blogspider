# -*- coding: utf-8 -*-
import scrapy, re
from urlparse import urlparse
from crawler.items import BlogspiderItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from DatabaseHelper import DatabaseHelper


class BlogSpider(CrawlSpider):
    """ a spider for crawling through pages given starting url"""
	
    name = "blogspider"
    start_urls = ["https://wordpress.com/"]
    rules = (
        # call parse_link on all links from starting url
        Rule(LinkExtractor(), callback='parse_link', follow=True),)
    
    def parse_link(self, response):
		""" extracts link on newly visited page,
		calls on database helper too see if link is unique,
		and checks if page is a wordpress blog page"""
		
        pageurl = str(response.request.url)
        unique = DatabaseHelper.check_new_url(pageurl) # fix this dupfilter
        if unique:
            self.check_wp(response)
            
    def check_wp(self, response):
		"""if there are 3+ instances of wp in href tags 
		in the html body, then identify the page as a wordpress 
		blog, and store it in the blogposts database"""
		
        url = str(response.request.url)
        iswp = False
        wpfound = 0
        for href in response.css('link::attr(href)'):
            print type(href)
            wpmatch = re.search('wp', str(href))
			# by regex pattern matching
            if wpmatch:
                wpfound += 1
            if wpfound >= 3:
                iswp = True
                break
        if iswp:
            DatabaseHelper.make_new_url(url, "Blogposts")
            print "post found:", url #for debugging
			self.check_review(response) # checks if blog page is a review post
	
	
	def check_review(self, response):
		"""identifies review blog posts as target for store sponsorship"""
		
		isReview = False
		titlelist = response.css('title::text').extract()
		for title in titlelist:
			result = re.match('*[Rr]eview*', title)
			if (result.group(0)):
				isReview = True
				break
		if isReview:
			self.find_home(response) # finds homepage of blog
			return True

	 
	def find_home(self, response):
		"""find homepage of identified target blog post,
		and stores it in the blogs database"""
		
		homeurl = urlparse(response)[0] + urlparse(response)[1]
		DatabaseHelper.make_new_url(url, "Blogs")
            print "blog found:", url #for debugging
	 
	 
	 
	 
	"""define item fields and extract that from blog home"""
	# blog title, link, author, contact info

    




