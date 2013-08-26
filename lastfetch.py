# -*- coding: utf-8 -*-


## LastFetch v.0.1.1

##  Fetch monthly and annual total stats of a specific user from last.fm
##  Copyright (C) 2011-2012 Sugardrunk <http://koti.tamk.fi/~c1jkahko/>

##  Forked from 'lastyear'
##  by Andy Theyer <https://github.com/offmessage/lastyear>


from xml.etree import ElementTree

import httplib2
import itertools
import sys
import time
import urllib

# url setup
scrobbler = 'http://ws.audioscrobbler.com/2.0/user' + \
          '/%s/recenttracks.xml?limit=200&%s'

# title setup
title = 'LastFetch v.0.1.1'
print '\n\n', title
print '=' * len(title)

# user input
try:
    fetch_year = raw_input('YEAR TO FETCH: ')
    play_count = input('MINIMUM PLAY COUNT: ')
    print '\nplease wait a little for each month...''\n\n'
except:
    pass


# set class
class LastFetch(object):

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

        def grouper(row):
            return row[0]

        g = itertools.groupby(main.data, grouper)

        main.results = [(len(list(v)), k) for k, v in g]
        main.results.sort()
        main.results.reverse()

    def show(main, limit=None, morethan=None):
        if limit:
            return main.results[:limit]
        if morethan:
            return [r for r in main.results if r[0] > morethan]
        return main.results

    def get(main):
        data = {'page': main.page, }
        if main.start:
            data['from'] = main.start
        if main.end:
            data['to'] = main.end
        qs = urllib.urlencode(data)
        url = scrobbler % (main.user, qs)
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

        return [processtrack(tr) for tr in t.findall('track')]

    def _getpages(main, xml):
        t = ElementTree.fromstring(xml)
        return int(t.get('totalPages', 1))

if __name__ == '__main__':

    try:
        singlemonth = [
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
            ('Annual Total', fetch_year + '-01-01', fetch_year + '-12-31',),
            ]
        format = '%Y-%m-%d'
        user = sys.argv[1]

        for month in singlemonth:
            print month[0]
            print '=' * len(month[0])
            start = int(time.mktime(time.strptime(month[1], format)))
            end = int(time.mktime(time.strptime(month[2], format)))
            m = LastFetch(user, start, end)
            cl = play_count
            data = m.show(morethan=cl)  # somehow funny

            totartists = len(data)
            totplays = 0

            for row in data:
                totplays += row[0]

            print 'Total artist count =', totartists
            print 'Total track count =', totplays, '\n'

            for row in data:
                print row[0], '=', row[1].encode('utf-8')

            raw_input('\npress enter to continue...''\n\n')
    except:
        print '\nSorry! I am breaking down over here!''\n\n'

    try:
        print 'Annual average track count per artist =', totplays / totartists
    except:
        print '0'

raw_input('\npress enter to exit...''\n\n')
