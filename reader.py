import sqlite3
import urlparse

def print_database():
    print 'cats'
    conn = sqlite3.connect('blogCrawler.db')
    c = conn.cursor()
    c.execute("SELECT * FROM blogs;")
    conn.commit()
    entry = c.fetchall()
    print len(entry)
    for x in entry:
        print 'dogs'
        print x[1]
    conn.close()

    


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
