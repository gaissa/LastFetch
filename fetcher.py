# -*- coding: utf-8 -*-


### LastFetch v.0.0.9

## AUTHOR: sugardrunk
#  URL: http://sugardrunk.devio.us

## ORIGIN: Andy Theyers
#  E-MAIL: andy.theyers@isotoma.com


import httplib2, itertools, urllib
from xml.etree import ElementTree

BASEURL = 'http://ws.audioscrobbler.com/2.0/user/%s/recenttracks.xml?limit=200&%s'

print '\n'
print 'PLEASE WAIT...'
print '\n'

class LastFetch1(object):    
    def __init__(self, user, start=None, end=None):
        self.user = user
        self.start = start
        self.end = end
        self.page = 1
        self.data = []
        xml = self.get()
        self.data.extend(self._process(xml))
        self.totpages = self._getpages(xml)
        while self.page < self.totpages:
            self.page += 1
            xml = self.get()
            self.data.extend(self._process(xml))
        self.data.sort()
        def grouper(row):
            return row[0]
        g = itertools.groupby(self.data, grouper)
        self.results = [ (len(list(v)), k) for k, v in g ]
        self.results.sort()
        self.results.reverse()
        
        
    def show(self, limit=None, morethan=None):
        if limit:
            return self.results[:limit]
        if morethan:
            return [ r for r in self.results if r[0] > morethan ]
        return self.results
    
    def get(self):
        data = {'page': self.page,}
        if self.start:
            data['from'] = self.start
        if self.end:
            data['to'] = self.end
        qs = urllib.urlencode(data)
        url = BASEURL % (self.user, qs,)
        h = httplib2.Http()
        resp, content = h.request(url)
        return content
        
    def _process(self, xml):
        t = ElementTree.fromstring(xml)
        def processtrack(track):
            return (
                track.find('artist').text,
                track.find('album').text,
                track.find('name').text,
                )
        return [ processtrack(tr) for tr in t.findall('track') ]
    
    def _getpages(self, xml):
        t = ElementTree.fromstring(xml)
        return int(t.get('totalPages', 1))        
    
if __name__ == '__main__':

    from datetime import datetime
    import time, sys

    months = [
        ('January', '2011-01-01', '2011-01-31',),
        ('February', '2011-02-01', '2011-02-28',),
        ('March', '2011-03-01', '2011-03-31',),
        ('April', '2011-04-01', '2011-04-30',),
        ('May', '2011-05-01', '2011-05-31',),
        ('June', '2011-06-01', '2011-06-30',),
        ('July', '2011-07-01', '2011-07-31',),
        ('August', '2011-08-01', '2011-08-31',),
        ('September', '2011-09-01', '2011-09-30',),
        ('October', '2011-10-01', '2011-10-31',),
        ('November', '2011-11-01', '2011-11-30',),
        ('December', '2011-12-01', '2011-12-31',),        
        ('Total', '2011-01-01', '2011-12-31',),
        ]

    format1 = '%Y-%m-%d'
    user = sys.argv[1]

    for month in months:
        print month[0]
        print '='*len(month[0])
        start = int(time.mktime(time.strptime(month[1], format1)))
        end = int(time.mktime(time.strptime(month[2], format1)))
        m = LastFetch1(user, start, end)
        data = m.show(morethan=0)
        totplays = 0
        for row in data:
            totplays += row[0]
        totartists = len(data)
        print 'Total artists :', totartists
        print 'Total tracks :', totplays
        for row in data:
            print row[0],":",row[1].encode('utf-8')
        print '\n'