import pycurl
from datetime import datetime
import pyping

f = open('sites', 'r')

websites = []

# adds list of websites to array
# for some reason, baidu.com, globo, and amazonaws
# resulted in an error, so those sites were
# omitted.
for website in f.readlines():
    website = website.replace('\n', '')
    website = website.replace("https://",'')
    website = website.replace("http://",'')
    print(website)
    websites.append(website)

print(websites)

f.close()

class Data:
    websiteName = ''
    timeOfReading = ''
    dnsTime = ''
    dnsTimeTwo = ''
    ttfbTime = ''
    ttfbTimeTwo = ''
    pretTime = ''
    pretTimeTwo = ''
    #there is a reason that RTTthree is before the first
    #RTT. this is because when adding additional
    #RTT calculations after the second, we want to
    #maintain the position of RTT as -3, RTTtwo as -2, pr as -1
    RTTthree = ''
    RTT = ''
    RTTtwo = ''
    pingRTT = ''

# will hold values of class type data
dataArray = []

# will hold all the times which will later be averaged
timesArray = []

for website in websites:
    timesArray.append([])


# number of times to load each website per run of the script.
numPageLoads = 1

"""this function goes through each website in the websites array
and gets various data"""

for website in websites:
    try:
        print(website)
        for x in range(0, numPageLoads):

            data = Data()
            data.websiteName = website

            #sets up the pycurl part of the calc
            c = pycurl.Curl()
            c.setopt(pycurl.URL, website)
            c.setopt(pycurl.FOLLOWLOCATION, 1)

            data.timeOfReading = str(datetime.now())

            content = c.perform()

            TTFB = c.getinfo(pycurl.STARTTRANSFER_TIME) * 1000
            PRET = c.getinfo(pycurl.PRETRANSFER_TIME) * 1000
            DNS = c.getinfo(pycurl.CONNECT_TIME) * 1000
            RTT = TTFB - PRET

            # the following will reuse the above curl perform handle,
            # with different options to try to maintain the connection
            # but will reset the option in order to reload the page
            # for the RTTtwo variable in the class data.

            c.setopt(pycurl.URL, website)
            c.setopt(pycurl.FOLLOWLOCATION, 1)
            content = c.perform()

            TTFBtwo = c.getinfo(pycurl.STARTTRANSFER_TIME) * 1000
            PRETtwo = c.getinfo(pycurl.PRETRANSFER_TIME) * 1000
            DNStwo = c.getinfo(pycurl.CONNECT_TIME) * 1000
            RTTtwo = TTFBtwo - PRETtwo

            #third load!!
            c.setopt(pycurl.URL, website)
            c.setopt(pycurl.FOLLOWLOCATION, 1)
            content = c.perform()

            TTFBthree = c.getinfo(pycurl.STARTTRANSFER_TIME) * 1000
            PRETthree = c.getinfo(pycurl.PRETRANSFER_TIME) * 1000
            DNSthree = c.getinfo(pycurl.CONNECT_TIME) * 1000
            RTTthree = TTFBthree - PRETthree

            data.ttfbTime = str(TTFB)
            data.ttfbTimeTwo = str(TTFBtwo)
            data.pretTime = str(PRET)
            data.pretTimeTwo = str(PRETtwo)
            data.dnsTime = str(DNS)
            data.dnsTimeTwo = str(DNStwo)
            data.RTTthree = str(RTTthree)
            data.RTT = str(RTT)
            data.RTTtwo = str(RTTtwo)


            c.close()

            #begin working with the system ping
            r = ''

            r = pyping.ping(website.replace('www.',''))
            data.pingRTT = str(r.avg_rtt)

            timesArray[websites.index(website)].append(TTFB)

            # this is an important line which later
            # allows all the data to be added to the file
            # because the for loop below goes through this
            # array and adds to file the contents of it
            dataArray.append(data)
    except:
        f = open('dysfunctional_sites','a')
        f.write(website)



timeAverages = []

f = open('newtestaggregatelog.txt', 'a')
x = open('newtestaggregatelog.txt', 'r')

# we want to check if the labels for the values has already been printed,
# if not then we want to print it since it is the first run on the log.
if(x.readline() != 'tstamp,sitename,dns time,dns time two,pret time,pret time two,ttfb time,ttfb time two,RTTthree,RTT,RTTtwo,pingRTT\n'):
    f.write('tstamp,sitename,dns time,dns time two,pret time,pret time two,ttfb time,ttfb time two,RTTthree,RTT,RTTtwo,pingRTT\n')

x.close()

# goes through data array and prints each value to file log
for datum in dataArray:
    line = datum.timeOfReading
    line += ',' + datum.websiteName
    line += ',' + datum.dnsTime
    line += ',' + datum.dnsTimeTwo
    line += ',' + datum.pretTime
    line += ',' + datum.pretTimeTwo
    line += ',' + datum.ttfbTime
    line += ',' + datum.ttfbTimeTwo
    line += ',' + datum.RTTthree
    line += ',' + datum.RTT
    line += ',' + datum.RTTtwo
    line += ',' + datum.pingRTT
    f.write(line)
    f.write('\n')

f.close()
