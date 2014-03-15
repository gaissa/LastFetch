# -*- coding: utf-8 -*-


## LastFetch v.0.1.3

##  Fetch monthly and annual total stats of a specific user from last.fm
##  Copyright (C) 2011-2014 Sugardrunk <http://koti.tamk.fi/~c1jkahko/>

##  Forked from 'lastyear'
##  by Andy Theyer <https://github.com/offmessage/lastyear>


from xml.etree import ElementTree
import calendar
import httplib2
import itertools
import sys
import time
import urllib


# debug output <True/False>
debug = False

# main error message
error = '\nSorry! Does not compute! Try again :D\n\n'

# url setup
scrobbler = 'http://ws.audioscrobbler.com/2.0/user' + \
            '/%s/recenttracks.xml?limit=200&%s'

# title setup and print
title = 'LastFetch v.0.1.3'
print '\n\n', title, '\n', '=' * len(title)

# user input
try:
    fetch_year = raw_input('YEAR TO FETCH: ')
    play_count = input('MINIMUM PLAY COUNT: ')
    print '\n\nLOADING January . . .\n'
except:
    error = '\nPLEASE! GIVE CORRECT INPUT (NUMERALS ONLY)!'
    print error

# fetch the xml data
class LastFetch(object):

    # init all
    def __init__(main, user, start = None, end = None):
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

    # limit the result
    def show(main, limit = None, morethan = None):
        if limit:
            return main.results[:limit]
        if morethan:
            return [r for r in main.results if r[0] > morethan]
        return main.results

    # get and return the data
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

    # process the data
    def _process(main, xml):
        t = ElementTree.fromstring(xml)

        def processtrack(track):
            return (track.find('artist').text,
                    track.find('album').text,
                    track.find('name').text,)

        return [processtrack(tr) for tr in t.findall('track')]

    # get total pages
    def _getpages(main, xml):
        t = ElementTree.fromstring(xml)
        return int(t.get('totalPages', 1))

# print the month
def mon(month):
    print month
    print '=' * len(month)

# run the main
if __name__ == '__main__':
    try:
        format = '%Y-%m-%d'
        user = sys.argv[1]

        for m in range(1,13):
            monthend = calendar.monthrange(int(fetch_year), m)[1]
            firstday = "%s-%02d-%02d" % (fetch_year, m, 1)
            lastday = "%s-%02d-%02d" % (fetch_year, m, monthend)
            month = calendar.month_name[m]

            if m < 12:
                nextmonth = calendar.month_name[m + 1]
            else:
                nextmonth = 'Annual Total'

            start = int(time.mktime(time.strptime(firstday, format)))
            end = int(time.mktime(time.strptime(lastday, format)))

            mon(month)
            m = LastFetch(user, start, end)

            cl = play_count
            data = m.show(morethan = cl)

            totalartists = len(data)
            totalplays = 0

            for row in data:
                totalplays += row[0]

            print 'Total artist count =', totalartists
            print 'Total track count =', totalplays, '\n'

            for row in data:
                print row[0], '=', row[1].encode('utf-8')

            raw_input('\nPRESS ENTER TO CONTINUE . . .')

            print '\n\nLOADING', nextmonth, '. . .\n'

        ann = ['Annual Total', fetch_year + '-01-01', fetch_year + '-12-31']

        start = int(time.mktime(time.strptime(ann[1], format)))
        end = int(time.mktime(time.strptime(ann[2], format)))

        mon(ann[0])
        m = LastFetch(user, start, end)

        cl = play_count
        data = m.show(morethan = cl)

        totalartists = len(data)
        totalplays = 0

        for row in data:
            totalplays += row[0]

        print 'Total artist count =', totalartists
        print 'Total track count =', totalplays, '\n'

        for row in data:
            print row[0], '=', row[1].encode('utf-8')
    except Exception, e:
        if debug == False:
            print error
            sys.exit()
        else:
            print '\n', e

    try:
        annual = totalplays / totalartists
        print '\n\nAnnual average track count per artist =', annual
    except:
        print 'Nothing to show!'

# exit
raw_input('\n\nPRESS ENTER TO EXIT . . .\n\n')