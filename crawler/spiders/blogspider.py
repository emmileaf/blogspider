# -*- coding: utf-8 -*-
import scrapy, re, urllib2
from urlparse import urlparse
from bs4 import BeautifulSoup

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
		  calls on database helpers and check methods"""
        
        unique = self.check_entry(response)
        # checks if the homepage blog is already in database
        if unique:
            wppost = self.check_wp(response)
            # check if page is a wordpress page and adds to database
            if wppost:
                review = self.check_review(response)
                # check if page contains review posts
                if review:
                    self.find_home(response) 
                    # finds homepage of review blog and adds to database
    
    
    def check_entry(self, response):
        """ checks if page is already a subpage of a blog in the database"""
        
        pageurl = str(response.request.url)
        unique = DatabaseHelper.check_new_url(pageurl, 'bloghome')
        return unique
        
            
    def check_wp(self, response):
        """identifies whether the page as an unvisited wordpress page
        and adds to database or updates backlinks accordingly"""
        # To-do: Improve filter- other pages can also contain this keyword
		
        url = str(response.request.url)
        iswp = False
        unique = False
        wpfound = 0
        for href in response.css('link::attr(href)'):
            # for debugging: print type(href)
            wpmatch = re.search('wp', str(href))
            if wpmatch:
                wpfound += 1
            if wpfound >= 3:
                iswp = True
                unique = DatabaseHelper.check_new_url(url, "wppages") 
                # checks if wp page has not been previously stored
                if unique:
                    DatabaseHelper.make_new_url(url, "wppages")
                    # adds page into database
                break
        return iswp

            
    def check_review(self, response):
        """identifies whether the wordpress page is a review post
        or contains review posts"""
        # To-do: Improve filter- sometimes shops also contain this keyword
        
        pageurl = str(response.request.url)
        page = urllib2.urlopen(pageurl).read()
        
        soup = BeautifulSoup(page, 'html.parser')        
        result = soup.find(string=re.compile(r'.*\b[Rr]eview\b.*'))
        return result
        

    def find_home(self, response):
        """find homepage of identified target blog post,
        and stores it in the blogs database"""
        
        pageurl = str(response.request.url)

        homeurl = urlparse(pageurl)[0] + "://" + urlparse(pageurl)[1]
        title = self.get_title(homeurl)
        last_active = self.get_active(homeurl)
        # insert into database
        DatabaseHelper.make_new_url(pageurl, 'bloghome', title, last_active)
            
    
    def get_title(self, url):
        """returns title of blogpage if possible"""
        
        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, 'html.parser')
        title = soup.title.string
        if not title: 
            title = 'Untitled'
        return title
    
    
    def get_active(self, url):
        """returns date of last published post if possible"""
        # To-do: find a way to accomodate for differen date/time locations on the page
        
        page = urllib2.urlopen(url).read()
        soup = BeautifulSoup(page, 'html.parser')
        
        # timestamp in tags under attr datetime
        for i in soup.find_all(re.compile("(date.*)|(time.*)")):
            if i.has_attr('datetime'):
                date = i['datetime']
                return date
                
        # timestamp in tags as a title with property datePublished
        for i in soup.find_all(attrs={"itemprop" : "datePublished" }):
                date = i['title']
                return date
        
        """
        cases commented out for being too page-specific and not containing year
               
        # date displayed as text with "post-date" included in class name
        for i in soup.find_all(attrs={"class" : "post-date" }):
            node = i.contents[1]
            date = node.find_all(text=True)
            return date[0]
        
        # date displayed as text with "date" included in class name
        for i in soup.find_all(attrs={"class" : "date"}):
            node = i.contents[0]
            date = node.find_all(text=True)
            return date
            
        """
        
        return "Unknown"
        
	 
    




