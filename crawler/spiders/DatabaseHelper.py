import sqlite3, sys
from urlparse import urlparse

class DatabaseHelper:
    
    conn = sqlite3.connect('blogs.db')
    c = conn.cursor()
    
    #create wppages table with Id, Netloc, Url, and Backlinks columns
    c.execute(
    "CREATE TABLE IF NOT EXISTS wppages (\
    Id INTEGER PRIMARY KEY AUTOINCREMENT, Backlinks INTEGER, \
    Netloc TEXT UNIQUE NOT NULL, Url TEXT UNIQUE NOT NULL);")
    
	  #create bloghome table with Id, Netloc, Title, Last_Active, and Backlinks columns
    c.execute(
    "CREATE TABLE IF NOT EXISTS bloghome (\
    Id INTEGER PRIMARY KEY AUTOINCREMENT, Backlinks INTEGER, \
    Netloc TEXT UNIQUE NOT NULL, Title TEXT NOT NULL, Last_Active TEXT NOT NULL);")
    conn.commit()
    conn.close()

    @staticmethod
    def check_new_url(url, tableName):
        """ check if url with the same netloc is in database.
        return false + increment backlink if in database
        return true if not in database """
		
        #connect to database and define variables
        conn = sqlite3.connect('blogs.db')
        netloc = urlparse(url)[1]
        t = (netloc,)
        c = conn.cursor()
        if tableName not in ['wppages', 'bloghome']:
            conn.close()
            return False
        else:
            c.execute('SELECT * FROM ' + tableName + ' WHERE Netloc=?', t)
            conn.commit()
            result = c.fetchone()
            if result is not None:
    		   #url with same netloc is already in database, increment backlink
                if result[1] is not sys.maxint:
                    back = result[1] + 1
                    c.execute(
                    'UPDATE wppages SET Backlinks=' + str(back) + \
                    ' WHERE Id=' + str(result[0]) + ';')
                    conn.close()
                    return False
            conn.close()
            return True
            

    @staticmethod
    def make_new_url(url, tableName, title=None, last_active=None):
        """ adds new url to database, 
        return false if there is an error """
        		
        conn = sqlite3.connect('blogs.db')
        c = conn.cursor()
        
        netloc = urlparse(url)[1]
        if (tableName == 'wppages'):
            # inserts into wppages table
            site = (netloc, url, 1)
            c.execute(
            'INSERT INTO wppages (Netloc, Url, Backlinks) VALUES (?,?,?)', site)
        elif (tableName == 'bloghome'): 
            # inserts into bloghome table
    			blog = (netloc, title, last_active, 1)
    			c.execute('INSERT INTO bloghome \
            (Netloc, Title, Last_Active, Backlinks) VALUES (?,?,?,?)', blog)
        else:
            conn.close()
            return False
        
        conn.commit()
        conn.close()
        return True


    


        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
