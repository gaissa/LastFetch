# -*- coding: utf-8 -*-


## LastFetch v.0.1.0

##  Fetch annual monthly and total stats of a specific user from last.fm
##  Copyright (C) 2011 Sugardrunk <http://sugardrunk.devio.us>

##  Forked from 'lastyear' by Andy Theyer <https://github.com/offmessage/lastyear>


import httplib2, itertools, urllib
from xml.etree import ElementTree

BASEURL = 'http://ws.audioscrobbler.com/2.0/user/%s/recenttracks.xml?limit=200&%s'

# print title
title1 = 'LastFetch v.0.1.0'
print '\n'
print title1
print '='*len(title1), '\n'
fetch_year = raw_input('YEAR TO FETCH: ')
print '\nPlease be patient as each month may take a lot of time to retrieve...'
print '\n'

class LastFetch1(object):
    def __init__(main, user, start=None, end=None):        
        main.user = user
        main.start = start
        main.end = end
        main.page = 1
        main.data = []
        xml = main.get()
        main.data.extend(main._process(xml))
        main.totpages = main._getpages(xml)
        while main.page < main.totpages:
            main.page += 1
            xml = main.get()
            main.data.extend(main._process(xml))
        main.data.sort()
        def grouper1(row):
            return row[0]
        g = itertools.groupby(main.data, grouper1)
        main.results = [ (len(list(v)), k) for k, v in g ]
        main.results.sort()
        main.results.reverse()     
        
    def show(main, limit=None, morethan=None):
        if limit:
            return main.results[:limit]
        if morethan:
            return [ r for r in main.results if r[0] > morethan ]
        return main.results
    
    def get(main):
        data = {'page': main.page,}
        if main.start:
            data['from'] = main.start
        if main.end:
            data['to'] = main.end
        qs = urllib.urlencode(data)
        url = BASEURL % (main.user, qs)
        h = httplib2.Http()
        resp, content = h.request(url)
        return content
       
    def _process(main, xml):
        t = ElementTree.fromstring(xml)
        def processtrack(track):
            return (
                track.find('artist').text,
                track.find('album').text,
                track.find('name').text,
                )
        return [ processtrack(tr) for tr in t.findall('track') ]
    
    def _getpages(main, xml):
        t = ElementTree.fromstring(xml)
        return int(t.get('totalPages', 1))              
    
if __name__ == '__main__':

    from datetime import datetime
    import time, sys

    months1 = [
        ('January', fetch_year + '-01-01', fetch_year + '-01-31',),
        ('February', fetch_year + '-02-01', fetch_year + '-02-28',),
        ('March', fetch_year + '-03-01', fetch_year + '-03-31',),
        ('April', fetch_year + '-04-01', fetch_year + '-04-30',),
        ('May', fetch_year + '-05-01', fetch_year + '-05-31',),
        ('June', fetch_year + '-06-01', fetch_year + '-06-30',),
        ('July', fetch_year + '-07-01', fetch_year + '-07-31',),
        ('August', fetch_year + '-08-01', fetch_year + '-08-31',),
        ('September', fetch_year + '-09-01', fetch_year + '-09-30',),
        ('October', fetch_year + '-10-01', fetch_year + '-10-31',),
        ('November', fetch_year + '-11-01', fetch_year + '-11-30',),
        ('December', fetch_year + '-12-01', fetch_year + '-12-31',),        
        ('Annual Total:', fetch_year + '-01-01', fetch_year + '-12-31',),
        ]

    format1 = '%Y-%m-%d'
    user = sys.argv[1]

    for month in months1:
        
        print month[0]
        print '='*len(month[0])
        start = int(time.mktime(time.strptime(month[1], format1)))
        end = int(time.mktime(time.strptime(month[2], format1)))
        months2 = LastFetch1(user, start, end)
        
        # play count limit & print stats
        countLimit1 = 20
        data = months2.show(morethan = countLimit1)
        totplays = 0
        for row in data:
            totplays += row[0]
        totartists = len(data)
        print 'Total artists =', totartists
        print 'Total tracks =', totplays
        print
        for row in data:
            print row[0],"=",row[1].encode('utf-8')

        raw_input('\n\nPRESS ENTER TO CONTINUE...''\n')

        # write output to file        
        ##br1 = '</br></br></br>'
        ##br2 = '</br></br>'
        ##write1 = month[0]
        ##write2 = 
        ##file1 = open('output.html','a')
        ##file1.write (br1)
        ##file1.write(write1)
        ##file1.write (br2)
        ##file1.write(write2)
        ##file1.close()

# the end 
try:
    print 'ANNUAL AVERAGE TRACKS PER ARTIST =', totplays / totartists
except (ZeroDivisionError):
    print '0'
    pass

raw_input('\n\nPRESS ENTER TO EXIT...')
print '\n'