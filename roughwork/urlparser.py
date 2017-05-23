# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 11:47:12 2016

@author: Emily
"""

from urlparse import urlparse
 
u = urlparse('http://www.adventurewithashley.blogspot.ca/2016/05/buynosaur-taobao-agent-review.html')
scheme = u[0]
netloc = u[1]
path = u[2]
params = u[3]
query = u[4]
fragment = u[5]

print "scheme: " + scheme + "\n" + "netloc: " + netloc + "\n" + "path: " + path + "\n"